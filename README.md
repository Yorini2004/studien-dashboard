# Studien-Dashboard

Dieses Projekt ist ein prototypisches Studien-Dashboard fuer das Modul
"Objektorientierte und funktionale Programmierung mit Python".

Das Programm zeigt wichtige Kennzahlen zum Studienfortschritt an und erlaubt
eine einfache Pflege der Studiendaten ueber ein Konsolenmenue.

## Ziel des Projekts

Ziel ist es, den eigenen Studienfortschritt uebersichtlich darzustellen.
Dabei stehen folgende Fragen im Mittelpunkt:

- Wie hoch ist der aktuelle Notendurchschnitt?
- Wie viele ECTS wurden bereits bestanden?
- Wie hoch ist der Studienfortschritt in Prozent?
- Welche Module sind bereits abgeschlossen?
- Welche Module haben noch keine Pruefungsleistung?

Der Schwerpunkt des Projekts liegt auf der objektorientierten Modellierung
und der Umsetzung eines einfachen, aber funktionsfaehigen Prototyps in Python.

## Objektorientierter Aufbau

Das Programm verwendet vier fachliche Hauptklassen:

- Pruefungsleistung
- Modul
- Semester
- Studiengang

Der Aufbau ist:

```text
Studiengang
  enthaelt mehrere Semester
    enthaelt mehrere Module
      enthaelt eine Pruefungsleistung