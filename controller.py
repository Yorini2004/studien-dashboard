"""Ablaufsteuerung (Controller) des Studien-Dashboards.

Der Controller liegt zwischen der View und dem Fachmodell. Er nimmt die
Menueauswahl entgegen, holt sich die noetigen Eingaben ueber die View, ruft
die passenden Methoden der Fachklassen auf und laesst das Ergebnis wieder
ueber die View ausgeben.

Der Controller selbst gibt nichts direkt auf der Konsole aus und liest auch
nichts direkt ein. Dadurch koennte die View spaeter ausgetauscht werden, ohne
dass der Ablauf geaendert werden muss.
"""

from __future__ import annotations

from beispieldaten import erstelle_beispieldaten
from modell import Modul, Pruefungsleistung, Semester, Studiengang
from repository import StudiengangRepository
from view import KonsolenView


class DashboardController:
    """Steuert den Ablauf des Programms."""

    def __init__(self, repository: StudiengangRepository, view: KonsolenView) -> None:
        self._repository = repository
        self._view = view
        self._studiengang: Studiengang | None = None

    def starte(self) -> None:
        """Startet das Programm und haelt die Menueschleife am Laufen."""
        self._studiengang = self._lade_startdaten()
        self._view.zeige_begruessung()

        weiter = True
        while weiter:
            self._view.zeige_menue()
            auswahl = self._view.frage_auswahl()
            weiter = self._verarbeite_auswahl(auswahl)

    # ------------------------------------------------------------------
    # Menuesteuerung
    # ------------------------------------------------------------------

    def _verarbeite_auswahl(self, auswahl: str) -> bool:
        """Fuehrt die gewaehlte Aktion aus.

        Rueckgabe False bedeutet: Das Programm soll beendet werden.
        """
        if auswahl == "1":
            self._zeige_uebersicht()
        elif auswahl == "2":
            self._speichere_daten()
        elif auswahl == "3":
            self._lade_daten()
        elif auswahl == "4":
            self._semester_hinzufuegen()
        elif auswahl == "5":
            self._modul_hinzufuegen()
        elif auswahl == "6":
            self._pruefungsleistung_hinzufuegen()
        elif auswahl == "7":
            self._modul_loeschen()
        elif auswahl == "0":
            self._view.zeige_meldung("Programm wird beendet.")
            return False
        else:
            self._view.zeige_fehler("Ungueltige Auswahl. Bitte eine Zahl von 0 bis 7 eingeben.")

        return True

    # ------------------------------------------------------------------
    # Einzelne Aktionen
    # ------------------------------------------------------------------

    def _zeige_uebersicht(self) -> None:
        """Stellt die Kennzahlen zusammen und laesst sie anzeigen."""
        self._view.zeige_uebersicht(self._kennzahlen(), self._studiengang.semester)

    def _kennzahlen(self) -> dict:
        """Sammelt alle Werte, die das Dashboard anzeigt, in einem Dictionary.

        So bekommt die View fertige Zahlen und muss selbst nicht rechnen.
        """
        modulzahlen = self._studiengang.zaehle_module()

        return {
            "studiengang": self._studiengang.name,
            "ziel_notendurchschnitt": self._studiengang.ziel_notendurchschnitt,
            "notendurchschnitt": self._studiengang.berechne_notendurchschnitt(),
            "ziel_erreicht": self._studiengang.ziel_erreicht(),
            "bestandene_ects": self._studiengang.berechne_bestandene_ects(),
            "gesamt_ects": self._studiengang.gesamt_ects,
            "studienfortschritt": self._studiengang.berechne_studienfortschritt(),
            "bestandene_module": modulzahlen["bestanden"],
            "offene_module": modulzahlen["offen"],
            "nicht_bestandene_module": modulzahlen["nicht_bestanden"],
        }

    def _speichere_daten(self) -> None:
        """Speichert den aktuellen Stand ueber das Repository."""
        try:
            self._repository.speichere(self._studiengang)
            self._view.zeige_meldung("Die Daten wurden gespeichert.")
        except OSError:
            self._view.zeige_fehler("Die Datei konnte nicht geschrieben werden.")

    def _lade_daten(self) -> None:
        """Laedt den zuletzt gespeicherten Stand."""
        if not self._repository.existiert():
            self._view.zeige_fehler("Es wurde noch nichts gespeichert.")
            return

        try:
            self._studiengang = self._repository.lade()
            self._view.zeige_meldung("Die Daten wurden geladen.")
        except (OSError, ValueError, KeyError):
            self._view.zeige_fehler("Die gespeicherte Datei konnte nicht gelesen werden.")

    def _semester_hinzufuegen(self) -> None:
        """Legt ein neues Semester an."""
        nummer = self._view.frage_ganzzahl("Nummer des neuen Semesters: ")

        if nummer is None:
            return

        try:
            neues_semester = Semester(nummer)
        except ValueError as fehler:
            self._view.zeige_fehler(str(fehler))
            return

        if self._studiengang.semester_hinzufuegen(neues_semester):
            self._view.zeige_meldung(f"Semester {nummer} wurde hinzugefuegt.")
        else:
            self._view.zeige_fehler("Dieses Semester existiert bereits.")

    def _modul_hinzufuegen(self) -> None:
        """Legt ein neues Modul in einem vorhandenen Semester an."""
        semester = self._frage_semester("Zu welchem Semester gehoert das Modul? ")

        if semester is None:
            return

        name = self._view.frage_text("Name des Moduls: ")
        ects = self._view.frage_ganzzahl("ECTS des Moduls (ganze Zahl): ")

        if ects is None:
            return

        try:
            neues_modul = Modul(name, ects)
        except ValueError as fehler:
            self._view.zeige_fehler(str(fehler))
            return

        if semester.modul_hinzufuegen(neues_modul):
            self._view.zeige_meldung(
                f"Modul '{neues_modul.name}' wurde zu Semester {semester.nummer} hinzugefuegt."
            )
        else:
            self._view.zeige_fehler("In diesem Semester gibt es bereits ein Modul mit diesem Namen.")

    def _pruefungsleistung_hinzufuegen(self) -> None:
        """Traegt eine Pruefungsleistung in ein vorhandenes Modul ein."""
        semester = self._frage_semester("In welchem Semester liegt das Modul? ")

        if semester is None:
            return

        modul = self._frage_modul(semester)

        if modul is None:
            return

        art = self._view.frage_text("Art der Pruefungsleistung: ")
        note = self._view.frage_kommazahl("Note (1.0 bis 5.0): ")

        if note is None:
            return

        try:
            modul.pruefungsleistung = Pruefungsleistung(art, note)
        except ValueError as fehler:
            self._view.zeige_fehler(str(fehler))
            return

        self._view.zeige_meldung(f"Pruefungsleistung fuer '{modul.name}' wurde eingetragen.")

    def _modul_loeschen(self) -> None:
        """Loescht ein Modul aus einem Semester."""
        semester = self._frage_semester("Aus welchem Semester soll geloescht werden? ")

        if semester is None:
            return

        name = self._view.frage_text("Name des Moduls: ")

        if semester.modul_loeschen(name):
            self._view.zeige_meldung(f"Modul '{name}' wurde geloescht.")
        else:
            self._view.zeige_fehler("Dieses Modul wurde nicht gefunden.")

    # ------------------------------------------------------------------
    # Gemeinsam genutzte Hilfsmethoden
    # ------------------------------------------------------------------

    def _frage_semester(self, frage: str) -> Semester | None:
        """Fragt eine Semesternummer ab und sucht das passende Semester."""
        nummer = self._view.frage_ganzzahl(frage)

        if nummer is None:
            return None

        semester = self._studiengang.semester_suchen(nummer)

        if semester is None:
            self._view.zeige_fehler("Dieses Semester existiert nicht.")

        return semester

    def _frage_modul(self, semester: Semester) -> Modul | None:
        """Fragt einen Modulnamen ab und sucht das passende Modul."""
        name = self._view.frage_text("Name des Moduls: ")
        modul = semester.modul_suchen(name)

        if modul is None:
            self._view.zeige_fehler("Dieses Modul gibt es in diesem Semester nicht.")

        return modul

    def _lade_startdaten(self) -> Studiengang:
        """Laedt gespeicherte Daten oder legt Beispieldaten an."""
        if self._repository.existiert():
            try:
                return self._repository.lade()
            except (OSError, ValueError, KeyError):
                self._view.zeige_fehler(
                    "Die gespeicherte Datei konnte nicht gelesen werden. "
                    "Es werden Beispieldaten verwendet."
                )

        return erstelle_beispieldaten()
