# Avanceret Konfiguration

Guide til at tilpasse og udvide integrationen ud over standard setup.

---

## 📋 Indholdsfortegnelse

1. [Tilføj flere rum (8+)](#tilføj-flere-rum-8)
2. [Ændre update frekvens](#ændre-update-frekvens)
3. [Home Assistant automations](#home-assistant-automations)
4. [Grafana visualisering](#grafana-visualisering)
5. [Data storage & history](#data-storage--history)

---

## Tilføj flere rum (8+)

Default flow komit med 8 rum forudindstilled. Her er hvordan du tilføjer flere.

### 5.1 - Tilføj rum sensorer

1. I Node-RED, find gruppen **"Github"** (venstre side)
2. Find sidste "Rum" sensor (senest "Rum8")
3. Højreklik på en eksisterende "Rum" sensor
4. Vælg **"Duplicate"**
5. En ny sensor bliver oprettet (f.eks. "Rum8 copy")
6. Dobbelt-klik for at redigere:
   - Ændre navn til **"Rum9"**
   - Ændre State til: `payload.Rum9`
   - Ændre Entity ID hvis ønsket
   - Click Done
7. Gentag for hver ekstra rum

### 5.2 - Tilføj setpoint sensorer

1. Gentag samme process for **"Setpoint"** sensorer
2. Opret "Setpoint Rum9", "Setpoint Rum10", osv.
3. State skal være: `payload["Setpoint Rum9"]`

### 5.3 - Opdater Index-function

1. Find noden **"Index data"** (function node)
2. Dobbelt-klik for at åbne
3. I koden, find sektionen med `forEach`:

```javascript
danfoss_data.forEach(function (item, index) {
  data["Setpoint "+item.topic] = item.payload.targetSetpoint.value
});
```

> Denne del behøver IKKE at ændres! Den er dynamisk og håndterer alle rum

4. Click Done

### 5.4 - Deploy og test

1. Klik **"Deploy"**
2. Check debug panel for nye rum
3. Verificer i Home Assistant

---

## Ændre update frekvens

Default: **5 minutter** (begrænsning fra Alexa).

### Option 1: Hurtigere updates (hvis Alexa tilader)

1. Find noden **"Hvert 5 min"** (Inject node)
2. Dobbelt-klik for at åbne
3. Ændre **"Repeat"** værdien:
   - 310 = 5 min 10 sek (standard)
   - 180 = 3 minutter
   - 60 = 1 minut
   - 30 = 30 sekunder
4. Click Done
5. Deploy

> ⚠️ **Advarsel:** Alexa API har begrænsninger. For hyperige requests (< 2 min) risikerer du throttling

### Option 2: Leveragere cron-expression

I stedet for "Repeat" kan du bruge cron-syntaks:

1. I **"Hvert 5 min"** node:
2. Skift til **"Cron"** tab
3. Brug cron-expression, f.eks:
   - `0 */5 * * * *` = hvert 5. minut
   - `0 0 12 * * *` = kl 12:00 hver dag
   - `0 */30 * * * *` = hvert 30. minut

---

## Home Assistant Automations

Nu kan du lave automations baseret på Danfoss temperaturer!

### Eksempel 1: Notification når temperatur falder

**YAML for automation:**

```yaml
automation:
  - id: 'danfoss_temp_alert'
    alias: 'Danfoss - Temperatur alarm'
    trigger:
      platform: numeric_state
      entity_id: sensor.danfoss_stue
      below: 18
    action:
      service: notify.notify
      data:
        message: "Advarsel: Stuen er faldet til {{ states('sensor.danfoss_stue') }} grader"
```

### Eksempel 2: Tænd varme hvis temperatur stiger

```yaml
automation:
  - id: 'danfoss_temp_control'
    alias: 'Danfoss - Auto heating'
    trigger:
      platform: template
      value_template: "{{ (states('sensor.danfoss_stue') | float(default=0)) < 20 }}"
    action:
      service: climate.set_temperature
      target:
        entity_id: climate.danfoss_stue
      data:
        temperature: 22
```

### Eksempel 3: Debug sensor i HA

Opret en template sensor i HA for debug:

```yaml
template:
  - sensor:
      - name: "Danfoss Debug"
        unique_id: danfoss_debug
        state: "{{ state_attr('sensor.danfoss_stue', 'friendly_name') }}"
        attributes:
          current_temp: "{{ states('sensor.danfoss_stue') }}"
          setpoint: "{{ states('sensor.danfoss_setpoint_stue') }}"
```

---

## Grafana Visualisering

Grafana er bydes til at visualisere historiske temperaturdata.

### 6.1 - InfluxDB Setup (Data Storage)

1. I Home Assistant, installer InfluxDB addon/integration
2. Konfigurér til at gemme Danfoss sensorer:

```yaml
influxdb:
  host: localhost
  port: 8086
  database: homeassistant
  include:
    entities:
      - sensor.danfoss_stue
      - sensor.danfoss_soveværelse
      - sensor.danfoss_setpoint_stue
```

3. Genstart Home Assistant

### 6.2 - Grafana Data Source

1. I Grafana, gå til **Configuration → Data Sources**
2. Klik **"Add Data Source"**
3. Vælg **"InfluxDB"**
4. Konfiguration:
   - URL: `http://homeassistant:8086` (eller intern HA IP)
   - Database: `homeassistant`
   - Username: `homeassistant`
   - Password: [dine HA credentials]
5. Click **"Save & Test"**

### 6.3 - Gør dashboard

1. I Grafana, gå til **Create → Dashboard**
2. Klik **"Add Panel"**
3. I Query editor:
   - Database: `homeassistant`
   - Measurement: `entities` (eller `°C`)
   - Select: `value`
   - Where: `tags.entity_id = 'sensor.danfoss_stue'`
4. Vis derefter graph
5. Gem dashboard

---

## Data Storage & History

### Onde: Gem kun vigtigt data

Home Assistant gemmer alt historik per standard. For kun at gemme Danfoss:

**configuration.yaml:**
```yaml
recorder:
  purge_keep_days: 90
  include:
    entities:
      - sensor.danfoss_stue
      - sensor.danfoss_soveværelse
      - sensor.danfoss_setpoint_stue
```

### Tonn: Arkivér til TimescaleDB

For større deployments, brug TimescaleDB:

```yaml
timescaledb:
  host: localhost
  port: 5432
  database: timescale_homeassistant
  username: homeassistant
```

---

## Avanceret: Node-RED Customization

### Tilføj fejlhåndtering

I flowet kan du tilføje error nodes:

1. Find en sensor node
2. Fra output, forbind til en "Catch" node
3. Output fra Catch til en debug node
4. Deploy

Dette hjælper med at se hvis data ikke kommer

### Monitor flow performance

Åbn **"Debug messages"** panel og monitor:
- Antal messages pr. update
- Timestamp for hver message
- Fejlmeldinger

---

## Praktiske eksempler

### Mål 1: Lagre temperatur hver time

```yaml
# Node-RED function node
let current_hour = new Date().getHours();
if (current_hour !== msg.last_hour) {
  msg.last_hour = current_hour;
  return msg; // Send videre
} else {
  return null; // Skip
}
```

### Mål 2: Smoothe spiky data

```javascript
// Add rolling average
let temps = flow.get("temp_history") || [];
temps.push(msg.payload.temperature);
if (temps.length > 5) temps.shift();
flow.set("temp_history", temps);

let average = temps.reduce((a,b) => a+b) / temps.length;
msg.payload = average;
return msg;
```

---

## Næste Trin

- 📖 Se [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for hjælp
- 🔧 Se [INSTALLATION.md](INSTALLATION.md) for basics
- 📚 Se Node-RED docs: https://nodered.org/docs/

---

**Last updated:** March 2026
