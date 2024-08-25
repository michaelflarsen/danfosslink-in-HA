# Danfoss Link CC In HomeAssistant <br>
<img src="https://github.com/michaelflarsen/danfosslink-in-HA/blob/main/danfosslink.JPG" alt="Controller" width="500">
Følg disse trin hvis du vil have dit gamle Danfoss Link CC system ind i Home Assistant, med mulighed for at se & styre temperature via automatiseringer og evt se statiktik i Grafana!<br>
<img src="https://github.com/michaelflarsen/danfosslink-in-HA/blob/main/grafanaTemp.JPG" alt="Grafana" width="300">
<img src="https://github.com/michaelflarsen/danfosslink-in-HA/blob/main/haKlima.JPG" alt="Grafana" width="250">
<br>
<i>Note: Vi trækker info fra Danfoss Link igennem Alexa og vidrer til Node-Red, mange trin, mange fejl muligheder!</i>
<br><br>

1. Tilføj din Danfoss Link til Alexa, <i>kræver ingen Alexa Enheder!</i>
    <br>Hjælp: <a href="https://github.com/michaelflarsen/danfosslink-in-HA/blob/main/danfossAlexaSetup.pdf">Her</a> 

2. Din <b>Node-Red</b> installation skal indholde disse 2 paletter (alt+shift+p) ellers får du fejl.
    <br> node-red-contrib-home-assistant-websocket 
    <br> node-red-contrib-alexa-remote2-applestrudel
   
3. Impoter flow fra denne fil: <a href="https://github.com/michaelflarsen/danfosslink-in-HA/blob/main/Node-Red%20Flow">Her fra</a><br>
    Tilføj det i din Node-Red installation

4. Opsæt din Alexa web server under en enhed der har "Account missing!", den skal have din Node-Red's IP, og port 3456! <a href="https://raw.githubusercontent.com/michaelflarsen/danfosslink-in-HA/main/alexaServerIp.JPG">eksempel</a>
6. Gå gennem flowet og ændre så den får dine Rum og Områder korrekt ind, kig efter * makering


