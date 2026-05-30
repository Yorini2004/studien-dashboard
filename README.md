# Studien-Dashboard

Dieses Projekt ist ein einfacher Python-Prototyp für ein Studien-Dashboard.

Das Programm zeigt:
- den Studiengang
- den Ziel-Notendurchschnitt
- den aktuellen Notendurchschnitt
- die bestandenen ECTS
- den Studienfortschritt in Prozent
- gespeicherte Semester, Module und Prüfungsleistungen

## Aufbau

Das Programm ist objektorientiert aufgebaut. Es verwendet die Klassen:

- `Studiengang`
- `Semester`
- `Modul`
- `Pruefungsleistung`

Ein Studiengang enthält mehrere Semester. Ein Semester enthält mehrere Module. Ein Modul kann eine Prüfungsleistung besitzen.

## Speicherung

Die Daten werden in der Datei `studiengang.json` gespeichert. Dafür werden die Objekte vor dem Speichern in Dicts umgewandelt und beim Laden wieder als Objekte erzeugt.

## Start des Programms

Das Programm benötigt keine externen Bibliotheken.

Start über die Konsole:

```bash
python main.py