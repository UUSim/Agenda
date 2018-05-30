""" Widget with overview of calendar (month) and day planning side by side. """
from datetime import date

from PyQt5.QtWidgets import QListWidgetItem, QWidget
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QDate

from agenda import UIPATH
from agenda.patient import PatientStore, Patient
from agenda.misc import popupInfo

from agenda.agendaentry import AgendaEntry

class AgendaOverview(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi(UIPATH + '/AgendaOverview.ui', self)

        self.patientStore = PatientStore.Instance()

        self._selectDay(QDate.currentDate())#date.today())

        # Connect ui signals
        self.calendarWidget.clicked.connect(self._selectDay)

    @pyqtSlot(QDate)
    def _selectDay(self, date):
        day = date.toPyDate()
        print(date, day)
        dayAppointments = self.patientStore.getDayAppointments(day)

        weekendString = '' if day.weekday() <= 4 else ' (weekend)'
        dayList = "Appointments on {}{}:\n".format(day, weekendString)

        self._clearDay()

        if dayAppointments:
            for app in dayAppointments:
                appTime = "{:02d}:{:02d}".format(app.hour, app.minute)
                appName = "{}".format(self.patientStore._appointmentCache[app])
                dayList += "{} - {}\n".format(
                    appTime, appName)
                self._addEntry(appTime, appName)
        else:
            self._addEntry('--:--', 'No appointments')

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
