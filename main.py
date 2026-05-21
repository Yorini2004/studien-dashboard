
"""Studien-Dashboard:

Dieses Programm ist ein Dashboard für einen Studienfortschritt.
Es zeigt den Notendurchschnitt, ECTS-Fortschritt und gespeicherte Module an.
Aufbau:
    Studiengang
        enthält mehrere Semester
            enthält mehrere Module
                enthält eine Prüfungsleistung"""

import json
import os

#Fachklasse
class Pruefungsleistung:
    def __init__(self, art, note):
        self.art = art
        self.note = note

    @property
    def art(self):
        return self._art

    @art.setter
    def art(self, art):
        self._art = art

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, note):
        self._note = note

    def ist_bestanden(self):
        return self.note <= 4.0  #Vergleich (True oder False)

    def als_dict(self):
        return {
            "art": self.art,
            "note": self.note
        }

    @classmethod
    def aus_dict(cls, daten):
        return cls(daten["art"], daten["note"])

    def __str__(self):
        status = "bestanden" if self.ist_bestanden() else "nicht bestanden"
        return f"Prüfungsart: {self.art} | Note: {self.note} -> {status}"

#Fachklasse
class Modul:
    def __init__(self, name, ects, pruefungsleistung=None):
        self.name = name
        self.ects = ects
        self.pruefungsleistung = pruefungsleistung

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def ects(self):
        return self._ects

    @ects.setter
    def ects(self, ects):
        self._ects = ects

    @property
    def pruefungsleistung(self):
        return self._pruefungsleistung

    @pruefungsleistung.setter
    def pruefungsleistung(self, pruefungsleistung):
        self._pruefungsleistung = pruefungsleistung

    def ist_abgeschlossen(self):
        if self.pruefungsleistung is None:
            return False

        return self.pruefungsleistung.ist_bestanden()

    def als_dict(self):
        if self.pruefungsleistung is None:
            pruefungsleistung_daten = None
        else:
            pruefungsleistung_daten = self.pruefungsleistung.als_dict()

        return {
            "name": self.name,
            "ects": self.ects,
            "pruefungsleistung": pruefungsleistung_daten
        }

    @classmethod
    def aus_dict(cls, daten):
        if daten["pruefungsleistung"] is None:
            pruefungsleistung = None
        else:
            pruefungsleistung = Pruefungsleistung.aus_dict(daten["pruefungsleistung"])

        return cls(daten["name"], daten["ects"], pruefungsleistung)

    def __str__(self):
        if self.pruefungsleistung is None:
            return f"Modul: {self.name} | {self.ects} ECTS | noch keine Prüfungsleistung"

        return f"Modul: {self.name} | {self.ects} ECTS | {self.pruefungsleistung}"

#Fachklasse
class Semester:
    def __init__(self, nummer):
        self.nummer = nummer
        self.module = []

    @property
    def nummer(self):
        return self._nummer

    @nummer.setter
    def nummer(self, nummer):
        self._nummer = nummer

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, module):
        self._module = module

    def modul_hinzufuegen(self, modul):
        self.module.append(modul)

    def modul_suchen(self, name):
        for modul in self.module:
            if modul.name == name:
                return modul

        return None

    def modul_loeschen(self, name):
        modul = self.modul_suchen(name)

        if modul is None:
            return False

        self.module.remove(modul)
        return True

    def zeige_modul(self):
        print(f"Semester: {self.nummer}")
        for modul in self.module:
            print(modul)

    def als_dict(self):
        module_liste= []
        for modul in self.module:
            module_liste.append(modul.als_dict())

        return {
            "nummer": self.nummer,
            "module": module_liste
        }

    @classmethod
    def aus_dict(cls, daten):
        semester = cls(daten["nummer"])

        for modul_daten in daten["module"]:
            modul = Modul.aus_dict(modul_daten)
            semester.modul_hinzufuegen(modul)

        return semester

