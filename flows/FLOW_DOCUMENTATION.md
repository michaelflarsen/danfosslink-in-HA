# Node-RED Flow Documentation

Detailed explanation of the Danfoss Link CC integration flow structure.

---

## 📋 Flow Overview

The main flow is structured into logical sections (groups) that handle different aspects of the integration:

```
┌─────────────────────────────────────────────────────────────┐
│                      MAIN FLOW GROUPS                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  1. Alexa Authentication & Keep-Alive              │    │
│  │     - Establishes connection to Alexa              │    │
│  │     - Refreshes daily (86400 sec)                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                              ↓                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  2. Data Fetching from Danfoss via Alexa          │    │
│  │     - Runs every 5 minutes (310 sec)               │    │
│  │     - Queries all configured rooms                 │    │
│  │     - Returns temperature & setpoint               │    │
│  └─────────────────────────────────────────────────────┘    │
│                              ↓                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  3. Data Processing & Indexing                     │    │
│  │     - Parses Alexa response                        │    │
│  │     - Creates indexed data structure               │    │
│  │     - Separates temperature and setpoint           │    │
│  └─────────────────────────────────────────────────────┘    │
│                              ↓                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  4. Flow Variable Storage                          │    │
│  │     - Saves setpoint to flow memory (rum1-rum8)    │    │
│  │     - Used for further processing                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                              ↓                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  5. Home Assistant Sensors                         │    │
│  │     - 8x Temperature sensors (Rum1-Rum8)          │    │
│  │     - 8x Setpoint sensors                          │    │
│  │     - Sends data to Home Assistant                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔌 Detailed Component Breakdown

### Group 1: Alexa Authentication & Keep-Alive

**Purpose:** Maintain stable connection to Alexa API

**Nodes:**

| Node Name | Type | Function |
|-----------|------|----------|
| **Ny forspørgelse** | Inject | Manual trigger for new authentication |
| **Alexa Auth (init)** | alexa-remote-init | Creates fresh authentication token |
| **Gem auth til flow** | Change | Stores auth token in flow memory |
| **Start og Gentagelse** | Inject | Recurring auth refresh (daily) |
| **Set auth fra flow** | Change | Retrieves stored auth for reuse |
| **Alexa Init (persistent)** | alexa-remote-init | Initializes persistent connection |

**Flow:**
```
[Manual Trigger] → [Fresh Auth] → [Save to Memory]
                                       ↓
[Daily Interval] → [Retrieve Auth] → [Persistent Init]
```

**Key Points:**
- Runs once at startup + daily
- Keeps connection alive for 24 hours
- Must complete before data fetching starts

---

### Group 2: Data Fetching from Danfoss

**Purpose:** Query Danfoss Link CC devices via Alexa

**Nodes:**

| Node Name | Type | Function |
|-----------|------|----------|
| **Hvert 5 min** | Inject | Triggers query every 5 minutes |
| **Hent Danfoss Link Info fra Alexa** | alexa-remote-smarthome | Main query node |
| **debug 112** | Debug | Shows raw Alexa response |

**Configuration Required:**
- Must add your rooms in the "Hent Danfoss" node
- Each room must be set to "All Properties"
- Rooms populated from Alexa account

**Limitations:**
- ⚠️ 5-minute minimum interval (Alexa API limit)
- ⚠️ Cannot go faster or will get throttled
- ✅ Can be slowed down if needed (change 310 seconds)

---

### Group 3: Data Processing & Indexing

**Purpose:** Transform Alexa response into usable data structure

**Key Node:** **Index data** (Function Node)

**Input:** Raw array from Alexa with structure:
```javascript
[
  {
    topic: "Rum1",
    payload: {
      temperature: { value: 21.5 },
      targetSetpoint: { value: 22.0 }
    }
  },
  // ... more rooms
]
```

**Processing Logic:**
```javascript
1. Create empty data object
2. For each room in response:
   - Extract temperature value
   - Store as data[roomname] = temp
3. For each room in response:
   - Extract setpoint value
   - Store as data["Setpoint " + roomname] = setpoint
4. Return indexed data
```

**Output:**
```javascript
{
  "Rum1": 21.5,
  "Rum2": 20.3,
  "Setpoint Rum1": 22.0,
  "Setpoint Rum2": 21.0,
  // ...
}
```

**Debug Node:** "find rum her" can be enabled to troubleshoot room names

---

### Group 4: Flow Variable Storage

**Purpose:** Store setpoint values for use throughout flow

**Node:** **Setpoint til flow.rumX** (Change Node)

**Actions:**
- Extracts `payload["Setpoint Rum1"]` → stores as `flow.rum1`
- Extracts `payload["Setpoint Rum2"]` → stores as `flow.rum2`
- ... up to `flow.rum8`

**Use Cases:**
- Used for flow logic decisions
- Available throughout the flow
- Can be used in function nodes

**Note:** Temperature values also available as `flow.temperaturX`

---

### Group 5: Link Out/In Distribution

**Purpose:** Route data to multiple destinations

**Nodes:**

| Node | In/Out | Purpose |
|------|--------|---------|
| **Send til export** | Out | Routes to two destinations |
| **Modtag til Temperatur** | In | Links to temperature sensors |
| **Modtag til Setpunkt** | In | Links to setpoint sensors |

**Data Distribution:**
```
[Index Data] → [Send til export]
                 ├→ [Modtag til Temperatur] → [Rum1-8 Sensors]
                 └→ [Modtag til Setpunkt] → [Setpoint Rum1-8 Sensors]
