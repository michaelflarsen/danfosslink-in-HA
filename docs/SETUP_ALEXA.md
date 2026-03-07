# Alexa Opsætningsvejledning

Guide til at tilslutte Danfoss Link CC til Amazon Alexa.

---

## 📋 Indholdsfortegnelse

1. [Krav](#krav)
2. [Trin 1: Alexa App](#trin-1-alexa-app-download)
3. [Trin 2: Tilslut Danfoss](#trin-2-tilslut-danfoss-link-cc)
4. [Trin 3: Verifikation](#trin-3-verifikation-af-forbindelse)
5. [Fejlfinding](#fejlfinding)

---

## Krav

- 📱 Smartphone eller computer
- 🔍 Amazon konto (kan være den samme som for andre Amazon services)
- 🔗 Danfoss Link CC i netværket
- 📝 Dit Danfoss Link Login (brugernavn + adgangskode)

---

## Trin 1: Alexa App Download

### For iPhone/iPad
1. Åbn **App Store**
2. Søg efter **"Amazon Alexa"**
3. Klik **"Get"** → **"Install"**
4. Vent på download og installation
5. Åbn appen

### For Android
1. Åbn **Google Play Store**
2. Søg efter **"Amazon Alexa"**
3. Klik **"Install"**
4. Vent på installation
5. Åbn appen

### For Web (Desktop)
1. Gå til https://alexa.amazon.com
2. Log ind med Amazon konto
3. Du har nu web versionen klar

---

## Trin 2: Tilslut Danfoss Link CC

### 2.1 - Find Danfoss Skill

1. I Alexa appen, gå til **"More"** (eller **"Mere"**) menuen
2. Vælg **"Skills & Games"**
3. Søg efter **"Danfoss"**
4. Find og vælg **"Danfoss Link CC"** (eller blot **"Danfoss Link"**)
5. Tap på det

> 💡 **Note:** Det kan også være under "Home & Garden" kategorien

### 2.2 - Autoriser Danfoss Account

1. Klik **"Enable"** eller **"Enable to Use"**
2. Appen åbner Danfoss login side
3. Log ind med dine **Danfoss Link credentials**:
   - Brugernavn (email eller brugernavn)
   - Adgangskode
4. Acceptér permissions når spurgt
5. Autoriseringen burde være gennemført

### 2.3 - Tillad Alexa Adgang

1. Tilbage i Alexa app, acceptér evenuelle permissions
2. Appen burde sige "_Danfoss Link CC has been successfully linked_"

---

## Trin 3: Verifikation af Forbindelse

### 3.1 - Find dine Danfoss Devices

1. I Alexa appen, gå til **"Devices"** (eller **"Enheder"**)
2. Tryk på **"Smart Home"** tab (hvis der er flere tabs)
3. Du burde nu se alle dine Danfoss rum/zoner

Eksempel:
```
Danfoss Link CC
├─ Living Room
├─ Bedroom
├─ Kitchen
└─ ...
```

### 3.2 - Test Temperatur Read

1. Klik på en af dine Danfoss rum
2. Du burde se:
   - 🌡️ Aktuel temperatur
   - 🎯 Ønsket setpoint
   - 📊 Andre properties

### 3.3 - Test Temperatur Write (Valgfrit)

1. I Alexa app, find en af dine rum
2. Prøv at ændre setpoint/temperatur
3. Hvis det virker, ændring skulle reflekteres i Danfoss Link app efter nogle sekunder

✅ Hvis alt virker = Alexa integration OK!

---

## Fejlfinding

### Danfoss Link vises ikke i Skills?

**Løsning 1:** Søg efter andre varianter
- "Danfoss"
- "Danfoss Link"
- "Link CC"

**Løsning 2:** Tjek Danfoss kompatibilitet
- Gå til https://www.danfoss.dk
- Søg efter "Alexa integration" eller "Smart Home"
- Verificer at din model understøttes

**Løsning 3:** Opdater Alexa
- I apper, check for iPhone/Android updates
- Opdater til seneste version

### Login fejl under Danfoss autorisation?

**Løsning 1:** Prøv igen med rigtigt password
- Sørg for at CAPS LOCK er fra
- Husk mellemrum hvis der er nogle
- Prøv copy/paste fra noter

**Løsning 2:** Reset loginoplysninger
- Gå til danfoss.dk
- Brug "Forgot Password" til at reset
- Vent 5 minutter
- Prøv Alexa integration igen

**Løsning 3:** Disable og re-enable skill
- I Alexa appen, find Danfoss skill
- Tap "Disable"  
- Vent 10 sekunder
- Tap "Enable" igen
- Log ind igen

### Rum/Devices vises ikke i Alexa?

**Løsning 1:** Opdater dine Danfoss devices
- I Danfoss Link app
- Check at alle rum/zoner er aktiveret
- Se at de ikke er offline

**Løsning 2:** Genstart Danfoss forbindelse
- I Alexa app
- Find Danfoss skill i "Skills"
- Vælg "Disable"
- Vent 30 sekunder
- Vælg "Enable"
- Vent 5 minutter for sync

**Løsning 3:** Genstart Alexa app
- Force close Alexa app
- Vent 10 sekunder
- Åbn igen
- Gå til Devices

### Alternativ: PDF Vejledning

Der er også en PDF vejledning til rådighed:
📄 Se [danfossAlexaSetup.pdf](danfossAlexaSetup.pdf)

---

## Næste Trin

Når Alexa integration virker:
1. Gå tilbage til [INSTALLATION.md](INSTALLATION.md#trin-2-node-red-setup)
2. Fortsæt med Node-RED setup
3. Importer flow filen

---

**Last updated:** March 2026
