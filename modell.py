"""Fachklassen (Domain-Schicht) des Studien-Dashboards.

Diese Datei enthaelt ausschliesslich das Fachmodell: Studiengang, Semester,
Modul und Pruefungsleistung. Die Klassen wissen nichts von der Konsole und
nichts von der JSON-Datei. Ein- und Ausgabe uebernimmt die View, das Speichern
uebernimmt das Repository.

Aufbau des Modells:
    Studiengang
        enthaelt 0..* Semester
            enthaelt 0..* Module
                besitzt 0..1 Pruefungsleistung
"""

from __future__ import annotations


class Pruefungsleistung:
    """Eine Pruefungsleistung eines Moduls, zum Beispiel eine Klausur.

    Gespeichert werden die Art der Pruefung und die erreichte Note. Die Klasse
    entscheidet selbst, ob die Leistung bestanden ist.
    """

    # Bis zu dieser Note gilt eine Pruefungsleistung als bestanden.
    BESTEHENSGRENZE = 4.0

    def __init__(self, art: str, note: float) -> None:
        # Die Zuweisung laeuft ueber die Property-Setter, damit die
        # Pruefungen der Werte auch beim Erzeugen greifen.
        self.art = art
        self.note = note

    @property
    def art(self) -> str:
        """Art der Pruefungsleistung, zum Beispiel 'Klausur'."""
        return self._art

    @art.setter
    def art(self, art: str) -> None:
        if art is None or str(art).strip() == "":
            raise ValueError("Die Pruefungsart darf nicht leer sein.")
        self._art = str(art).strip()

    @property
    def note(self) -> float:
        """Note der Pruefungsleistung im Bereich von 1.0 bis 5.0."""
        return self._note

    @note.setter
    def note(self, note: float) -> None:
        note = float(note)
        if note < 1.0 or note > 5.0:
            raise ValueError("Die Note muss zwischen 1.0 und 5.0 liegen.")
        self._note = note

    def ist_bestanden(self) -> bool:
        """Gibt True zurueck, wenn die Note die Bestehensgrenze einhaelt."""
        return self.note <= Pruefungsleistung.BESTEHENSGRENZE


