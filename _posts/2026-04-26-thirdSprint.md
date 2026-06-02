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
Gegner bewegen sich jetzt immer Richtung des Spielers und finden immer den besten Weg zum Spieler mithilfe eines A*-Algorithmus.
Bisher wird der Pfad alle 0,5 Sekunden aktualisiert und die Pfade der einzelnen Gegner werden nicht gleichzeitig sondern durch Zufall verteilt berechnet, was den Rechenaufwand aufteilt.  
Problem: Bisher ist die Map aus 20x20 Blöcken aufgebaut. Je mehr Blöcke die Map eingeteilt ist, desto rechenintensiver ist der A*-Algorithmus. Wenn wir also später 50+ Gegner gleichzeitig auf dem Feld haben wollen, wird das eventuell zu starken lags führen.  
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

          <img width="1506" height="1161" alt="Screenshot 2026-06-01 185024" src="https://github.com/user-attachments/assets/234665df-446d-49c5-aedb-2b0f45466ee5" />

            Wände wurden in großes Array hinzugefügt und ein paar tiles hinzugefügt

          Blitzarea

         <img width="1502" height="1155" alt="Screenshot 2026-06-01 185104" src="https://github.com/user-attachments/assets/7e2e15cf-c4f9-4e19-a67c-4d3f3bb7f1fa" />

         Tornado der von den wänden der arena wie ein Bildschirmschoner fliegt und Schaden macht.
         Blitze wurden eingfügt 4 an der Anzahl machen ebenfals schaden und spwanen random im               Bereich

   
         Rockarea   


         <img width="1498" height="1168" alt="Screenshot 2026-06-01 185135" src="https://github.com/user-attachments/assets/ac94fb44-1997-4307-8e9c-192e6b36c9c4" />


            Mit 3 schachbrett funktionen erstellt

          Wüste   

            <img width="1503" height="1171" alt="Screenshot 2026-06-01 185202" src="https://github.com/user-attachments/assets/7142a502-c561-450d-b8a4-59dc8df0f2e0" />


            Neue tiles Kaktus, schädel und Knochen wurden eingügt


         Enemy spwan auserhablb der Kamera dafür wurde erst der kamera spwan neu gestallet. Von
         von oben rechts direkt auf den player. Dann wurde mit schkleife geprüft ob der spwan in
         der kamera des players ist.
        
  
         Code smeels wurden aufgräumt redunadetre Code wurde gelöscht. Leider
         mussten fast alle änderung durch mergconfikte von denis gelöscht werden.
     
      
  3. Woche

        Level wurden überarbeitet

