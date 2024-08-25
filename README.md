# Danfoss Link CC In HomeAssistant <br>
<img src="https://github.com/michaelflarsen/danfosslink-in-HA/blob/main/danfosslink.JPG" alt="Controller" width="500">
Følg disse trin hvis du vil have dit gamle Danfoss Link CC system ind i Home Assistant, med mulighed for at se & styre temperatur via automatiseringer og evt se statiktik i Grafana!<br>
<img src="https://github.com/michaelflarsen/danfosslink-in-HA/blob/main/grafanaTemp.JPG" alt="Grafana" width="400">
<img src="https://github.com/michaelflarsen/danfosslink-in-HA/blob/main/haKlima.JPG" alt="Grafana" width="300">
<br>
<i>Vi trækker info fra Danfoss Link igennem Alexa og til Node-Red, mange trin, mange fejl muligheder!!</i>
<br><br>

1. Tilføj din Danfoss Link CC til Alexa Appen, <i>kræver ingen Alexa Enheder!</i>
    <br>Hjælp: <a href="https://github.com/michaelflarsen/danfosslink-in-HA/blob/main/danfossAlexaSetup.pdf">Her</a> 

2. Din <b>Node-Red</b> installation skal indholde disse 2 paletter (alt+shift+p).
    <br> node-red-contrib-home-assistant-websocket <a href="https://flows.nodered.org/node/node-red-contrib-home-assistant-websocket">Her fra</a>
    <br> node-red-contrib-alexa-remote2-applestrudel <a href="https://flows.nodered.org/node/node-red-contrib-alexa-remote2-applestrudel">Her fra</a>
   
3. Impoter flow fra denne fil: <a href="https://github.com/michaelflarsen/danfosslink-in-HA/blob/main/Node-Red%20Flow">Her fra</a><br>
    Tilføj det i din Node-Red installation
   
5. Opsæt din Alexa web server under en enhed der har "Account missing!", den skal have din Node-Red's IP, og port 3456! <a href="https://raw.githubusercontent.com/michaelflarsen/danfosslink-in-HA/main/alexaServerIp.JPG">eksempel</a>

6. Deploy dit flow og opsæt Noden "Hent Danfoss Link Info fra Alexa" med dine rum, de skulle gerne være en mulighed fra dropdown menuen ved at trykke på "+ add", tilføj alle dine rum og sæt den til "All Properties"<br>
    Tilføj dem her: <a href="https://raw.githubusercontent.com/michaelflarsen/danfosslink-in-HA/main/haFejlVedHentInfo2.JPG">Opsæt Rum</a>

8. Gå gennem flowet og ændre så den får dine Rum og Områder korrekt ind, kig efter * makering<br>
    Find dine rum her: <a href="https://raw.githubusercontent.com/michaelflarsen/danfosslink-in-HA/main/findRum.JPG">Find Rum</a><br>

