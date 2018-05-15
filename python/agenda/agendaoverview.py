""" Widget with overview of calendar (month) and day planning side by side. """
from datetime import date

from PyQt5.QtWidgets import QListWidgetItem, QWidget
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QDate

from agenda import UIPATH
from agenda.patient import PatientStore, Patient
from agenda.misc import popupInfo

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
        if dayAppointments:
            for app in dayAppointments:
                appTime = "{:02d}:{:02d}".format(app.hour, app.minute)
                dayList += "{} - {}\n".format(
                    appTime, self.patientStore._appointmentCache[app])
        else:
            dayList += "none\n"

        self.plainTextEdit.setPlainText(dayList)
