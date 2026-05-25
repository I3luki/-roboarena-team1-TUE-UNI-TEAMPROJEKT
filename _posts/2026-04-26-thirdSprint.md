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
