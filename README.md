# Studien-Dashboard

Dieses Projekt ist ein Studien-Dashboard für das Modul
"Objektorientierte und funktionale Programmierung mit Python" im Bachelor Studiengang "Angewandte Künstliche Intelligenz" an der IU.

Das Programm zeigt wichtige Kennzahlen zum Studienfortschritt an:

- aktueller Notendurchschnitt
- bestandene ECTS
- gesamte ECTS
- Studienfortschritt in Prozent
- Übersicht der Module und Prüfungsleistungen

## Ziel des Projekts

Ziel ist es, ein einfaches Dashboard für den eigenen Studienfortschritt zu erstellen.
Der Schwerpunkt liegt auf der objektorientierten Modellierung mit Python.

## Objektorientierter Aufbau

Das Programm verwendet folgende Klassen:

- `Prüfungsleistung`
- `Modul`
- `Semester`
- `Studiengang`

Der Aufbau ist:

```text
Studiengang
  enthält mehrere Semester
    enthält mehrere Module
      enthält eine Prüfungsleistung