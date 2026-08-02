"""Persistenz-Schicht des Studien-Dashboards.

Das Repository ist die einzige Stelle im Programm, die die JSON-Datei kennt.
Es uebernimmt zwei Aufgaben:

1. Speichern und Laden der Datei,
2. das Umwandeln zwischen Fachobjekten und Dictionaries (das sogenannte
   Mapping).

Beide Aufgaben lagen frueher in den Fachklassen (Methoden als_dict() und
aus_dict()). Sie wurden hierher verschoben, damit das Fachmodell unabhaengig
von der gewaehlten Speichertechnik bleibt.
"""

from __future__ import annotations

import json
import os

from modell import Modul, Pruefungsleistung, Semester, Studiengang


class StudiengangRepository:
    """Laedt und speichert einen Studiengang in einer JSON-Datei."""

    def __init__(self, dateiname: str = "studiengang.json") -> None:
        self.dateiname = dateiname

    @property
    def dateiname(self) -> str:
        """Pfad der Datei, in der die Daten abgelegt werden."""
        return self._dateiname

    @dateiname.setter
    def dateiname(self, dateiname: str) -> None:
        if dateiname is None or str(dateiname).strip() == "":
            raise ValueError("Der Dateiname darf nicht leer sein.")
        self._dateiname = str(dateiname).strip()

    def existiert(self) -> bool:
        """Prueft, ob bereits eine gespeicherte Datei vorhanden ist."""
        return os.path.exists(self.dateiname)

    def speichere(self, studiengang: Studiengang) -> None:
        """Schreibt den Studiengang als JSON in die Datei."""
        daten = self._studiengang_als_dict(studiengang)

        with open(self.dateiname, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, indent=4, ensure_ascii=False)

    def lade(self) -> Studiengang:
        """Liest die Datei und erzeugt daraus wieder Fachobjekte."""
        with open(self.dateiname, "r", encoding="utf-8") as datei:
            daten = json.load(datei)

        return self._studiengang_aus_dict(daten)

    # ------------------------------------------------------------------
    # Mapping: Objekt -> Dictionary
    # Die folgenden Methoden sind interne Hilfsmethoden (fuehrender
    # Unterstrich) und werden nur innerhalb des Repositories benoetigt.
    # ------------------------------------------------------------------

    def _studiengang_als_dict(self, studiengang: Studiengang) -> dict:
        semester_liste = []

        for semester in studiengang.semester:
            semester_liste.append(self._semester_als_dict(semester))

        return {
            "name": studiengang.name,
            "ziel_notendurchschnitt": studiengang.ziel_notendurchschnitt,
            "gesamt_ects": studiengang.gesamt_ects,
            "semester": semester_liste,
        }

    def _semester_als_dict(self, semester: Semester) -> dict:
        module_liste = []

        for modul in semester.module:
            module_liste.append(self._modul_als_dict(modul))

        return {
            "nummer": semester.nummer,
            "module": module_liste,
        }

    def _modul_als_dict(self, modul: Modul) -> dict:
        if modul.pruefungsleistung is None:
            pruefungsleistung_daten = None
        else:
            pruefungsleistung_daten = self._pruefungsleistung_als_dict(
                modul.pruefungsleistung
            )

        return {
            "name": modul.name,
            "ects": modul.ects,
            "pruefungsleistung": pruefungsleistung_daten,
        }

    def _pruefungsleistung_als_dict(self, pruefungsleistung: Pruefungsleistung) -> dict:
        return {
            "art": pruefungsleistung.art,
            "note": pruefungsleistung.note,
        }

    # ------------------------------------------------------------------
    # Mapping: Dictionary -> Objekt
    # ------------------------------------------------------------------

    def _studiengang_aus_dict(self, daten: dict) -> Studiengang:
        studiengang = Studiengang(
            daten["name"],
            daten["ziel_notendurchschnitt"],
            daten["gesamt_ects"],
        )

        for semester_daten in daten["semester"]:
            studiengang.semester_hinzufuegen(self._semester_aus_dict(semester_daten))

        return studiengang

    def _semester_aus_dict(self, daten: dict) -> Semester:
        semester = Semester(daten["nummer"])

        for modul_daten in daten["module"]:
            semester.modul_hinzufuegen(self._modul_aus_dict(modul_daten))

        return semester

    def _modul_aus_dict(self, daten: dict) -> Modul:
        if daten["pruefungsleistung"] is None:
            pruefungsleistung = None
        else:
            pruefungsleistung = self._pruefungsleistung_aus_dict(
                daten["pruefungsleistung"]
            )

        return Modul(daten["name"], daten["ects"], pruefungsleistung)

    def _pruefungsleistung_aus_dict(self, daten: dict) -> Pruefungsleistung:
        return Pruefungsleistung(daten["art"], daten["note"])
