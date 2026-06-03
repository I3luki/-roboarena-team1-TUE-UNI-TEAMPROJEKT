---
title: Der dritte Sprint
date: 2026-04-20
---

1. Simon Schmauch:

Lebensleiste für Spieler:  
Ich habe eine Lebensleiste für den Spieler hinzugefügt, die mit Damage eines Gegners fällt und bei niedrigen Leben rot wird.  
Außerdem habe ich eine (noch nicht benutze) Staminaleiste hinzugefügt.  
<img width="400" height="411" alt="Player Healthbar" src="https://github.com/user-attachments/assets/8491ca32-8dbb-45c4-b94b-a0d9ad69726a" />  

Angriff für Spieler + Lebensleiste für Gegner:  
Ich habe für den Player einen periodischen Angriff hinzugefügt, der bisher ein Bereich um den Spieler herum ist und alle 1000ms einmal aktiviert wird.  
Wird ein (oder mehrere) Gegner getroffen, verliert er Leben. Das ist anhand der Lebensleiste des Gegners zu erkennen.  
Ich habe eine Liste implementiert, die alle lebenden Gegner speichert.  
In diese Liste können entweder neue Gegner hinzugefügt oder bestehende Gegner entfernt werden.
Nur Gegner in dieser Liste werden gezeichnet.
Wenn jetzt die Leben eines Gegners auf 0 HP droppen, wird er aus der Liste entfernt und somit verschwindet er aus der Arena.
<img width="400" height="411" alt="Player Attack" src="https://github.com/user-attachments/assets/741827fd-d485-46ba-beaa-f7fabd2394dc" />  

Veränderter Angriff + Gegnerbewegung:  
Wir haben uns dazu entschieden den Angriff des Spielers in einer Kegelform zu machen, damit man zielen muss, um Gegner zu treffen.
Gegner bewegen sich jetzt immer Richtung des Spielers und finden immer den besten Weg zum Spieler mithilfe eines "A*-Algorithmus".
Bisher wird der Pfad alle 0,5 Sekunden aktualisiert und die Pfade der einzelnen Gegner werden nicht gleichzeitig sondern durch Zufall verteilt berechnet, was den Rechenaufwand aufteilt.  
Problem: Bisher ist die Map aus 20x20 Blöcken aufgebaut. Je mehr Blöcke die Map eingeteilt ist, desto rechenintensiver ist der "A*-Algorithmus". Wenn wir also später 50+ Gegner gleichzeitig auf dem Feld haben wollen, wird das eventuell zu starken lags führen.  
Um das zu verbessern, müssen wir eventuell noch einmal die Map überarbeiten.  
<img width="400" height="331" alt="Enemy_Movement" src="https://github.com/user-attachments/assets/998a04cc-2555-4f0a-af79-b340f3fffc91" />



