# Studien-Dashboard

Prototyp eines Dashboards für den eigenen Studienfortschritt. Das Projekt ist
im Rahmen des Portfoliokurses *Objektorientierte und funktionale Programmierung
mit Python* (DLBDSOOFPP01_D) an der IU Internationale Hochschule entstanden.

Das Dashboard zeigt an:

- Studiengang und Ziel-Notendurchschnitt
- aktueller Notendurchschnitt und ob das Ziel erreicht ist
- bestandene ECTS im Verhältnis zu den Gesamt-ECTS
- Studienfortschritt in Prozent mit Fortschrittsbalken
- Anzahl bestandener, offener und nicht bestandener Module
- alle Semester mit ihren Modulen und Prüfungsleistungen

## Aufbau

Das Programm ist in Schichten aufgeteilt. Jede Datei enthält genau eine
Zuständigkeit:

| Datei | Klasse(n) | Aufgabe |
| --- | --- | --- |
| **main.py** | *DashboardApp* | Startpunkt, erzeugt und verbindet die Schichten |
| **view.py** | *KonsolenView* | Ein- und Ausgabe über die Konsole |
| **controller.py** | *DashboardController* | Ablaufsteuerung, Menüverarbeitung |
| **repository.py** | *StudiengangRepository* | Speichern und Laden, Mapping Objekt ↔ JSON |
| **modell.py** | *Studiengang*, *Semester*, *Modul*, *Pruefungsleistung* | Fachmodell |
| **beispieldaten.py** | – | Startdaten für den ersten Programmstart |

Ein Studiengang enthält mehrere Semester, ein Semester mehrere Module und ein
Modul kann eine Prüfungsleistung besitzen. Die Fachklassen kennen weder die
Konsole noch die Datei, das Repository ist die einzige Stelle mit Wissen über
das Speicherformat.

## Speicherung

Die Daten liegen in der Datei `studiengang.json`. Das Repository wandelt die
Objekte vor dem Speichern in Dictionaries um und beim Laden wieder zurück in
Objekte.

## Start des Programms

Es werden keine externen Bibliotheken benötigt, nur Python 3.10 oder neuer.

```bash
python main.py
```

Danach erscheint das Konsolenmenü. Über die Zahlen 1 bis 7 lassen sich
Übersicht, Speichern, Laden, Semester, Module und Prüfungsleistungen
verwalten, mit 0 wird das Programm beendet.
