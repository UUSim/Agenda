""" Widget for displaying 1 appointment. """

import datetime
from PyQt5           import uic
from PyQt5.QtCore    import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QMenu, QAction

from agenda import UIPATH

class AgendaEntry(QWidget):
    sigBookClicked   = pyqtSignal()
    sigBlockClicked  = pyqtSignal()
    sigCancelClicked = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = uic.loadUi(UIPATH + '/agendaentry.ui', self)
        self.bookButton.clicked.connect(self.sigBookClicked)

        self.time = None
        self.entryMenu = QMenu()
        self.actionCancel = self.entryMenu.addAction("Cancel booking...")
        self.actionCancel.triggered.connect(self.slotCancelClicked)

        self.actionBlock  = self.entryMenu.addAction("Block...")
        self.actionBlock.triggered.connect(self.sigBlockClicked)
        self.optionsButton.setMenu(self.entryMenu)

    @pyqtSlot()
    def slotCancelClicked(self):
        print("Cancel clicked") # TODO: Confirm cancellation
        self.sigCancelClicked.emit()

    def setTime(self, entryTime):
        assert isinstance(entryTime, (type(None), datetime.time)), \
            "Incorrect type: {}".format(type(entryTime))
        self.time = entryTime
        if self.time is not None:
            self.timeLabel.setText("{:02d}:{:02d}".format(self.time.hour, self.time.minute))
        else:
            self.timeLabel.setText('--:--')

    def setText(self, text):
        self.textLabel.setText(text)

    def setEnableBooking(self, enabled):
        self.bookButton.setEnabled(enabled)
        self.actionCancel.setEnabled(not enabled and self.time is not None) # cancel appointment is inverse
        self.actionBlock.setEnabled(enabled) # reserve follows enabled
