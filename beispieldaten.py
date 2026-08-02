"""Beispieldaten fuer den ersten Programmstart.

Wenn noch keine Datei 'studiengang.json' vorhanden ist, wird mit diesen Daten
gestartet. So ist das Dashboard sofort gefuellt und kann ausprobiert werden.
"""

from __future__ import annotations

from modell import Modul, Pruefungsleistung, Semester, Studiengang


def erstelle_beispieldaten() -> Studiengang:
    """Erzeugt einen kleinen Beispiel-Studiengang mit zwei Semestern."""
    studiengang = Studiengang("Artificial Intelligence", 2.0, 180)

    semester1 = Semester(1)
    semester1.modul_hinzufuegen(
        Modul("OOP", 5, Pruefungsleistung("Portfolio", 1.7))
    )
    semester1.modul_hinzufuegen(
        Modul("Mathematik", 5, Pruefungsleistung("Klausur", 2.3))
    )
    semester1.modul_hinzufuegen(
        Modul("Ethik", 5, Pruefungsleistung("Vortrag", 5.0))
    )

    semester2 = Semester(2)
    # Ein Modul ohne Pruefungsleistung: Es ist geplant, aber noch offen.
    semester2.modul_hinzufuegen(Modul("Statistik", 5))

    studiengang.semester_hinzufuegen(semester1)
    studiengang.semester_hinzufuegen(semester2)

    return studiengang
