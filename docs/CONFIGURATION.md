# Avanceret Konfiguration

Guide til at tilpasse og udvide integrationen ud over standard setup.

---

## 📋 Indholdsfortegnelse

1. [Tilføj flere rum (8+)](#tilføj-flere-rum-8)
2. [Ændre update frekvens](#ændre-update-frekvens)
3. [Setpoint Styring – Skriv temperatur til Danfoss](#setpoint-styring--skriv-temperatur-til-danfoss)
4. [Home Assistant automations](#home-assistant-automations)
5. [Grafana visualisering](#grafana-visualisering)
6. [Data storage & history](#data-storage--history)

---

## Tilføj flere rum (8+)

Default flow kommer med 8 rum forudindstillet. Her er hvordan du tilføjer flere.

### 1.1 - Tilføj rum sensorer

1. I Node-RED, find gruppen **"Github"** (venstre side)
2. Find sidste "Rum" sensor (senest "Rum8")
3. Højreklik på en eksisterende "Rum" sensor
4. Vælg **"Duplicate"**
5. En ny sensor bliver oprettet (f.eks. "Rum8 copy")
6. Dobbelt-klik for at redigere:
   - Ændre navn til **"Rum9"**
   - Ændre State til: `payload.Rum9`
   - Ændre Entity ID hvis ønsket
   - Klik Done
7. Gentag for hver ekstra rum

### 1.2 - Tilføj setpoint sensorer

1. Gentag samme process for **"Setpoint"** sensorer
2. Opret "Setpoint Rum9", "Setpoint Rum10", osv.
3. State skal være: `payload["Setpoint Rum9"]`

### 1.3 - Opdater Index-function

1. Find noden **"Index data"** (function node)
2. Dobbelt-klik for at åbne
3. I koden, find sektionen med `forEach`:

```javascript
danfoss_data.forEach(function (item, index) {
  data["Setpoint "+item.topic] = item.payload.targetSetpoint.value
});
```

> Denne del behøver IKKE at ændres! Den er dynamisk og håndterer alle rum automatisk.

4. Klik Done

### 1.4 - Deploy og test

1. Klik **"Deploy"**
2. Check debug panel for nye rum
3. Verificer i Home Assistant

---

## Ændre update frekvens

Default: **5 minutter** (begrænsning fra Alexa).

### Option 1: Hurtigere updates (hvis Alexa tillader)

1. Find noden **"Hvert 5 min"** (Inject node)
2. Dobbelt-klik for at åbne
3. Ændre **"Repeat"** værdien:
   - 310 = 5 min 10 sek (standard)
   - 180 = 3 minutter
   - 60 = 1 minut
4. Klik Done
5. Deploy

> ⚠️ **Advarsel:** Alexa API har begrænsninger. For hyppige requests (< 2 min) risikerer du throttling.

### Option 2: Brug cron-expression

I stedet for "Repeat" kan du bruge cron-syntaks:

1. I **"Hvert 5 min"** noden, skift til **"Cron"** tab
2. Brug cron-expression, f.eks.:
   - `0 */5 * * * *` = hvert 5. minut
   - `0 0 12 * * *` = kl 12:00 hver dag
   - `0 */30 * * * *` = hvert 30. minut

---

## Setpoint Styring – Skriv temperatur til Danfoss

> ℹ️ **Ofte stillet spørgsmål:** Mange spørger hvordan man skriver setpoints tilbage til Danfoss og om man kan få climate-entiteter. Her er svaret!

Danfoss setpoints kan styres via Alexa API'et. Node-RED sender kommandoen til Alexa, som videredelegerer til Danfoss Link CC.

### Overblik over datavej for setpoint

```
Home Assistant (input_number) → Node-RED → Alexa → Danfoss Link CC
```

---

### Metode 1: input_number + Node-RED (anbefalet)

Opret `input_number`-hjælpere i HA som fungerer som skrivbare setpoints. Node-RED lytter til ændringer og sender dem til Alexa.

#### Trin 1 – Opret input_number hjælpere i HA

Tilføj dette til `configuration.yaml` (tilpas rum-navne):

```yaml
input_number:
  danfoss_setpoint_stue:
    name: "Stue – Ønsket temperatur"
    min: 5
    max: 30
    step: 0.5
    unit_of_measurement: "°C"
    icon: mdi:thermometer
  danfoss_setpoint_sovevaerelse:
    name: "Soveværelse – Ønsket temperatur"
    min: 5
    max: 30
    step: 0.5
    unit_of_measurement: "°C"
    icon: mdi:thermometer
  # Tilføj flere rum som ønsket...
```

Genstart Home Assistant efter ændringen.

#### Trin 2 – Importer setpoint-flow i Node-RED

Importer filen [flows/danfoss-setpoint-control.json](../flows/danfoss-setpoint-control.json) i Node-RED (samme fremgangsmåde som hoved-flowet).

#### Trin 3 – Konfigurér rum i flowet

For hvert rum i flowet:
1. Find noden **"* Sæt Setpoint – Rum1"** (alexa-remote-smarthome)
2. Dobbelt-klik for at åbne
3. Under **"Devices"** – vælg dit Danfoss-rum fra dropdown
4. Sæt **"Action"** til `setTargetTemperature`
5. Klik Done → Deploy

> 💡 **Tip:** Rummets navn i Alexa skal matche præcis. Find det i Alexa-appen under Devices → Smart Home.

#### Trin 4 – Test setpoint

1. Gå til HA → Developer Tools → States
2. Find `input_number.danfoss_setpoint_stue`
3. Ændre værdien manuelt
4. Verificer i Alexa-appen at setpoint er opdateret
5. Verificer i Danfoss Link-appen efter ~30 sekunder

---

### Metode 2: Template Climate Entity i HA (avanceret)

Med en `template` climate entity får du et rigtigt termostat-kort i HA's dashboard med både aktuel temperatur og setpoint-kontrol.

#### Trin 1 – Forudsætninger

- Metode 1 skal være sat op og virke
- HA 2023.4 eller nyere

#### Trin 2 – Opret template climate entity

Tilføj til `configuration.yaml`:

```yaml
climate:
  - platform: generic_thermostat
    name: "Stue"
    unique_id: danfoss_climate_stue
    heater: input_boolean.danfoss_stue_dummy
    target_sensor: sensor.danfoss_stue
    min_temp: 5
    max_temp: 30
    target_temp_step: 0.5
    cold_tolerance: 0.1
    hot_tolerance: 0.1
    initial_hvac_mode: "heat"
```

> ⚠️ `generic_thermostat` kræver en `heater`-entitet. Opret en `input_boolean.danfoss_stue_dummy` som dummy – den bruges ikke reelt, men er påkrævet af platformen.

#### Trin 3 – Kobl climate entity til Danfoss via automation

Når climate-entiteten ændres, sender en automation den nye temperatur til `input_number`, som Node-RED håndterer:

```yaml
automation:
  - id: 'danfoss_climate_to_nodered'
    alias: 'Danfoss – Climate setpoint → Node-RED'
    trigger:
      platform: state
      entity_id: climate.stue
      attribute: temperature
    action:
      service: input_number.set_value
      target:
        entity_id: input_number.danfoss_setpoint_stue
      data:
        value: "{{ state_attr('climate.stue', 'temperature') }}"
```

#### Resultat

Du får et fuldt termostat-kort i HA:

```
┌─────────────────────────┐
│  🌡️ Stue                │
│  Aktuel: 21.5°C         │
│  Setpoint: [──●──] 22°C │
└─────────────────────────┘
```

---

## Home Assistant Automations

Nu kan du lave automations baseret på Danfoss temperaturer!

### Eksempel 1: Notification når temperatur falder

```yaml
automation:
  - id: 'danfoss_temp_alert'
    alias: 'Danfoss - Temperatur alarm'
    trigger:
      platform: numeric_state
      entity_id: sensor.danfoss_stue
      below: 18
      for:
        minutes: 5
    action:
      service: notify.notify
      data:
        message: "Advarsel: Stuen er faldet til {{ states('sensor.danfoss_stue') }} grader"
```

### Eksempel 2: Daglig temperaturrapport

```yaml
automation:
  - id: 'danfoss_daily_report'
    alias: 'Danfoss - Daglig rapport'
    trigger:
      platform: time
      at: '08:00:00'
    action:
      service: notify.notify
      data:
        title: "📊 Daglig temperaturrapport"
        message: |
          Stue: {{ states('sensor.danfoss_stue') }}°C (setpoint: {{ states('sensor.danfoss_setpoint_stue') }}°C)
          Soveværelse: {{ states('sensor.danfoss_sovevaerelse') }}°C
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

Grafana er oplagt til at visualisere historiske temperaturdata.

### 5.1 - InfluxDB Setup (Data Storage)

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
      - sensor.danfoss_sovevaerelse
      - sensor.danfoss_setpoint_stue
```

> ℹ️ **InfluxDB v2:** Brug `api_version: 2` og `token:` i stedet for `username`/`password` ved InfluxDB v2+.

3. Genstart Home Assistant

### 5.2 - Grafana Data Source

1. I Grafana, gå til **Configuration → Data Sources**
2. Klik **"Add Data Source"**
3. Vælg **"InfluxDB"**
4. Konfiguration:
   - URL: `http://homeassistant:8086` (eller intern HA IP)
   - Database: `homeassistant`
   - Credentials: dine InfluxDB credentials (ikke HA-credentials)
5. Klik **"Save & Test"**

### 5.3 - Gør dashboard

1. I Grafana, gå til **Create → Dashboard**
2. Klik **"Add Panel"**
3. I Query editor:
   - Database: `homeassistant`
   - Measurement: `°C`
   - Select: `value`
   - Where: `entity_id = 'sensor.danfoss_stue'`
4. Vis som graph
5. Gem dashboard

---

## Data Storage & History

### 💡 Anbefaling: Gem kun vigtigt data

Home Assistant gemmer alt historik som standard. For kun at gemme Danfoss-data:

**configuration.yaml:**
```yaml
recorder:
  purge_keep_days: 90
  include:
    entities:
      - sensor.danfoss_stue
      - sensor.danfoss_sovevaerelse
      - sensor.danfoss_setpoint_stue
```

### ⚙️ Avanceret: Arkivér til TimescaleDB

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

Dette hjælper med at se hvis data ikke kommer.

### Monitor flow performance

Åbn **"Debug messages"** panel og monitor:
- Antal messages pr. update
- Timestamp for hver message
- Fejlmeldinger

---

## Praktiske eksempler

### Lagre temperatur hver time

```javascript
// Node-RED function node
let current_hour = new Date().getHours();
if (current_hour !== msg.last_hour) {
  msg.last_hour = current_hour;
  return msg;
} else {
  return null;
}
```

### Smoothe spiky data

```javascript
// Rolling average over 5 målinger
let temps = flow.get("temp_history") || [];
temps.push(parseFloat(msg.payload));
if (temps.length > 5) temps.shift();
flow.set("temp_history", temps);

msg.payload = temps.reduce((a, b) => a + b) / temps.length;
return msg;
```

---

## Næste Trin

- 📖 Se [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for hjælp
- 🔧 Se [INSTALLATION.md](INSTALLATION.md) for basics
- 📚 Se Node-RED docs: https://nodered.org/docs/

---

**Last updated:** May 2026