class Modul:
    """Ein Modul des Studiengangs mit Name, ECTS und optionaler Pruefung.

    Ein Modul kann bereits angelegt sein, bevor eine Pruefung geschrieben
    wurde. In diesem Fall ist die Pruefungsleistung None.
    """

    def __init__(self, name: str, ects: int,
                 pruefungsleistung: Pruefungsleistung | None = None) -> None:
        self.name = name
        self.ects = ects
        self.pruefungsleistung = pruefungsleistung

    @property
    def name(self) -> str:
        """Name des Moduls."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if name is None or str(name).strip() == "":
            raise ValueError("Der Modulname darf nicht leer sein.")
        self._name = str(name).strip()

    @property
    def ects(self) -> int:
        """ECTS-Punkte des Moduls (ganzzahlig)."""
        return self._ects

    @ects.setter
    def ects(self, ects: int) -> None:
        ects = int(ects)
        if ects <= 0:
            raise ValueError("Die ECTS eines Moduls muessen groesser als 0 sein.")
        self._ects = ects

    @property
    def pruefungsleistung(self) -> Pruefungsleistung | None:
        """Die zugehoerige Pruefungsleistung oder None."""
        return self._pruefungsleistung

    @pruefungsleistung.setter
    def pruefungsleistung(self, pruefungsleistung: Pruefungsleistung | None) -> None:
        if pruefungsleistung is not None and not isinstance(pruefungsleistung, Pruefungsleistung):
            raise ValueError("Es wird ein Objekt der Klasse Pruefungsleistung erwartet.")
        self._pruefungsleistung = pruefungsleistung

    def ist_abgeschlossen(self) -> bool:
        """Gibt True zurueck, wenn eine bestandene Pruefungsleistung vorliegt."""
        if self.pruefungsleistung is None:
            return False

        return self.pruefungsleistung.ist_bestanden()


class Semester:
    """Ein Semester, das mehrere Module buendelt."""

    def __init__(self, nummer: int) -> None:
        self.nummer = nummer
        # Die Modulliste wird nur intern gefuehrt und ueber Methoden geaendert.
        self._module: list[Modul] = []

    @property
    def nummer(self) -> int:
        """Nummer des Semesters, beginnend bei 1."""
        return self._nummer

    @nummer.setter
    def nummer(self, nummer: int) -> None:
        nummer = int(nummer)
        if nummer < 1:
            raise ValueError("Die Semesternummer muss mindestens 1 sein.")
        self._nummer = nummer

    @property
    def module(self) -> list[Modul]:
        """Alle Module des Semesters.

        Zurueckgegeben wird eine Kopie der Liste. Dadurch kann die interne
        Liste nicht versehentlich von aussen veraendert werden; Aenderungen
        laufen ueber modul_hinzufuegen() und modul_loeschen().
        """
        return list(self._module)

    def modul_hinzufuegen(self, modul: Modul) -> bool:
        """Fuegt ein Modul hinzu. False, wenn der Name schon vergeben ist."""
        if self.modul_suchen(modul.name) is not None:
            return False

        self._module.append(modul)
        return True

    def modul_suchen(self, name: str) -> Modul | None:
        """Sucht ein Modul anhand des Namens (Gross-/Kleinschreibung egal)."""
        for modul in self._module:
            if modul.name.lower() == str(name).strip().lower():
                return modul

        return None

    def modul_loeschen(self, name: str) -> bool:
        """Loescht ein Modul. False, wenn es nicht gefunden wurde."""
        modul = self.modul_suchen(name)

        if modul is None:
            return False

        self._module.remove(modul)
        return True


class Studiengang:
    """Der Studiengang als oberste Fachklasse.

    Der Studiengang buendelt die Semester und berechnet die Kennzahlen des
    Dashboards: Notendurchschnitt, bestandene ECTS und Studienfortschritt.
    """

    def __init__(self, name: str, ziel_notendurchschnitt: float,
                 gesamt_ects: int) -> None:
        self.name = name
        self.ziel_notendurchschnitt = ziel_notendurchschnitt
        self.gesamt_ects = gesamt_ects
        self._semester: list[Semester] = []

    @property
    def name(self) -> str:
        """Name des Studiengangs."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if name is None or str(name).strip() == "":
            raise ValueError("Der Name des Studiengangs darf nicht leer sein.")
        self._name = str(name).strip()

    @property
    def ziel_notendurchschnitt(self) -> float:
        """Angestrebter Notendurchschnitt, zum Beispiel 2.0."""
        return self._ziel_notendurchschnitt

    @ziel_notendurchschnitt.setter
    def ziel_notendurchschnitt(self, ziel_notendurchschnitt: float) -> None:
        ziel_notendurchschnitt = float(ziel_notendurchschnitt)
        if ziel_notendurchschnitt < 1.0 or ziel_notendurchschnitt > 4.0:
            raise ValueError("Der Ziel-Notendurchschnitt muss zwischen 1.0 und 4.0 liegen.")
        self._ziel_notendurchschnitt = ziel_notendurchschnitt

    @property
    def gesamt_ects(self) -> int:
        """Gesamtzahl der ECTS des Studiengangs (ganzzahlig, z. B. 180)."""
        return self._gesamt_ects

    @gesamt_ects.setter
    def gesamt_ects(self, gesamt_ects: int) -> None:
        gesamt_ects = int(gesamt_ects)
        if gesamt_ects <= 0:
            raise ValueError("Die Gesamt-ECTS muessen groesser als 0 sein.")
        self._gesamt_ects = gesamt_ects

    @property
    def semester(self) -> list[Semester]:
        """Alle Semester des Studiengangs (Kopie der internen Liste)."""
        return list(self._semester)

    def semester_hinzufuegen(self, semester: Semester) -> bool:
        """Fuegt ein Semester hinzu. False, wenn die Nummer schon existiert."""
        if self.semester_suchen(semester.nummer) is not None:
            return False

        self._semester.append(semester)
        # Sortierung, damit die Semester im Dashboard in der richtigen
        # Reihenfolge erscheinen.
        self._semester.sort(key=lambda vorhandenes: vorhandenes.nummer)
        return True

    def semester_suchen(self, nummer: int) -> Semester | None:
        """Sucht ein Semester anhand seiner Nummer."""
        for semester in self._semester:
            if semester.nummer == int(nummer):
                return semester

        return None

    def berechne_notendurchschnitt(self) -> float:
        """Durchschnitt aller bestandenen Pruefungsleistungen.

        Nicht bestandene Leistungen fliessen nicht in den Durchschnitt ein,
        weil sie spaeter wiederholt werden. Ohne bestandene Leistung wird 0.0
        zurueckgegeben.
        """
        noten_summe = 0.0
        anzahl_noten = 0

        for semester in self._semester:
            for modul in semester.module:
                if modul.ist_abgeschlossen():
                    noten_summe += modul.pruefungsleistung.note
                    anzahl_noten += 1

        if anzahl_noten == 0:
            return 0.0

        return noten_summe / anzahl_noten

    def berechne_bestandene_ects(self) -> int:
        """Summe der ECTS aller bestandenen Module."""
        bestandene_ects = 0

        for semester in self._semester:
            for modul in semester.module:
                if modul.ist_abgeschlossen():
                    bestandene_ects += modul.ects

        return bestandene_ects

    def berechne_studienfortschritt(self) -> float:
        """Fortschritt in Prozent: bestandene ECTS im Verhaeltnis zu allen ECTS."""
        # Die Gesamt-ECTS koennen durch die Property nicht 0 werden,
        # die Abfrage bleibt aber als Schutz vor Division durch 0 stehen.
        if self.gesamt_ects == 0:
            return 0.0

        return self.berechne_bestandene_ects() / self.gesamt_ects * 100

    def ziel_erreicht(self) -> bool:
        """Prueft, ob der aktuelle Durchschnitt das gesetzte Ziel einhaelt."""
        durchschnitt = self.berechne_notendurchschnitt()

        if durchschnitt == 0.0:
            return False

        return durchschnitt <= self.ziel_notendurchschnitt

    def zaehle_module(self) -> dict[str, int]:
        """Zaehlt die Module nach Status: bestanden, offen, nicht bestanden."""
        ergebnis = {"bestanden": 0, "offen": 0, "nicht_bestanden": 0}

        for semester in self._semester:
            for modul in semester.module:
                if modul.pruefungsleistung is None:
                    ergebnis["offen"] += 1
                elif modul.ist_abgeschlossen():
                    ergebnis["bestanden"] += 1
                else:
                    ergebnis["nicht_bestanden"] += 1

        return ergebnis