#Fachklasse
class Studiengang:
    def __init__(self, name, ziel_notendurchschnitt):
        self.name = name
        self.ziel_notendurchschnitt = ziel_notendurchschnitt
        self.semester = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def ziel_notendurchschnitt(self):
        return self._ziel_notendurchschnitt

    @ziel_notendurchschnitt.setter
    def ziel_notendurchschnitt(self, ziel_notendurchschnitt):
        self._ziel_notendurchschnitt = ziel_notendurchschnitt

    def semester_hinzufuegen(self, semester):
        self.semester.append(semester)

    def semester_suchen(self, nummer):
        for semester in self.semester:
            if semester.nummer == nummer:
                return semester

        return None

    def als_dict(self):
        semester_liste = []

        for semester in self.semester:
            semester_liste.append(semester.als_dict())

        return {
            "name": self.name,
            "ziel_notendurchschnitt": self.ziel_notendurchschnitt,
            "semester": semester_liste
        }

    @classmethod
    def aus_dict(cls, daten):
        studiengang = cls(daten["name"], daten["ziel_notendurchschnitt"])

        for semester_daten in daten["semester"]:
            semester = Semester.aus_dict(semester_daten)
            studiengang.semester_hinzufuegen(semester)

        return studiengang

    def zeige_uebersicht(self):
        print(f"Studiengang: {self.name}")
        print(f"Ziel-Notendurchschnitt: {self.ziel_notendurchschnitt}")
        print(f"Aktueller Notendurchschnitt: {self.berechne_notendurchschnitt():.2f}")
        print(f"Bestandene ECTS: {self.berechne_bestandene_ects()}")
        print(f"Gesamte ECTS: {self.berechne_gesamte_ects()}")
        print(f"Studienfortschritt: {self.berechne_studienfortschritt():.2f} %")
        print()

        for semester in self.semester:
            semester.zeige_modul()
            print()

    def __str__(self):
        return f"Studiengang: {self.name}"

    def berechne_notendurchschnitt(self):
        noten_summe = 0
        anzahl_noten = 0
        #Es zählen nur bestandene Pruefungsleistungen.
        for semester in self.semester:
            for modul in semester.module:
                if modul.ist_abgeschlossen():
                    noten_summe += modul.pruefungsleistung.note
                    anzahl_noten += 1
        if anzahl_noten == 0:
            return 0

        return noten_summe / anzahl_noten

    def berechne_gesamte_ects(self):
        gesamte_ects = 0
        for semester in self.semester:
            for modul in semester.module:
                gesamte_ects += modul.ects
        return gesamte_ects

    def berechne_bestandene_ects(self):
        bestandene_ects = 0
        for semester in self.semester:
            for modul in semester.module:
                if modul.ist_abgeschlossen():
                    bestandene_ects += modul.ects
        return bestandene_ects

    def berechne_studienfortschritt(self):
        #Schutz vor Division durch 0, falls noch keine Module vorhanden sind.
        gesamte_ects = self.berechne_gesamte_ects()
        if gesamte_ects == 0:
            return 0
        return self.berechne_bestandene_ects() / gesamte_ects * 100

#Funktionen zum Speichern und Laden
def speichere_studiengang(studiengang, dateiname):
    datei = open(dateiname, "w", encoding="utf-8")
    #Vor dem Speichern werden die Objekte in Dictionaries umgewandelt.
    json.dump(studiengang.als_dict(), datei, indent=4, ensure_ascii=False)
    datei.close()

def lade_studiengang(dateiname):
    #Aus den geladenen Dictionaries werden wieder Objekte erzeugt.
    datei = open(dateiname, "r", encoding="utf-8")
    daten = json.load(datei)
    datei.close()

    return Studiengang.aus_dict(daten)

def erstelle_beispieldaten():
    pruefung1 = Pruefungsleistung("Portfolio", 1.7)
    modul1 = Modul("OOP", 5.0, pruefung1)

    pruefung2 = Pruefungsleistung("Klausur", 2.3)
    modul2 = Modul("Mathematik", 5.0, pruefung2)

    pruefung3 = Pruefungsleistung("Vortrag", 5.0)
    modul3 = Modul("Ethik", 5.0, pruefung3)

    semester1 = Semester(1)
    semester1.modul_hinzufuegen(modul1)
    semester1.modul_hinzufuegen(modul2)
    semester1.modul_hinzufuegen(modul3)

    studiengang = Studiengang("Artificial Intelligence", 2.0)
    studiengang.semester_hinzufuegen(semester1)

    return studiengang

