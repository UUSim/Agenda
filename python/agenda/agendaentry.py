""" Widget for displaying 1 appointment. """
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from agenda import UIPATH

class AgendaEntry(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = uic.loadUi(UIPATH + '/agendaentry.ui', self)

    def setTime(self, time):
        self.time.setText(time)

    def setText(self, text):
        self.text.setText(text)
