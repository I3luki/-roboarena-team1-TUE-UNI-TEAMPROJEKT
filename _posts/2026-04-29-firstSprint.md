---
title: Sprint 1
date: 2026-04-29
---

1. Noah Utech:
   
Issue 1
Eine grundlegende Struktur wurde angelegt mit einem Fenster, Game-loop und Bildschrim-Updates
<img width="400" height="400" alt="Screenshot 2026-04-29 132510" src="https://github.com/user-attachments/assets/df940d1a-cdeb-48f3-9014-81e143f9b9f6" />

Issue 2
Die Key-Press wurden angelegt, sowie die gegensätzlichen Bewegungen definiert, damit die Schlange sich nur um eine 90 Grade Rotation bewegen kann.


2.
Simon Schmauch:

Um die Bewegungslogik in eine animierte Bewegung umzusetzen, wird immer ein neuer Kopf in die Richtung platziert, wo der Spieler mit den Pfeiltasten hin drückt.

Gleichzeitig wird das letzte Element der Schlange entfernt.

Somit bleibt die Anzahl der Schlangenelemente gleich und kann sich durch den Raum bewegen.

Dies bietet auch eine Grundlange zum Wachsen der Schlange:

Wenn die Schlange in einer Iteration des Spiels ein Apfel isst, wird das letzte Element nicht entfernt, wodurch die Schlange 1 Element mehr bekommt.

<img width="400" height="420" alt="SnakeMovement" src="https://github.com/user-attachments/assets/cb038061-af7c-49b0-84eb-8c15cc3b0fb5" />


3. Joshua Supper:
   
Die Schlange verschwindet nun nicht mehr wenn sie den Bildschirm verlässt sondern kommt auf der
anderen Seite wieder raus.

![img.png](img.png)



4.
   Dennis Andler: 

Bisher haben wir nur eine Schlange die sich bewegen lässt. Leider ist diese bisher auf strenger Diät. Um das zu fixen wurde ein Apfel(oder eher ein leckeres rotes Rechteck) eingefuegt.

Dieser Apfel kann von der Schlange gegessen werden indem der Schlangenkopf den Apfel berührt. Wird der Apfel gegessen so wird er an einer zufälligen Stelle des Bildschirms neu generiert. 

Damit der Apfel auch immer schön in der Mitte des Kopfes liegt, wird der Apfel immer in der Mitte möglicher Position des Schlangenviereckes generiert. (nur optisch, eigentlich liegt er genau auf der Ecke vom Schlangendreieck)

<img width="400" height="420" alt="SnakeWithApple" src="https://github.com/user-attachments/assets/2fc1df55-a740-4092-933b-37878e178eca" />