```

---

### Group 6: Home Assistant Sensor Nodes

**Purpose:** Create/update sensors in Home Assistant

**Sensor Structure:**

For each room (example for Rum1):

| Node | Type | Entity | State |
|------|------|--------|-------|
| **Rum1** | ha-sensor | `sensor.danfoss_..._1` | `payload.Rum1` |
| **Setpoint Rum1** | ha-sensor | `sensor.danfoss_..._setpoint_1` | `payload["Setpoint Rum1"]` |

**Configuration Per Sensor:**
```
- Entity Name: Danfoss_[RoomName]
- Unit: °C
- Device Class: temperature
- State Class: measurement
```

**Entity IDs in Home Assistant:**
- `sensor.danfoss_stue` (Room1)
- `sensor.danfoss_soveværelse` (Room2)
- etc.

---

## 📊 Data Flow Diagram

```
┌──────────────┐
│  Danfoss Link│ ← Physical heating controller
├──────────────┤
│    Alexa App │ ← Connection via Alexa skill
├──────────────┤
│              │
│  Node-RED    │
│              │
│ ┌──────────────────────────────────┐
│ │ 1. Auth: Create/Refresh Token   │
│ └────────┬─────────────────────────┘
│          │
│ ┌────────▼─────────────────────────┐
│ │ 2. Query: Get Temperature Data   │
│ └────────┬─────────────────────────┘
│          │
│ ┌────────▼─────────────────────────┐
│ │ 3. Process: Index & Parse Data   │
│ └────────┬─────────────────────────┘
│          │
│ ┌────────▼─────────────────────────┐
│ │ 4. Store: Save to Flow Memory    │
│ └────────┬─────────────────────────┘
│          │
│ ┌────────▼──────────────────────────────┐
│ │ 5. Distribute: Split to two outputs  │
│ │    ├─→ Temp sensors                  │
│ │    └─→ Setpoint sensors              │
│ └────────┬──────────────────────────────┘
│          │
│ ┌────────▼─────────────────────────────────┐
│ │ 6. Publish: Send to Home Assistant      │
│ └──────────────────────────────────────────┘
│
├──────────────┤
│ Home         │ ← All room sensors available
│ Assistant    │   in HA UI and automations
└──────────────┘
```

---

## 🔧 Configuration Points

### Must Configure:

1. **Alexa Account**
   - Property: Each room node
   - Value: Select your Alexa account

2. **Danfoss Rooms**
   - Node: "Hent Danfoss Link Info fra Alexa"
   - Action: Add each room + select "All Properties"

3. **Sensor Names** (Optional)
   - Property: Each sensor's "Name" field
   - Current: "Danfoss_Stue", "Danfoss_Soveværelse", etc.
   - Change to match your room names

### Advanced Customization:

1. **Update Frequency**
   - Node: "Hvert 5 min"
   - Property: "Repeat" value (in seconds)
   - Default: 310 (5 min 10 sec)

2. **Room Count**
   - Add/duplicate sensor nodes
   - Update "Index data" function if needed
   - Update link routing

3. **Home Assistant Server**
   - All sensor nodes reference "Home Assistant" server
   - Requires HA addon: `node-red-contrib-home-assistant-websocket`

---

## 🐛 Troubleshooting Flow Issues

### Red "Account missing!" on Alexa node
→ Configure Alexa account (see Configuration Points)

### No messages in debug
→ Check "Hvert 5 min" inject node is enabled
→ Verify Alexa account authorization

### Temperature showing null/undefined
→ Check room name matches Alexa device exactly
→ Enable "find rum her" debug to see available rooms
→ Verify "All Properties" selected for room

### HA sensors not updating
→ Check "Home Assistant" server connection
→ Verify HA-WebSocket addon installed
→ See [TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md)

---

## 📝 Comments in Flow

The Node-RED flow includes comment nodes at key sections:

- **"Github"** - Main group label with documentation link
- **"Ved fejl..."** - Error reference link
- **"Forbind til Alexa..."** - Authentication section label
- **"*Tilføj dine rum her"** - Customization points marked with *

---

## Next Steps

1. **Import:** Copy `danfoss-link-integration.json` into Node-RED
2. **Configure:** Follow setup in [INSTALLATION.md](../docs/INSTALLATION.md)
3. **Debug:** Use debug nodes to monitor data flow
4. **Extend:** Add more rooms or modify logic as needed

---

**Last updated:** March 2026  
**Flow Version:** 1.2.0
