# Fejlfinding Guide

Løsninger til almindelige problemer.

---

## 📋 Hurtige links

- [Node-RED problemer](#node-red-problemer)
- [Home Assistant problemer](#home-assistant-problemer)
- [Alexa problemer](#alexa-problemer)
- [Data flow problemer](#data-flow-problemer)
- [Generelle tips](#generelle-tips)

---

## Node-RED Problemer

### ❌ Røde noder eller fejl efter import

**Årsag:** Paletter ikke installeret eller dependencies mangler

**Løsning:**
1. Gå til Node-RED menu → **"Manage Palette"**
2. Geninstaller begge paletter:
   - `node-red-contrib-home-assistant-websocket`
   - `node-red-contrib-alexa-remote2-applestrudel`
3. Restart Node-RED helt (stop/start service)
4. Reload flow

> ⏱️ **Tider:** Restart kan tage 2-5 minutter

### ❌ "Account missing!" på Alexa node

**Årsag:** Alexa credentials ikke konfigureret

**Løsning:**
1. Dobbelt-klik på noden med fejlen
2. Under "Account" dropdown:
   - Hvis tom: klik "pencil" icon
   - Login med Alexa credentials
   - Acceptér permissions
3. Select account fra dropdown
4. Click Done
5. Deploy

### ❌ Noder vises ikke i venstre panel

**Årsag:** Paletter ikke fuldt installeret

**Løsning:**
1. Gå til "Manage Palette" → **Install**
2. Søg: `alexa-remote`
3. Find `node-red-contrib-alexa-remote2-applestrudel`
4. Klik **Install**
5. Vent til færdigt
6. Restart Node-RED browser (F5)

### ⚠️ Flow starter ikke / Messages kommer ikke

**Årsag:** Inject node disabled

**Løsning:**
1. Find **"Hvert 5 min"** inject node
2. Åbn den (dobbelt-klik)
3. Verificer **"Inject once at start?"** er checked: ☑️
4. Deploy igen

**Alternativ:**
1. Find **"Hvert 5 min"** noden
2. Klik på "edit" (pencil)
3. Klik "Inject" knapp i noden for manuel trigger
4. Se om debug messages kommer

---

## Home Assistant Problemer

### ❌ Sensorer vises ikke i HA

**Årsag 1:** Flow ikke deployed
- Check Node-RED er grønt deployed
- Se events i HA history

**Årsag 2:** Server integration ikke sat op
- Home Assistant websocket skal konfigureres i Node-RED
- Se [INSTALLATION.md](INSTALLATION.md#trin-2-node-red-setup)

**Løsning:**
1. I Node-RED, dobbelt-klik **"Rum1"** sensor node
2. Check "Server" er valgt
3. Hvis ikke → vælg fra dropdown
4. Deploy

### ⚠️ Sensorer er "unavailable" eller "unknown"

**Årsag:** Sensorer får ikke data fra flow

**Løsning:**
1. Open Node-RED debug panel
2. Find messages fra flow
3. Check payload indeholder data
4. Se [Data flow problemer](#data-flow-problemer)

### ❌ "long_lived_access_token required" fejl

**Årsag:** HA authentication token mangler eller udløbet

**Løsning:**
1. I Node-RED, gå til **"Manage Palette"** → **"Install"**
2. Geninstaller `node-red-contrib-home-assistant-websocket`
3. Gå til HA → **Settings** → **Security**
4. Generate new **"Long-Lived Access Token"**
5. I Node-RED, dobbelt-klik HA connection (f.eks. i sensor)
6. Paste nyt token
7. Deploy

---

## Alexa Problemer

### ❌ "Unauthorized" eller "Invalid request" fra Alexa

**Årsag 1:** Alexa credentials udløbet
- Amazon kræver periodisk re-auth

**Løsning:**
1. I Node-RED, find "Alexa-remote-init" node (gruppen øverst)
2. Dobbelt-klik "Ny forspørgelse" inject node
3. Klik "Inject" knap for at trigger ny auth
4. Vent 10 sekunder
5. Check debug messages

**Årsag 2:** Danfoss ikke længere forbundet til Alexa
- Check i Alexa app at Danfoss device stadig virker

**Løsning:**
1. Åbn Alexa app
2. Gå til Devices → Smart Home
3. Check status på Danfoss
4. Hvis "offline": re-enable skill og log ind igen
5. Se [SETUP_ALEXA.md](SETUP_ALEXA.md)

### ❌ Danfoss device ikke fundet i Alexa

**Årsag:** Device ikke aktiveret eller konfigureret forkert

**Løsning:**
1. I Node-RED, check debug messages fra Alexa node
2. Se hvad devices bliver returneret
3. I Alexa app, verify device vises
4. Hvis ikke: re-add Danfoss skill
5. Se [SETUP_ALEXA.md](SETUP_ALEXA.md#fejlfinding)

---

## Data Flow Problemer

### ❌ Ingen debug messages

**Årsag:** Flow ikke executing

**Løsning:**
1. Open Node-RED debug panel (højre side)
2. Find **"Hvert 5 min"** inject node
3. Klik på "Inject" triangle
4. Vent max 3 sekunder
5. Check om message kommer i debug panel

**Hvis stadig intet:**
1. Check all noder for rødt fejltegn
2. Se [Node-RED problemer](#node-red-problemer)

### ⚠️ Messages, men ingen temperature data

**Årsag:** Payload struktur forkert

**Løsning:**
1. I debug panel, ekspander messages
2. Find `payload.temperature.value`
3. Check værdien vises
4. Hvis ikke: Alexa returnerer ikke data
   - Se Alexa problems sektion
   - Re-auth Alexa

### ❌ Temperatura data kommer, men ikke i HA

**Årsag:** Sensor nodes ikke forbundet eller konfigureret forkert

**Løsning:**
1. I Node-RED, find "Rum1" sensor node
2. Dobbelt-klik for at åbne
3. Check:
   - [ ] "Server" er valgt (ikke "unselected")
   - [ ] "State" er: `payload.Rum1`
   - [ ] "Entity ID" har værdi
4. Click Done, Deploy
5. Wait 10 sec
6. Check HA entities

---

## Generelle tips

### 🔧 Debug Node-RED Flow

1. Tilføj debug nodes overalt:
   - Find interessant node
   - Forbind output til et debug node
   - Deploy
   - Kig på messages i debug panel

### 🔍 Check network forbindelse

Alexa API kræver internet:
```bash
# Linux/Mac
ping api.example.com

# Windows PowerShell
Test-Connection 8.8.8.8
```

### 📝 Save error logs

Hvis noget går galt:
1. Copy error text fra console
2. Se "Manage Palette" install log
3. Gem screenshot af error
4. Upload til GitHub issue

### ▶️ Restart alt systematisk

Hvis ingenting virker:
1. Restart Node-RED (stop/start service)
2. Refresh browser (F5)
3. Restart Home Assistant
4. Restart WiFi router
5. Check internet forbindelse

### 🆘 Hvis alt fejler

Som sidste udvej:
1. **Backup** current flow (Menu → Export)
2. **Delete** flow completely
3. **Restart** Node-RED
4. **Re-import** fresh from `flows/danfoss-link-integration.json`
5. **Reconfigure** Alexa account
6. Deploy

---

## Hvor får jeg hjælp?

- 📖 [GitHub Issues](https://github.com/michaelflarsen/danfosslink-in-HA/issues)
- 💬 [GitHub Discussions](https://github.com/michaelflarsen/danfosslink-in-HA/discussions)
- 🤖 [Node-RED Forum](https://discourse.nodered.org/)
- 🏠 [Home Assistant Community](https://community.home-assistant.io/)
- 📱 Alexa-remote2 [Documentation](https://github.com/Apollon77/node-red-contrib-alexa-remote2-applestrudel)

---

**Last updated:** May 2026
