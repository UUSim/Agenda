""" Widget with overview of calendar (month) and day planning side by side. """
from datetime import date

from PyQt5.QtWidgets import QWidget  #pylint: disable=no-name-in-module
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QDate  #pylint: disable=no-name-in-module

from agenda import UIPATH
from agenda.patient import PatientStore

from agenda.agendaentry import AgendaEntry
from operator import itemgetter

class AgendaOverview(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi(UIPATH + '/AgendaOverview.ui', self)

        self.patientStore = PatientStore.Instance()

        self._selectDay(QDate.currentDate())#date.today())

        # Connect ui signals
        self.calendarWidget.clicked.connect(self._selectDay)

    @pyqtSlot(QDate)
    def _selectDay(self, day):
        day = day.toPyDate()
        dayAppointments = self.patientStore.getDayAppointments(day)

        self._clearDay()

        # Populate day overview widget with list of appointments
        daySlots = self.patientStore.getDayAvailableTimeSlots(day)
        daySlots = [(slot, None) for slot in daySlots]

        if dayAppointments or daySlots:
            for app, patient in sorted(dayAppointments + daySlots, key=itemgetter(0)):
                if patient:
                    appName = "{}".format(patient)
                else:
                    appName = '-- --'
                self._addEntry(app.time(), appName)
        else:
            self._addEntry(None, 'Day not available')

    def _clearDay(self):
        layout = self.dayWidget.layout()

        # Clear list of old day entries
        while True:
            oldItem = layout.takeAt(0)
            if not oldItem:
                break
            oldItem.widget().setParent(None)
            del oldItem

    def _addEntry(self, time, text):
        layout = self.dayWidget.layout()
        entry = AgendaEntry(self.dayWidget)
        entry.setText(text)
        entry.setTime(time)
        layout.addWidget(entry)
