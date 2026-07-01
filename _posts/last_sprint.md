---
title: Sprint 4/5?
date: 2026-07-01
---

Simon:
Nachdem die Gegnerbewegung hinzugefügt wurde, habe ich eingeführt, dass zwei Gegner jede Sekunde spawnen und max. 10 Gegner gleichzeitig exisiteren können.  

Als nächstes habe ich mir kostenlose Charakteranimations-Assets gedownloaded und ein Animations-Handler eingeführt, um Animationen leicht in das Spiel einzufügen.
Dieser Handler ist vor allem hilfreich, weil man damit sehr leicht Animationen abspielen lassen und diese einheitlich vergrößern/verkleinern kann.
Damit habe ich dann die Characteranimations für idle, moving, idle-attack und moving-attack hinzugefügt. (Später wurden idle-attack und moving-attack entfernt).  

Mithilfe einer hinzugefügten Textures Klasse, ist es jetzt sehr leicht Texturen ins Spiel zu laden und beliebig zu plazieren und zu verändern.
Folgende Objekte haben Texturen erhalten:
- Labyrinth-Region Boden
- Labyrinthwände
- Stein-Region Boden
- Steine in Stein-Region werden zufällig von 7 Steintexturen geladen
- Steinerhöhungen in Blitz-Region werden zufällig von 2 Texturen geladen
- Löcher in Blitz-Region werden zufällig von 3 Texturen geladen
- Tornado in Blitz-Region hat Animationen bekommen
- Blitze in Blitz-Region haben Animation und Schatten als Indikator bekommen
- Wüsten-Region Boden
- Kaktus in Wüsten-Region
- Knochen in Wüsten-Region werden zufällig von 6 Knochentexturen geladen
- Rippenknochen in Wüsten-Region werden zufällig von 2 Texturen geladen
- Zentrum-Region Boden
- Zentrum-Region hat jeweils drei zum naheliegenden Region passende Bäume/Büsche bekommen, die zufällig aus Texturen geladen werden
- Zentrum-Region hat als Map-Mittelpunkt einen zerfallenen Tempel bekommen
- Speed,Healing,Question-Tiles haben darüber fliegende Icons bekommen
- Orbs haben Texturen erhalten

(Zufällig ausgewählte Texturen heißt: Jedes mal wenn man das Spiel neu lädt, werden aus ausgewählten Texturen zufällig welche gewählt, sodass die Map immer etwas anders aussieht.
Die ist vor allem in der Wüste und in der Stein-Region zu sehen.  
Die Objekte haben außerdem jeweils ihre eigenen Hitboxen angepasst bekommen, sodass diese realistisch sind.  
Die meisten Objekte haben außerdem einen Effekt erhalten, sodass der Spieler hinter den Objekten verschwindet. Das soll das Spiel etwas räumlicher wirken lassen.  

Nach dem Hinzufügen von Gegnerarten, habe ich den Gegnern Animationen für Laufen und Sterben gegeben (Goblin, Wolf, Slime, Biene).  

Der Kegelangriff des Spielers wurde dann von einem umherschwingenden Schwert ausgetauscht. Das Schwert schwingt in einem 45° Winkel periodisch nach rechts/links.  
Das Schwingen skaliert mit der Angriffsgeschwindigkeit.  
Die Schwergröße skaliert mit der Angriffsreichweite.  

Ich habe einen Bug gefixed, wo Gegner in Objekten spawnen und sich dadurch nicht bewegen können.  

Ich habe Healing, Speed und Questionmark Tiles gleichmäßig auf die Map verteilt.  
Außerdem habe ich folgende Balance-Changes durchgeführt:  
- Spieler hat wieder 100 Leben
- Gegner machen angepassten Damage
- Gegner machen jetzt nicht mehr konstant Schaden, sondern jede 1 Sekunde können sie 1 mal Schaden am Spieler hinzufügen
- Buffs können nur 1 mal gleichzeitig sein (vor allem wegen Slime slow)
- Slime slow ist nur noch solange, wie man im slime steht
- Waves spawnen nicht mehr gleichzeitig, sondern verteilt
- Waves skalieren nicht mehr linear, sondern etwas langsamer
- Reliktstärken wurden angepasst
- Level-Up progression wurde angepasst (quadratisches Wachstum an benötigtem XP)
- Level-Up Power-Ups wurden angepasst
- Health Tiles Heilung wurde erhöht
- Speed Tile Geschwindigkeitsboost wurde gesenkt
