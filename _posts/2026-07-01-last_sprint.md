---
title: "Last Sprint"
date: 2026-07-01
---

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

Texturen sind von Craftpix.net

(Zufällig ausgewählte Texturen heißt: Jedes mal wenn man das Spiel neu lädt, werden aus ausgewählten Texturen zufällig welche gewählt, sodass die Map immer etwas anders aussieht.
Die ist vor allem in der Wüste und in der Stein-Region zu sehen.  
Die Objekte haben außerdem jeweils ihre eigenen Hitboxen angepasst bekommen, sodass diese realistisch sind.  
Die meisten Objekte haben außerdem einen Effekt erhalten, sodass der Spieler hinter den Objekten verschwindet. Das soll das Spiel etwas räumlicher wirken lassen.  
<img width="906" height="846" alt="image" src="https://github.com/user-attachments/assets/067b5f96-7085-4a4d-9349-9c86700541e4" />
<img width="995" height="1003" alt="image" src="https://github.com/user-attachments/assets/e0176d01-8b11-4f12-862e-7c1af9a3cf07" />
<img width="998" height="998" alt="image" src="https://github.com/user-attachments/assets/3e2fe74a-a8a1-4cf4-ad1b-9f2760f907a1" />
<img width="995" height="999" alt="image" src="https://github.com/user-attachments/assets/6783f9f8-9039-4b86-9585-e9bd009a6170" />
<img width="984" height="923" alt="image" src="https://github.com/user-attachments/assets/56384a6d-6f65-4301-b990-6502be804954" />


Nach dem Hinzufügen von Gegnerarten, habe ich den Gegnern Animationen für Laufen und Sterben gegeben (Goblin, Wolf, Slime, Biene).  

Der Kegelangriff des Spielers wurde dann von einem umherschwingenden Schwert ausgetauscht. Das Schwert schwingt in einem 45° Winkel periodisch nach rechts/links.  
Das Schwingen skaliert mit der Angriffsgeschwindigkeit.  
Die Schwergröße skaliert mit der Angriffsreichweite.  

<img width="400" height="398" alt="Ohne Titel" src="https://github.com/user-attachments/assets/29cdfc0c-3041-434a-8115-50a9ea156d6d" />

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

--- 

Noah:

Menüs und Benutzeroberfläche
Hauptmenü

Es wurde ein Hauptmenü hinzugefügt. Von dort aus kann der Spieler:

- ein neues Spiel starten,
- die Statistiken ansehen,
- das Spiel beenden.

<img width="300" height="290" alt="Screenshot 2026-07-07 192814" src="https://github.com/user-attachments/assets/8faa5bb3-d3bb-420d-a17f-c36743d97a4e" />




Pausemenü

Es wurde ein Pausemenü implementiert. Dieses ermöglicht:

- Spiel fortsetzen,
- zum Hauptmenü zurückkehren,
- Spiel beenden.


<img width="300" height="200" alt="Screenshot 2026-07-07 192913" src="https://github.com/user-attachments/assets/5bcf8b3f-54db-4135-9bd1-0d2e56865150" />



Statistiksystem

Ein Statistiksystem wurde eingeführt.

Jeder Spieldurchlauf wird dauerhaft gespeichert.
Vergangene Runs können eingesehen werden.
- Mit den WASD kann durch die Einträge gescrollt werden.
- <img width="997" height="791" alt="Screenshot 2026-07-07 192814" src="https://github.com/user-attachments/assets/704d20e1-c1e2-46ca-8d30-9cc376ce46c1" />
Mit R können alle Statistiken gelöscht werden.



<img width="300" height="300" alt="Screenshot 2026-07-07 192939" src="https://github.com/user-attachments/assets/24653666-b5a0-4939-a4cb-3288b38256e5" />




Startbildschirm

Ein neuer Startbildschirm mit animierten Wolken.




https://github.com/user-attachments/assets/e0e6f295-1255-4e98-b58a-e2758ecce699





Hintergründe

Für die verschiedenen Menüs wurden passende Hintergründe erstellt, wodurch das Spiel deutlich hochwertiger wirkt (wurden ki erstellt).




<img width="300" height="300" alt="Screenshot 2026-07-07 193352" src="https://github.com/user-attachments/assets/85af3bad-a518-4fb9-8da8-0e4749d6f44d" />




<img width="300" height="300" alt="Screenshot 2026-07-07 193411" src="https://github.com/user-attachments/assets/9666fc1d-193c-47d1-8934-9d251c3eefcd" />



<img width="300" height="300" alt="Screenshot 2026-07-07 193425" src="https://github.com/user-attachments/assets/6e81a900-6f80-46ee-9e93-28dd6de9b702" />






Map-Auswahl

Vor Spielbeginn kann der Spieler nun zwischen den verfügbaren Arenen wählen.


<img width="300" height="300" alt="Screenshot 2026-07-07 193503" src="https://github.com/user-attachments/assets/9f282af1-2afd-4c3d-a539-148f73c0494a" />






Inhalte zusätlich




Lbyrinth erste Arena

Das labyrinth der ersten map wurde so überarbeitet, dass player und enemys sich optimert bewegen können und durch jeden Durchgang passen.

Zweite Arena

Die zweite Arena wurde vollständig fertiggestellt und kann nach der Freischaltung gespielt werden.



https://github.com/user-attachments/assets/64971b83-200a-47e7-8238-d00ec505268d






Tornado

Der Tornado wurde überarbeitet. Seine Anziehungskraft hängt nun vom Abstand des Spielers ab. Je näher sich der Spieler befindet, desto stärker wird er angezogen.





https://github.com/user-attachments/assets/2ee07d60-99c0-4944-8345-baa81c66182b






Shop und Fortschrittssystem
Shop

Das Shop-System wurde vollständig integriert.

Die Buffs Ice Relic und Ricochet Relic können mit Coins gekauft werden. Erst anschließend erscheinen sie bei einem Level-Up als auswählbare Buffs.



<img width="300" height="170" alt="Screenshot 2026-07-07 195059" src="https://github.com/user-attachments/assets/64cd68d9-0bf3-45c5-a73b-4b36a44bfa87" />




Zweite Map freischalten

Die neue Labyrinth-Map muss für coins im Shop freigeschaltet werden.

Für das Speichern und Laden der Freischaltung wurde das Shop-System verwendet. Dadurch musste kein zusätzliches Speichersystem entwickelt werden.



Audio

Für den Startbildschirm wurde passende Hintergrundmusik eingefügt.

Außerdem wurde versucht, das Musikstottern durch einen größeren Audiobuffer zu beheben. Aufgrund eines Problems mit der WSL-Verbindung brachte dies jedoch keine Verbesserung, weshalb der ursprüngliche Buffer wiederhergestellt wurde. Auch nach trouble shots mit Kis wurde keine lösung gefunden für WSL version 2. 

Bugfixes

Folgende Fehler wurden behoben:

- Absturz des Pausemenüs beseitigt.
- Bewegungstiles funktionieren wieder korrekt.
- Attributfehler beim Laden der Labyrinth-Map behoben.
- Gegner verursachen während ihrer Todesanimation keinen Schaden mehr.
- Level-Up-Buffs bleiben nach dem Verlassen eines Runs nicht mehr erhalten.
- Der BuffManager wird beim Wechsel ins Hauptmenü vollständig zurückgesetzt.





Sonstiges
Reset-System

Das Reset-System wurdeüberarbeitet. Beim Neustart werden nun Spieler, Gegner, Orbs, Level, Health, Stamina und sämtliche Level-Buffs korrekt zurückgesetzt.

Vorstellungsvideo

Für das Projekt wurde ein Vorstellungsvideo erstellt. Nach mehreren Bearbeitungsversuchen und viel verlorener Zeit (Sprites erstellen lassen und alle möglichen versuche zu schneiden mit mehreren Schnittsoftwares) wurde dieses jedoch verworfen, da die verwendete Videoschnittsoftware ohne Premium-Version keine zufriedenstellende Qualität ermöglichte (keine viedos > 1min, begrenzte auswahl an Feautres wie Übergänge, text einfügungen usw und Musik nich bearbeitbar).



---
---

Dennis(I3luki):


Zuerst wurde die Logik für den Surprisetile eingeführt. Diese gibt einen zufälligen Effekt von 3 Effekten (Heilung, Schnelligkeit, Gift). Es stand im Raum der Liste an zufälligen Effekten noch mehr hinzuzufügen, dies wurde bis zum jetzigen Zeitpunkt nicht gemacht.

Weiterhin wurde ein Cooldown für die Tiles eingeführt, welcher auch visuell dargestellt wird. Später wurde ein ähnlicher Effekt auch für Status-Effekte des Spieler eingeführt.
TODO: VIDEO EINFÜGEN VON COOLDOWN

Um dem Spiel etwas mehr Geschmack zu geben wurden Relikte eingeführt. Diese kann man bei einer LevelUp-Belohnung bekommen. Sie können in 3 verschiedenen Seltenheiten(Common, Rare, Epic) kommen. Initial wurden 2 Relikte eingeführt. Das eine verlangsamt Gegner bei einem Treffer und das andere schickt einen Ricochet Effekt durch nahe Gegner falls es welche in der Nähe gibt.
Später wurden dann noch Relikte mit folgenden Effekten hinzugefügt:
- temporäre, stapelbare Reichweite bei Treffern
- verbesserte Angriffgeschwindigkeit jede x Hiebe für y Hiebe
- kurzer aber schneller Geschwindigkeitsschub bei Treffern
- muplipikative Attributsanpassung (1.7x DMG, 0.7x maxHealth, 0.5x Range)
- Lebensraub basierend auf fehlendem Leben

Für diese Relikte wurden später dann auch Icons eingefügt, so wie die visuelle Seite bei Auswahl der LevelUp-Belohnung überarbeitet.
TODO: VIDEO EINFÜGEN VON RELIKTEN

Musik und Sounds wurden nach Auswahl mit dem Team eingefügt. Hier gab es Probleme mit WSL die bisher leider nicht gefixt werden konnten. 

Der Rest der Zeit wurde für genaue PR-Reviews so wie viel Refactoring verwendet. Bugfixes nahmen natürlich auch gut Zeit ein. 

----
---

Joshua (Oshy44)

Zuerst habe ich neue Gegnerarten eingeführt. Insgesamt wurden vier verschiedene Gegner hinzugefügt, die jeweils eigene Fähigkeiten besitzen und dadurch unterschiedliche Herausforderungen für den Spieler darstellen.

Folgende Gegner wurden ergänzt:

* **Goblin:** Der Goblin erhält ab 30% Leben einen Rage-Modus, wodurch er gefährlicher wird.
* **Biene:** Die Biene verursacht Giftschaden, der den Spieler zusätzlich belastet.
* **Wolf:** Der Wolf besitzt eine Dash-Fähigkeit und kann sich dadurch schnell auf den Spieler zubewegen.
* **Slime:** Der Slime verursacht keinen direkten Schaden, verlangsamt den Spieler jedoch, sobald dieser mit ihm in Kontakt kommt.

Anschließend habe ich den **WaveManager** erstellt. Dieser kontrolliert, welche Gegner in den einzelnen Wellen spawnen können. Es werden die Gegner innerhalb der Waves noch zufällig ausgewählt was zu unterschiedlichen Run erlebnissen führt. In anfänglichen Wellen spawnen erstmal Goblins und erst in höheren können auch stärkere Gegner spawnen. Mit jeder neuen Welle erhöht sich jedoch die Schwierigkeit, da mehr Gegner erscheinen und diese zusätzlich stärker werden. Dabei skalieren sowohl der Schaden als auch die Lebenspunkte der Gegner mit fortschreitenden Waves.

Zusätzlich wurden für die verschiedenen Gegner eigene **XP-Orbs** eingeführt. Diese geben je nach Gegner unterschiedlich viele Erfahrungspunkte. Darauf aufbauend wurde auch das Level-System überarbeitet, sodass die benötigte Erfahrung besser zu den erhaltenen XP-Orbs passt und die Progression im Spiel ausgeglichener wirkt.

Außerdem wurden **Boss-Monster** hinzugefügt. Diese sind größer und deutlich stärker als normale Gegner und erscheinen alle fünf Waves. Damit der Spieler jederzeit sehen kann, wie weit er bereits gekommen ist, wurde zusätzlich ein **Wavecounter** eingebaut, der die aktuelle Welle im Spiel anzeigt.

Zum Schluss habe ich eine neue Seite im Shop eingefügt. Dort kann der Spieler sein gesammeltes Gold verwenden, um eigene Stats zu verbessern und sich dadurch langfristig stärker zu machen.

<img width="900" height="550" alt="image" src="https://github.com/user-attachments/assets/98837528-b018-48e9-84ab-0463d811350f" />
<img width="675" height="594" alt="image" src="https://github.com/user-attachments/assets/35a6a8fd-4f3c-4292-9c9b-9f90e6b20d35" />


