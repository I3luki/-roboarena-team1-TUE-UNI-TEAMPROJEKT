---
title: Sprint 2
date: 2026-05-06
---

1. Simon Schmauch:  
Zuerst wurde ein Game Window erstellt mit Größe 1000x1000  
Danach wurde eine Arena aus verschiedenen 50x50 Blöcken gebaut.  
- Dunkelgrauer Block: Arenabegrenzung
- Blauer Block: Interne Arenawand
- Roter Block: Gegnerspawnfeld
- Grüner Block: Heilungsfeld
- Gelber Block: Powerupfeld
<img width="500" height="512" alt="arena (1) (2)" src="https://github.com/user-attachments/assets/87624e69-65a6-4424-9c54-0ff5736b58d5" />
<br>
Spielidee:
<img width="776" height="561" alt="589690260-a195a0f5-f39d-4433-b062-2045772dd2b5 (2)" src="https://github.com/user-attachments/assets/abd731b4-1109-4986-b090-47d001651d2b" />

<br>
Basisspiel Ideen:
<br>

Unsere Spielidee soll ein Roguelike werden und ist inspiriert von Spielen wie "Vampire Survivors".  
Man spielt einen Charakter mit automatischen Angriffen und muss sich durch unendlich viele spawnende Gegner kämpfen.  
Roguelike heißt: Gegner, Upgrades usw. in jedem Spieldurchlauf zufällig und wenn man stirbt, verliert man alles und fängt von neuem an.  

Charakter:  
Der Charakter hat Waffen, die ohne Input des Spielers automatisch angreifen.  
Der Charakter soll bestimmt viele Leben haben.  
Der Spieler kann durch generische Angriffe Schaden bekommen.  
Wenn die Leben auf 0 fallen, ist das Spiel vorbei.  
Der Charakter soll außerdem Energie haben, die eingesetzt werden kann, um Fähigkeiten auszuführen.  

XP:  
Wenn man Gegner tötet, droppen sie XP, die man einsammeln kann.  
Wenn man genug XP gesammelt hat, bekommt man ein Level-Up.  

Level-Up:  
Mit einem Level-Up kann man zwischen drei Upgrades aussuchen, die Stats des Spielers verbessern, neue Angriffe/Fähigkeiten hinzufügen usw.  
Upgrades sollen in verschiedenen Seltenheiten eingestuft sein: Je seltener, desto besser.  

Gegner:  
Gegner sollen immer weiter spawnen und je länger das Spiel geht, desto mehr und stärkere Gegner spawnen.  
Alle 5 Level des Charakters oder nach einer bestimmten Zeit soll ein Boss spawnen, der besondere Waffen/Fähigkeiten droppt.  

Fähigkeiten:  
Der Charakter soll Fähigkeiten freischalten und benutzen können wie z.B. Dash, Explosion, Boosters.  
Diese kann der Spieler mit definierten Tasten aktivieren können.  

Felder:  
Es sollen Felder auf vorher definierten Teilen der Map sein, die Leben oder Energie regenerieren, den Charakter buffen oder sonstiges können.  
Es soll auch Felder geben, die sowohl dem Charakter, als auch Gegner Schaden hinzufügen können z.B. Fallen.  


2. Noah Utech:  

3. Joshua Supper:  

4. Dennis Andler:
   
Um Exp zum leveln zu bekommen sollen Orbs eingefügt werden. Diese sollen erstmal nur beim Spielstart spawnen und wenn der Roboter sie berührt verschwinden.

Das größte Problem hier ist die Kollision einzuführen. Hierfür benutzen wir die berühmten Axis-Aligned-Bounding-Boxes. Diese haben einen sehr schnellen Kollisionstest und können in Zukunft für feingranularere Objekte einfach übereinander gestacked werden. Bisher ist die AABB nur für den Roboter und die Orbs definiert. 

Mit den AABBs und einem einfachen Kollisioncheck der für jeden Frame ausgeführt wird, lassen sich die Orbs nun einfach durch eine neue Klasse einfügen. Die Orbpositionen lassen sich mit einer eingebauten Methode zufällig innerhalb des Screens setzen.
(Achtung: Bisher werden die Orbs zufälig innherhalb des Screens mit der Methode generiert, dies ist jedoch nicht immer sinnvoll, da Screengröße und Arenagröße nicht gleich sein müssen. Auch ist in der Arena noch keine Wandlogik eingebaut, so dass das spawnen des Orbs auf einer Wand bisher möglich ist.) 

Für die Zukunft könnte man für bessere Performance überlegen ob sich ein anderes Modell als "Kollisionscheck mit jedem Objektpaar auzurechnen" lohnen könnte, da dies für viele Objekte schlecht skaliert (Vielleicht Ray Tracing?). 

<img width="420" height="420" alt="newfeature_orbs" src="https://github.com/user-attachments/assets/e5783426-1ed7-4309-9f36-8d4be6678c48" />

Ein Testmodus wurde eingefügt der mit einer Flag in der main Datei an und ausgeschaltet werden kann. Der Testmodus dient unserem Entwicklerteam zur Visualisierung von sonst versteckten Berechnungen. Ein gutes Beispiel sind die AABB, die sonst dem Spieler nicht gezeigt werden. Das ganze soll dann beim debuggen helfen. 

<img width="353" height="379" alt="screen_feature_testmodus" src="https://github.com/user-attachments/assets/78ee1e65-bfa2-4292-9eb2-e931810728a7" />