#Konsolenmenü
def zeige_menue():
    print()
    print("===== Studien-Dashboard =====")
    print("1 - Übersicht anzeigen")
    print("2 - Daten speichern")
    print("3 - Daten laden")
    print("4 - Semester hinzufügen")
    print("5 - Modul hinzufügen")
    print("6 - Prüfungsleistung hinzufügen")
    print("7 - Modul löschen")
    print("0 - Programm beenden")

def semester_hinzufuegen_menue(studiengang):
    nummer = int(input("Nummer des neuen Semesters: "))

    if studiengang.semester_suchen(nummer) is not None:
        print("Dieses Semester existiert bereits.")
    else:
        neues_semester = Semester(nummer)
        studiengang.semester_hinzufuegen(neues_semester)
        print(f"Semester {nummer} wurde hinzugefügt.")

def modul_hinzufuegen_menue(studiengang):
    semester_nummer = int(input("Zu welchem Semester soll das Modul hinzugefügt werden? "))
    semester = studiengang.semester_suchen(semester_nummer)

    if semester is None:
        print("Dieses Semester existiert nicht.")
        return

    name = input("Name des Moduls: ")
    ects = float(input("ECTS des Moduls: "))

    neues_modul = Modul(name, ects)
    semester.modul_hinzufuegen(neues_modul)

    print(f"Modul {name} wurde zu Semester {semester_nummer} hinzugefügt.")

def pruefungsleistung_hinzufuegen_menue(studiengang):
    semester_nummer = int(input("In welchem Semester liegt das Modul? "))
    semester = studiengang.semester_suchen(semester_nummer)

    if semester is None:
        print("Dieses Semester existiert nicht.")
        return

    modul_name = input("Name des Moduls: ")
    modul = semester.modul_suchen(modul_name)

    if modul is None:
        print("Dieses Modul existiert in diesem Semester nicht.")
        return

    art = input("Art der Prüfungsleistung: ")
    note = float(input("Note: "))

    pruefungsleistung = Pruefungsleistung(art, note)
    modul.pruefungsleistung = pruefungsleistung

    print(f"Prüfungsleistung für {modul.name} wurde hinzugefügt.")

def modul_loeschen_menue(studiengang):
    semester_nummer = int(input("Aus welchem Semester soll das Modul gelöscht werden? "))
    semester = studiengang.semester_suchen(semester_nummer)

    if semester is None:
        print("Dieses Semester existiert nicht.")
        return

    modul_name = input("Name des Moduls: ")

    wurde_geloescht = semester.modul_loeschen(modul_name)

    if wurde_geloescht:
        print(f"Modul {modul_name} wurde gelöscht.")
    else:
        print("Dieses Modul wurde nicht gefunden.")

#Programmstart
def main():
    dateiname = "studiengang.json"

    if os.path.exists(dateiname):
        studiengang = lade_studiengang(dateiname)
    else:
        studiengang = erstelle_beispieldaten()

    while True:
        zeige_menue()
        auswahl = input("Bitte Auswahl eingeben: ")

        if auswahl == "1":
            studiengang.zeige_uebersicht()

        elif auswahl == "2":
            speichere_studiengang(studiengang, dateiname)
            print("Daten wurden gespeichert.")

        elif auswahl == "3":
            studiengang = lade_studiengang(dateiname)
            print("Daten wurden geladen.")

        elif auswahl == "4":
            semester_hinzufuegen_menue(studiengang)

        elif auswahl == "5":
            modul_hinzufuegen_menue(studiengang)

        elif auswahl == "6":
            pruefungsleistung_hinzufuegen_menue(studiengang)

        elif auswahl == "7":
            modul_loeschen_menue(studiengang)

        elif auswahl == "0":
            print("Programm wird beendet.")
            break

        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()




