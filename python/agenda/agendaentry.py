""" Widget for displaying 1 appointment. """

import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from agenda import UIPATH

class AgendaEntry(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = uic.loadUi(UIPATH + '/agendaentry.ui', self)

    def setTime(self, entryTime):
        if entryTime is not None:
            assert isinstance(entryTime, datetime.time), "Incorrect type: {}".format(type(entryTime))
            self.time.setText("{:02d}:{:02d}".format(entryTime.hour, entryTime.minute))
        else:
            self.time.setText('--:--')

    def setText(self, text):
        self.text.setText(text)