2. Noah
      1. Woche
         Level wurden hinzugefügt

         <img width="439" height="112" alt="Screenshot 2026-05-25 124349" src="https://github.com/user-attachments/assets/da92ebd1-0361-410d-9864-7849950a8522" />

      
      2. Woche
       

         Arena wurde überarbeitet:
  
         In 5 Teile Aufgeteilt (mehrere farbige Rechtecke)

         Labyrtinth 

          <img width="400" height="411" alt="Screenshot 2026-06-01 185024" src="https://github.com/user-attachments/assets/234665df-446d-49c5-aedb-2b0f45466ee5" />

            Wände wurden in großes Array hinzugefügt und ein paar tiles hinzugefügt

          Blitzarea

         <img width="400" height="411" alt="Screenshot 2026-06-01 185104" src="https://github.com/user-attachments/assets/7e2e15cf-c4f9-4e19-a67c-4d3f3bb7f1fa" />

         Tornado der von den wänden der arena wie ein Bildschirmschoner fliegt und Schaden macht.
         Blitze wurden eingfügt 4 an der Anzahl machen ebenfals schaden und spwanen random im               Bereich

   
         Rockarea   


         <img width="400" height="411" alt="Screenshot 2026-06-01 185135" src="https://github.com/user-attachments/assets/ac94fb44-1997-4307-8e9c-192e6b36c9c4" />


            Mit 3 schachbrett funktionen erstellt

          Wüste   

            <img width="400" height="411" alt="Screenshot 2026-06-01 185202" src="https://github.com/user-attachments/assets/7142a502-c561-450d-b8a4-59dc8df0f2e0" />


            Neue tiles Kaktus, schädel und Knochen wurden eingügt


         Enemy spwan auserhablb der Kamera dafür wurde erst der kamera spwan neu gestallet. Von
         von oben rechts direkt auf den player. Dann wurde mit schkleife geprüft ob der spwan in
         der kamera des players ist.
        
  
         Code smeels wurden aufgräumt redunadetre Code wurde gelöscht(ca 200 zeilen Code). Leider
         mussten fast alle Änderung aufgrund von Mergconfikte von denis gelöscht werden.
     
      
  3. Woche

        Level wurden überarbeitet, da eine Balckenfrom ansprechender ist und dieser wurden nach oben rechts verschoben.

      <img width="551" height="320" alt="Screenshot 2026-06-02 192145" src="https://github.com/user-attachments/assets/3e516b41-2448-4260-bb88-f05ba3315921" />



      Außerdem wurden bei einem level up die gameloop pausiert damit der player eine Auswahl möglichkeit bekommt von 2 zufälligen Buffs. 

      <img width="551" height="320" alt="Screenshot 2026-06-02 192412" src="https://github.com/user-attachments/assets/2f0b26b3-5942-4ec0-8a64-a33d4446081e" />

     
      Anknüpfend darauf wurden die angezigten Buffs implemtiert. Dazu zählen Healt buff, speed Buff, Attack speed, Attack damage und attack range.




     Insgesamt erfolgreicher Sprint ca 1000 neue Zeilen Code wurden Eingefügt von meiner Seite.
     
<br><br><br><br><br><br>
3. Joshua Supper
     Es wurden Stationäre Gegner erstmal hinzugefügt welche in einem kleinen umkreis dem Roboter dauerhaft schaden zufügen sollte            dieser sich diesen nähern. 
     Des weiteren wurde ein Game Over Screen hinzugefügt und verschieden Statstiken werden gespeichert und angezeigt. So kann nach dem       Tod auch eine neue Runde gestartet werden.
     
     <img width="659" height="508" alt="image" src="https://github.com/user-attachments/assets/4721024a-900a-4130-bad3-c71dfae3e17d" />
       
      Zusätlich kann die Klasse um einige dinge erweitert werden, wie z.B. getötete Monster oder andere Statistiken welche im laufe der       Entwicklung oder auch sonst für Interissant gehalten werden.

      Auch eine Möglichekeit ist das mit erreichten Punkten sich in Zukunft dauerhafte upgrades oder neue Waffen etc. erworben werden.        Diese würden den Spielfluss verändern und interessanter gestalten.




<br><br><br><br><br><br>
4. Dennis

**Scrolling Map**

Zu dem Zeitpunkt war die Map noch statisch und durch die Ränder des Screens begrenzt. Alles hing von der Screengröße ab. 
Dann wurde eine Arena größer als der Screen erstellt und die draw Funktionen wurden auf die globale Koordinaten abhängig vom Roboter angepasst. Um den Mittelpunkt des Screens, also die Kamera, dynamischer zu gestalten wurde ein Nachzieheffekt eingeführt.
Des Weiteren wurde eine Klasse für Wände und generelle Arenaobjekte eingeführt. 

davor:
<img width="250" height="250" alt="newfeature_orbs" src="https://github.com/user-attachments/assets/ff854d65-1dea-4e4f-879e-f1b80effdde6" />

danach:
<img width="250" height="250" alt="extendable-map" src="https://github.com/user-attachments/assets/6446596d-ebfe-4e36-b175-3d919f134365" />

<br><br>

**Tile-Effekte** 

Das Team hat sich Effektfelder auf dem Boden gewünscht. Diese lagen auch bisher auf dem Boden rum, aber eine Implementation für ihre Effekte gab es noch nicht. Diese wurden erstmals für ein Speedfeld und ein Heilfeld eingeführt.

<img width="400" height="400" alt="Effektfelder" src="https://github.com/user-attachments/assets/950feecb-af32-404a-bc3e-4b79279d4d31" />

