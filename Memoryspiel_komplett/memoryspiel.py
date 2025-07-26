""" 
************************************************
Ein Memory-Spiel vollständig
************************************************
""" 
# die Module importieren
# --- Aufgabe 3: QPushButton importiert, um die "Schummeln"-Schaltfläche zu erstellen. ---
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QAbstractItemView, QTableWidgetItem, QLabel, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QTimer

import random

# die Klasse für die Spielkarten (unverändert)
class Memorykarte(QTableWidgetItem):
    def __init__(self, vorne, nummer):
        super().__init__()
        self.bild_vorne = QIcon(vorne)
        self.bild_hinten = QIcon("bilder/back.bmp")
        self.setIcon(self.bild_hinten)
        self.umgedreht = False
        self.noch_im_spiel = True
        self.bild_ID = nummer
        self.bild_pos = 0
        
    def umdrehen(self):
        if self.noch_im_spiel == True:
            if self.umgedreht == True:
                self.setIcon(self.bild_hinten)
                self.umgedreht = False
            else:
                self.setIcon(self.bild_vorne)
                self.umgedreht = True
 
    def rausnehmen(self):
        self.setIcon(QIcon("bilder/aufgedeckt.bmp"))
        self.noch_im_spiel = False
 
    def get_bild_ID(self):
        return self.bild_ID
 
    def get_bild_pos(self):
        return self.bild_pos
 
    def set_bild_pos(self, position):
        self.bild_pos = position

    def get_noch_im_spiel(self):
        return self.noch_im_spiel

    def get_umgedreht(self):
        return self.umgedreht 

