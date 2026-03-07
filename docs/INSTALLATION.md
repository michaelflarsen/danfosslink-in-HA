# Installationsvejledning - Danfoss Link CC in Home Assistant

Denne vejledning tager dig gennem alle trin helt fra start til slut.

---

## 📋 Tabel over indhold

1. [Forudsætninger](#forudsætninger)
2. [Trin 1: Alexa Integration](#trin-1-alexa-integration)
3. [Trin 2: Node-RED Setup](#trin-2-node-red-setup)
4. [Trin 3: Flow Import](#trin-3-flow-import)
5. [Trin 4: Konfiguration](#trin-4-konfiguration)
6. [Trin 5: Testing](#trin-5-testing)
7. [Fejlfinding](#fejlfinding)

---

## Forudsætninger

Oversigt over hvad du skal have:

### Obligatorisk
- ✅ **Danfoss Link CC** - dit varmestyringssystem
- ✅ **Amazon Alexa konto** - bare app, ingen device nødvendig
- ✅ **Home Assistant** - installeret og kørende
- ✅ **Node-RED** - som HA addon eller standalone server
- ✅ **Internet forbindelse** - på både HA og Node-RED

### Anbefalede
- 📱 Danfoss Link app - på din telefon
- 🖥️ Node-RED GUI adgang - normalt `http://nodehost:1880`
- 📝 Administrator adgang - til Home Assistant

---

## Trin 1: Alexa Integration

### 1.1 - Danfoss Link i Alexa

1. Download Amazon Alexa app på din telefon eller computer
2. Log ind med din Amazon konto
3. Åbn **"Devices"** (eller **"Enheder"**)
4. Tap **„+"** knappen for at tilføje en ny enhed
5. Søg efter **"Danfoss Link"** app (eller skill)
6. Følg instruktionerne til at koppel din Danfoss Link CC
   - Du skal bruge dine Danfoss Link login credentials

> 💡 **Tip:** Du behøver IKKE en fysisk Alexa enhed (Echo, Dot osv.), appen er nok!

### 1.2 - Verificer forbindelsen

I Alexa app:
1. Gå til **"Devices"** → **"Smart Home"**
2. Du skal se dine temperaturzoner/rum fra Danfoss
3. Prøv at justera temperatur i Alexa for at verificere

> ⚠️ **Vigtigt:** Hvis dine rum ikke vises, checker du login eller enhed status i Danfoss app

📖 **Se også:** [SETUP_ALEXA.md](SETUP_ALEXA.md) for detaljeret vejledning

---

## Trin 2: Node-RED Setup

### 2.1 - Find Node-RED

Åbn Node-RED i din browser:
- Hvis HA addon: `http://<ha-ip>:1880`
- Hvis standalone: `http://<node-red-ip>:1880`

### 2.2 - Installer Paletter

1. Klik på **☰ menu** (øverst til højre)
2. Vælg **"Manage Palette"** (eller **"Manage Palletes"**)
3. Gå til **"Install"** tab
4. Søg efter første palette: **`node-red-contrib-home-assistant-websocket`**
   - Klik **"Install"** når du finder det
   - Vent til det er installeret
5. Søg efter anden palette: **`node-red-contrib-alexa-remote2-applestrudel`**
   - Klik **"Install"** når du finder det
   - Vent til det er installeret
6. Luk Palette manager

> ⏱️ **Tider:** Installation kan tage 1-5 minutter pr. palette

> ✅ **Verificering:** Efter restart af Node-RED skal du se nye noder i panelet til venstre

### 2.3 - Verificer Paletter

Efter Node-RED restart:
1. Søg i venstre panel for **"alexa-remote"** noder
2. Søg i venstre panel for **"ha-"** noder

Hvis de er der = ✅ installation lykkedes!

---

## Trin 3: Flow Import

### 3.1 - Forbered Flow-fil

1. Find filen `flows/danfoss-link-integration.json` i projektet
2. Åbn den i en teksteditor
3. Kopier alt indholdet (Ctrl+A, Ctrl+C)

### 3.2 - Importer i Node-RED

1. Gå til Node-RED GUI
2. Klik **☰ menu** → **"Import"**
3. Vælg **"Clipboard"** eller paste direkte (Ctrl+V)
4. Kly **"Import"** knappen
5. Flowet skal nu vises på canvas'et

### 3.3 - Deploy

1. Klik den røde **"Deploy"** knap øverst til højre
2. Vent til den bliver grøn med teksten "Deploy done"

> ✅ Hvis du ser grønne noder = deployment lykkedes!

> ❌ Hvis du ser røde noder = check fejlfinding sektion

---

## Trin 4: Konfiguration

### 4.1 - Opsæt Alexa account

1. Find noden med teksten **"Account missing!"** (rødt felt)
2. Dobbelt-klik på den
3. I dropdown "Account" - vælg din Alexa account (eller opret ny)
4. Click **"Done"**
5. Deploy igen

### 4.2 - Tilføj og konfigurér dine rum

1. Find noden **"Hent Danfoss Link Info fra Alexa"**
2. Dobbelt-klik for at åbne
3. Under "Devices" del - find **"Add"** og klik "+"
4. En dropdown skal vise dine Danfoss rum
5. For HVERT rum:
   - Vælg det fra dropdown
   - Sæt "Properity" til **"All Properties"**
   - Klik "Add"
6. Click **"Done"**

> 💡 **Tip:** Hvis rummet ikke vises - gå tilbage til Alexa app og verificer enhedens status

### 4.3 - Tilpas sensor navne

1. Tab højre side af flowet - du ser 8 "Rum" noder
2. For hver sensør du skal bruge:
   - Dobbelt-klik noden (f.eks. "Rum1")
   - Ret "Name" til f.eks. "Stue" (dit rum navn)
   - Ret "Entity Id" hvis nødvendig
   - Click **"Done"**
3. Repeat for alle rum du bruger
4. Deploy igen

---

## Trin 5: Testing

### 5.1 - Check flow execution

1. Åbn debug panel (højre side, "Debug messages" tab)
2. Klik på **"Start and Repetition"** noden
3. Du burde se messages i debug panelet
4. Hvis OK, flowet sender data til HA 🎉

### 5.2 - Verificer i Home Assistant

1. Gå til Home Assistant UI
2. Gå til **"Developer Tools"** → **"States"**
3. Søg efter sensor navne fra dit flow (f.eks. `sensor.danfoss_stue`)
4. Du skal se temperaturer og setpoints

### 5.3 - Check update timing

1. Note tidspunktet på først update
2. Vent 5 minutter
3. Check igen - data skal være opdateret

> ✅ Hvis alt virker = Installation komplet!

---

## Fejlfinding

Se [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for:
- Røde noder i Node-RED
- Ingen data i Home Assistant
- Alexa connection fejl
- Mange andre problemer

**Hurtige checks:**
- ❌ Røde forspørgsningstegn? → Reinstalér paletter
- ❌ Ingen data? → Check Alexa credentials
- ❌ Timeout fejl? → Tjek netværk forbindelse

---

## Næste trin

Nu har du en fungerende integration! 🎉

### Hvad nu?

1. **Lav automationer** - Se [CONFIGURATION.md](CONFIGURATION.md)
2. **Sæt Grafana op** - Se [CONFIGURATION.md](CONFIGURATION.md#grafana-setup)
3. **Tilføj flere rum** - Se [CONFIGURATION.md](CONFIGURATION.md#tilføj-flere-rum)
4. **Læs troubleshooting** - Se [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Got help from:** Michael F. Larsen  
**Last updated:** March 2026
