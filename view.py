"""Darstellungs-Schicht (View) des Studien-Dashboards.

Die View ist die einzige Stelle im Programm, die print() und input()
verwendet. Sie enthaelt keine fachliche Logik und rechnet nichts aus: Alle
Zahlen bekommt sie fertig vom Controller uebergeben.

Die Ausgabe erfolgt bewusst nur mit der Standardbibliothek. Eine
Weiterentwicklung mit der Bibliothek 'rich' waere moeglich, wuerde aber eine
zusaetzliche Installation erfordern.
"""

from __future__ import annotations

from modell import Semester

# Breite der Trennlinien und des Fortschrittsbalkens
BREITE = 60
BALKEN_BREITE = 30
SKALA_BREITE = 25          # Breite der Notenskala von 1,0 bis 5,0


class KonsolenView:
    """Zeigt das Dashboard an und fragt Eingaben ueber die Konsole ab."""

    # ------------------------------------------------------------------
    # Ausgaben
    # ------------------------------------------------------------------

    def zeige_begruessung(self) -> None:
        """Begruessung beim Programmstart."""
        print()
        print("=" * BREITE)
        print("STUDIEN-DASHBOARD".center(BREITE))
        print("=" * BREITE)

    def zeige_menue(self) -> None:
        """Zeigt das Auswahlmenue der Konsole."""
        print()
        print("-" * BREITE)
        print("1 - Uebersicht anzeigen")
        print("2 - Daten speichern")
        print("3 - Daten laden")
        print("4 - Semester hinzufuegen")
        print("5 - Modul hinzufuegen")
        print("6 - Pruefungsleistung hinzufuegen")
        print("7 - Modul loeschen")
        print("0 - Programm beenden")
        print("-" * BREITE)

    def zeige_meldung(self, text: str) -> None:
        """Gibt eine normale Rueckmeldung aus."""
        print(text)

    def zeige_fehler(self, text: str) -> None:
        """Gibt eine Fehlermeldung deutlich erkennbar aus."""
        print("[!] " + text)

    def zeige_uebersicht(self, kennzahlen: dict, semesterliste: list[Semester]) -> None:
        """Zeigt das eigentliche Dashboard.

        Die Kennzahlen sind bereits fertig berechnet und werden hier nur noch
        formatiert. Die Semesterliste wird durchlaufen, um die Module
        anzuzeigen.
        """
        print()
        print("=" * BREITE)
        print("STUDIEN-DASHBOARD".center(BREITE))
        print("=" * BREITE)
        print(f"Studiengang            : {kennzahlen['studiengang']}")
        print(f"Ziel-Notendurchschnitt : {kennzahlen['ziel_notendurchschnitt']:.1f}")
        print(f"Aktueller Durchschnitt : {self._durchschnitt_als_text(kennzahlen['notendurchschnitt'])}")
        print(f"Zielerreichung         : {self._ziel_als_text(kennzahlen)}")
        for zeile in self._notenskala(kennzahlen):
            print(zeile)
        print(f"Bestandene ECTS        : {kennzahlen['bestandene_ects']} von {kennzahlen['gesamt_ects']}")
        print(f"Studienfortschritt     : {kennzahlen['studienfortschritt']:.2f} %")
        print(f"Fortschritt            : {self._fortschrittsbalken(kennzahlen['studienfortschritt'])}")
        print(f"Module                 : {kennzahlen['bestandene_module']} bestanden | "
              f"{kennzahlen['offene_module']} offen | "
              f"{kennzahlen['nicht_bestandene_module']} nicht bestanden")
        print("=" * BREITE)

        if len(semesterliste) == 0:
            print("Es ist noch kein Semester angelegt.")
            return

        for semester in semesterliste:
            print()
            print(f"Semester {semester.nummer}")
            print("-" * BREITE)

            if len(semester.module) == 0:
                print("  (noch keine Module in diesem Semester)")
                continue

            for modul in semester.module:
                print("  " + self._modul_als_text(modul))

        print()

    # ------------------------------------------------------------------
    # Eingaben
    # ------------------------------------------------------------------

    def frage_auswahl(self) -> str:
        """Fragt die Menueauswahl ab."""
        return input("Bitte Auswahl eingeben: ").strip()

    def frage_text(self, frage: str) -> str:
        """Fragt einen Text ab, zum Beispiel einen Modulnamen."""
        return input(frage).strip()

    def frage_ganzzahl(self, frage: str) -> int | None:
        """Fragt eine ganze Zahl ab. Bei einer Fehleingabe wird None geliefert."""
        eingabe = input(frage).strip()

        try:
            return int(eingabe)
        except ValueError:
            self.zeige_fehler("Bitte eine ganze Zahl eingeben.")
            return None

    def frage_kommazahl(self, frage: str) -> float | None:
        """Fragt eine Kommazahl ab. Komma und Punkt sind beide erlaubt."""
        eingabe = input(frage).strip().replace(",", ".")

        try:
            return float(eingabe)
        except ValueError:
            self.zeige_fehler("Bitte eine Zahl eingeben, zum Beispiel 2.3.")
            return None

    # ------------------------------------------------------------------
    # Interne Hilfsmethoden zur Formatierung
    # ------------------------------------------------------------------

    def _modul_als_text(self, modul) -> str:
        """Baut die Anzeigezeile eines Moduls zusammen."""
        text = f"{modul.name:<22} | {modul.ects:>2} ECTS | "

        if modul.pruefungsleistung is None:
            return text + "noch keine Pruefungsleistung"

        if modul.ist_abgeschlossen():
            status = "bestanden"
        else:
            status = "nicht bestanden"

        return (text + f"{modul.pruefungsleistung.art:<10} | "
                       f"Note {modul.pruefungsleistung.note:.1f} -> {status}")

    def _durchschnitt_als_text(self, notendurchschnitt: float) -> str:
        """Ein Durchschnitt von 0.0 bedeutet: noch keine bestandene Leistung."""
        if notendurchschnitt == 0.0:
            return "noch keine bestandene Pruefungsleistung"

        return f"{notendurchschnitt:.2f}"

    def _ziel_als_text(self, kennzahlen: dict) -> str:
        """Formuliert die Zielerreichung als kurzen Text."""
        if kennzahlen["notendurchschnitt"] == 0.0:
            return "noch nicht bewertbar"

        if kennzahlen["ziel_erreicht"]:
            return "Ziel erreicht"

        return "Ziel noch nicht erreicht"

    def _notenskala(self, kennzahlen: dict) -> list[str]:
        """Zeichnet eine Skala von 1,0 bis 5,0 mit Ziel- und Ist-Marke.

        Beide Werte kommen fertig vom Controller. Hier wird nur die Position
        auf der Skala bestimmt und das Zeichen gesetzt.
        """
        durchschnitt = kennzahlen["notendurchschnitt"]

        if durchschnitt == 0.0:
            return []

        skala = ["-"] * SKALA_BREITE
        pos_ziel = self._skalenposition(kennzahlen["ziel_notendurchschnitt"])
        pos_ist = self._skalenposition(durchschnitt)

        # O steht fuer den aktuellen Durchschnitt, | fuer das Ziel. Liegen
        # beide auf derselben Spalte, gewinnt die Ist-Marke.
        skala[pos_ziel] = "|"
        skala[pos_ist] = "O"

        return ["Notenskala             : 1.0 [" + "".join(skala) + "] 5.0"]

    def _skalenposition(self, note: float) -> int:
        """Rechnet eine Note von 1,0 bis 5,0 in eine Spalte der Skala um."""
        anteil = (note - 1.0) / 4.0
        spalte = int(anteil * (SKALA_BREITE - 1))

        if spalte < 0:
            return 0
        if spalte > SKALA_BREITE - 1:
            return SKALA_BREITE - 1

        return spalte

    def _fortschrittsbalken(self, prozent: float) -> str:
        """Erzeugt einen einfachen Fortschrittsbalken aus Textzeichen."""
        gefuellt = int(prozent / 100 * BALKEN_BREITE)

        if gefuellt > BALKEN_BREITE:
            gefuellt = BALKEN_BREITE

        return "[" + "#" * gefuellt + "-" * (BALKEN_BREITE - gefuellt) + "]"