# eine Klasse für das Spiel
class Memoryspiel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memoryspiel")
        # --- Aufgabe 2 & 3: Fensterhöhe angepasst, um Platz für die neuen Widgets zu schaffen. ---
        self.resize(394, 600)
        
        self.timer_umdrehen = QTimer(self)
        self.timer_umdrehen.setSingleShot(True)

        self.umgedrehte_karten = 0 
        self.spieler = 0 
        self.mensch_punkte = 0 
        self.computer_punkte = 0 
        self.gemerkte_karten = [[-1] * 21 for index in range(2)]
        self.paar = [None, None]
        self.spielstaerke = 10
       
        self.spielfeld = QTableWidget(7, 6, self)
        self.spielfeld.horizontalHeader().hide()
        self.spielfeld.verticalHeader().hide()
        self.spielfeld.setShowGrid(False)
        self.spielfeld.setSelectionMode(QTableWidget.NoSelection)
        self.spielfeld.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        zeilen = range(0, 7)
        spalten = range(0, 6)
        
        for zeile in zeilen:
            self.spielfeld.setRowHeight(zeile, 64)
        for spalte in spalten:
            self.spielfeld.setColumnWidth(spalte, 64)
            
        self.timer_umdrehen.timeout.connect(self.timer_slot)
        self.spielfeld.cellClicked.connect(self.maus_klick_slot)
        
        self.spielfeld.resize(386, 450)
        
        self.label_text_mensch =  QLabel("Mensch", self)
        self.label_text_mensch.setGeometry(10, 460, 60, 25)
        self.label_mensch =  QLabel("0", self)
        self.label_mensch.setGeometry(80, 460, 60, 25)
        self.label_text_computer =  QLabel("Computer", self)
        self.label_text_computer.setGeometry(10, 485, 60, 25)
        self.label_computer =  QLabel("0", self)
        self.label_computer.setGeometry(80, 485, 60, 25)
        
        # --- Beginn der Lösung für Aufgabe 2 ---
        # Ein neues QLabel erstellt, um den Text für den aktiven Spieler anzuzeigen.
        # Es wird unterhalb der Punkteanzeige positioniert.
        self.aktiver_spieler_label = QLabel(self)
        self.aktiver_spieler_label.setGeometry(10, 520, 200, 25)
        # --- Ende der Lösung für Aufgabe 2 ---
        
        # --- Beginn der Lösung für Aufgabe 3 ---
        # Ein QPushButton erstellt und mit der schummeln-Methode verbunden.
        self.schummel_button = QPushButton("Schummeln", self)
        self.schummel_button.setGeometry(280, 520, 100, 30)
        self.schummel_button.clicked.connect(self.schummeln)
        # Ein separater Timer für die Schummel-Funktion deklariert.
        self.timer_schummel = QTimer(self)
        self.timer_schummel.setSingleShot(True)
        self.timer_schummel.timeout.connect(self.schummel_karten_verstecken)
        # --- Ende der Lösung für Aufgabe 3 ---
        
        self.bild_namen = [
            "bilder/apfel.bmp", "bilder/birne.bmp", "bilder/blume.bmp", "bilder/blume2.bmp", "bilder/ente.bmp", 
            "bilder/fisch.bmp", "bilder/fuchs.bmp", "bilder/igel.bmp", "bilder/kaenguruh.bmp", "bilder/katze.bmp", 
            "bilder/kuh.bmp", "bilder/maus1.bmp", "bilder/maus2.bmp", "bilder/maus3.bmp", "bilder/melone.bmp", 
            "bilder/pilz.bmp", "bilder/ronny.bmp", "bilder/schmetterling.bmp", "bilder/sonne.bmp", "bilder/wolke.bmp", 
            "bilder/maus4.bmp" ]
        
        self.karten = []
        bild_zaehler = 0
        schleife = 0
        while schleife < 42:
            self.karten.append(Memorykarte(self.bild_namen[bild_zaehler], bild_zaehler))
            if (schleife + 1) % 2 == 0:
                bild_zaehler = bild_zaehler + 1
            schleife = schleife + 1    

        random.shuffle(self.karten)
        self.spielfeld.setIconSize(QSize(64, 64))       
       
        # Befüllen der Tabelle gemäß der Logik aus dem Grundgerüst (Spalte für Spalte)
        for zeile in zeilen:
            for spalte in spalten:
                karten_index = (spalte * 7) + zeile
                self.spielfeld.setItem(zeile, spalte, self.karten[karten_index])
                self.karten[karten_index].set_bild_pos(karten_index)
       
        # --- Beginn der Lösung für Aufgabe 2 ---
        # Initialer Aufruf, um den Startspieler anzuzeigen.
        self.aktiven_spieler_anzeigen()
        # --- Ende der Lösung für Aufgabe 2 ---
        self.show()
        
    def maus_klick_slot(self, row, column):
        if self.zug_erlaubt():
            # Die Index-Berechnung muss mit der Befüll-Logik übereinstimmen.
            karten_index = (column * 7) + row
            karte = self.karten[karten_index]
            if not karte.get_umgedreht() and karte.get_noch_im_spiel():
                karte.umdrehen()
                self.karte_oeffnen(karte)

    def timer_slot(self):
        self.karte_schliessen()
    
    def karte_oeffnen(self, karte):
        self.paar[self.umgedrehte_karten] = karte
        karten_id = karte.get_bild_ID()
        karten_pos = karte.get_bild_pos()
        if self.gemerkte_karten[0][karten_id] == -1:           
            self.gemerkte_karten[0][karten_id] = karten_pos
        elif self.gemerkte_karten[0][karten_id] != karten_pos:
            self.gemerkte_karten[1][karten_id] = karten_pos
        
        self.umgedrehte_karten = self.umgedrehte_karten + 1

        if self.umgedrehte_karten == 2:
            self.paar_pruefen()
            self.timer_umdrehen.start(1500)

        if self.mensch_punkte + self.computer_punkte == 21:
            self.timer_umdrehen.stop()
            
            # --- Beginn der Lösung für Aufgabe 1 ---
            # Statt einer statischen Nachricht wird hier der Gewinner ermittelt.
            nachricht = "Das Spiel ist vorbei!\n\n"
            if self.mensch_punkte > self.computer_punkte:
                nachricht += "Herzlichen Glückwunsch, Sie haben gewonnen!"
            elif self.computer_punkte > self.mensch_punkte:
                nachricht += "Der Computer hat gewonnen."
            else:
                nachricht += "Das Spiel endet unentschieden."
            
            QMessageBox.information(self, "Spielende", nachricht)
            # --- Ende der Lösung für Aufgabe 1 ---
            
            self.close()

    def paar_pruefen(self):
        if self.paar[0].get_bild_ID() == self.paar[1].get_bild_ID():
            self.paar_gefunden()
            karten_id = self.paar[0].get_bild_ID()
            self.gemerkte_karten[0][karten_id] = -2
            self.gemerkte_karten[1][karten_id] = -2
	
    def paar_gefunden(self):
        if self.spieler == 0:
            self.mensch_punkte = self.mensch_punkte + 1
            self.label_mensch.setNum(self.mensch_punkte)
        else:
            self.computer_punkte = self.computer_punkte + 1
            self.label_computer.setNum(self.computer_punkte)
	
    def karte_schliessen(self):
        raus = False
        if self.paar[0].get_bild_ID() == self.paar[1].get_bild_ID():
            self.paar[0].rausnehmen()
            self.paar[1].rausnehmen()
            raus = True
        else:
            self.paar[0].umdrehen()
            self.paar[1].umdrehen()
        
        self.umgedrehte_karten = 0
        if raus == False:
            self.spieler_wechseln()
        elif self.spieler == 1:
            QTimer.singleShot(500, self.computer_zug)
                
    def spieler_wechseln(self):
        if self.spieler == 0:
            self.spieler = 1
            QTimer.singleShot(500, self.computer_zug)
        else:
            self.spieler = 0
            
        # --- Beginn der Lösung für Aufgabe 2 ---
        # Bei jedem Spielerwechsel wird die Anzeige aktualisiert.
        self.aktiven_spieler_anzeigen()
        # --- Ende der Lösung für Aufgabe 2 ---

    # --- Beginn der Lösung für Aufgabe 2 ---
    # Diese Methode aktualisiert den Text des Labels, das den aktuellen Spieler anzeigt.
    def aktiven_spieler_anzeigen(self):
        if self.spieler == 0:
            self.aktiver_spieler_label.setText("Es zieht der Mensch")
        else:
            self.aktiver_spieler_label.setText("Der Computer zieht...")
    # --- Ende der Lösung für Aufgabe 2 ---
            
    def computer_zug(self):
        karten_zaehler = 0
        treffer = False

        if random.randint(0, 50) % self.spielstaerke == 0:
            while (karten_zaehler < 21) and (treffer == False):
                if (self.gemerkte_karten[0][karten_zaehler] >= 0) and (self.gemerkte_karten[1][karten_zaehler] >= 0):
                    pos1 = self.gemerkte_karten[0][karten_zaehler]
                    if self.karten[pos1].get_noch_im_spiel():
                        treffer = True
                        pos2 = self.gemerkte_karten[1][karten_zaehler]
                        self.karten[pos1].umdrehen()
                        self.karte_oeffnen(self.karten[pos1])
                        self.karten[pos2].umdrehen()
                        self.karte_oeffnen(self.karten[pos2])
                karten_zaehler = karten_zaehler + 1
	
        if (treffer == False):
            pos1 = -1
            while True: 
                zufall = random.randint(0, 41)
                if self.karten[zufall].get_noch_im_spiel() == True:
                    pos1 = zufall
                    self.karten[pos1].umdrehen()
                    self.karte_oeffnen(self.karten[pos1])
                    break
            
            while True:
                zufall = random.randint(0, 41)
                if self.karten[zufall].get_noch_im_spiel() == True and zufall != pos1:
                    self.karten[zufall].umdrehen()
                    self.karte_oeffnen(self.karten[zufall])
                    break

    # --- Beginn der Lösung für Aufgabe 3 ---
    # Diese Methode wird ausgeführt, wenn der "Schummeln"-Button geklickt wird.
    def schummeln(self):
        # Verhindert Schummeln, während bereits Karten aufgedeckt sind.
        if self.umgedrehte_karten > 0:
            return
            
        # Deaktiviert Button und Spielfeld, um Interaktionen zu sperren.
        self.schummel_button.setEnabled(False)
        self.spielfeld.setEnabled(False)

        # Dreht alle noch im Spiel befindlichen, verdeckten Karten um.
        for karte in self.karten:
            if karte.get_noch_im_spiel() and not karte.get_umgedreht():
                karte.umdrehen()
        
        # Startet den Timer, der die Karten nach 1.5 Sekunden wieder verdeckt.
        self.timer_schummel.start(1500)
        
    # Diese Methode wird vom Schummel-Timer aufgerufen.
    def schummel_karten_verstecken(self):
        # Dreht alle aufgedeckten Karten wieder um.
        for karte in self.karten:
            if karte.get_noch_im_spiel() and karte.get_umgedreht():
                karte.umdrehen()
        
        # Gibt Button und Spielfeld wieder für die Interaktion frei.
        self.schummel_button.setEnabled(True)
        self.spielfeld.setEnabled(True)
    # --- Ende der Lösung für Aufgabe 3 ---

    def zug_erlaubt(self):
        erlaubt = True
        if (self.spieler == 1) or (self.umgedrehte_karten == 2):
            erlaubt = False
        return erlaubt
               
# eine Instanz der Klasse QApplication erzeugen
app = QApplication([])
# eine Instanz unseres Fensters erzeugen
fenster = Memoryspiel()

# die Anwendung ausführen
app.exec_()