"""Studien-Dashboard - Prototyp fuer den Portfoliokurs
'Objektorientierte und funktionale Programmierung mit Python'.

Diese Datei ist der Startpunkt des Programms. Sie erzeugt die Objekte der
einzelnen Schichten und verbindet sie miteinander.

Aufbau des Programms (Schichten):

    main.py         DashboardApp             Startpunkt, verbindet die Schichten
    view.py         KonsolenView             Ein- und Ausgabe ueber die Konsole
    controller.py   DashboardController      Ablaufsteuerung
    repository.py   StudiengangRepository    Speichern und Laden (JSON)
    modell.py       Studiengang, Semester,   Fachmodell
                    Modul, Pruefungsleistung
    beispieldaten.py                         Startdaten fuer den ersten Lauf

Start des Programms:  python main.py
"""

from controller import DashboardController
from repository import StudiengangRepository
from view import KonsolenView

# Name der Datei, in der die Studiendaten gespeichert werden.
DATEINAME = "studiengang.json"


class DashboardApp:
    """Startpunkt der Anwendung.

    Die Klasse erzeugt Repository, View und Controller und verbindet sie
    miteinander. Nur an dieser einen Stelle ist bekannt, welche konkreten
    Klassen verwendet werden. Soll spaeter zum Beispiel statt der JSON-Datei
    eine Datenbank genutzt werden, muss nur hier ein anderes Repository
    eingesetzt werden.
    """

    def __init__(self, dateiname: str = DATEINAME) -> None:
        self._repository = StudiengangRepository(dateiname)
        self._view = KonsolenView()
        self._controller = DashboardController(self._repository, self._view)

    def start(self) -> None:
        """Startet das Dashboard."""
        self._controller.starte()


if __name__ == "__main__":
    DashboardApp().start()
