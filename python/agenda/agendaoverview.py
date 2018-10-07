""" Widget with overview of calendar (month) and day planning side by side. """
from datetime import date, datetime

from PyQt5.QtWidgets import QWidget  #pylint: disable=no-name-in-module
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QDate  #pylint: disable=no-name-in-module

from agenda import UIPATH
from agenda.patient import PatientStore

from agenda.agendaentry import AgendaEntry
from operator import itemgetter
#from PyQt5.QtCore import QObject

class AgendaOverview(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi(UIPATH + '/AgendaOverview.ui', self)

        self.patientStore = PatientStore.Instance()
        self.day = date.today()

        self.refreshDayOverview()
        self.refreshSelectedPatientList()
        self.patientStore.sigUpdated.connect(self.refreshDayOverview)
        self.patientStore.sigUpdated.connect(self.refreshSelectedPatientList)

        # Connect ui signals
        self.calendarWidget.clicked.connect(self._selectDay)
        self.selectedPatient.currentTextChanged.connect(self._selectPatient)

    @pyqtSlot(str)
    def _selectPatient(self, selectedText):
        selectedPatient = self.patientStore.getPatient(selectedText)
        self.patientStore.activePatient = selectedPatient

    @pyqtSlot()
    def refreshSelectedPatientList(self):
        self.selectedPatient.blockSignals(True)
        self.selectedPatient.clear()
        self.selectedPatient.addItems(self.patientStore.getPatientNames())

        if self.patientStore.activePatient is not None:
            # Mark initial selection in GUI
            activePatientIndex = self.selectedPatient.findText(
                self.patientStore.activePatient.name)
            if activePatientIndex != -1:
                self.selectedPatient.setCurrentIndex(activePatientIndex)
        self.selectedPatient.blockSignals(False)

    @pyqtSlot(QDate)
    def _selectDay(self, day):
        self.day = day.toPyDate()
        self.refreshDayOverview()

    @pyqtSlot()
    def refreshDayOverview(self):
        dayAppointments = self.patientStore.getDayAppointments(self.day)
        self._clearDay()

        # Populate day overview widget with list of appointments
        daySlots = self.patientStore.getDayAvailableTimeSlots(self.day)
        daySlots = [(slot, None) for slot in daySlots]

        if dayAppointments or daySlots:
            for app, patient in sorted(dayAppointments + daySlots, key=itemgetter(0)):
                if patient:
                    appName = "{}".format(patient)
                else:
                    appName = '-- --'
                self._addEntry(app.time(), appName, patient is None)
        else:
            self._addEntry(None, 'Day not available', False)

    def _clearDay(self):
        layout = self.dayWidget.layout()

        # Clear list of old day entries
        while True:
            oldItem = layout.takeAt(0)
            if not oldItem:
                break
            oldItem.widget().setParent(None)
            del oldItem

    def _addEntry(self, time, text, bookingEnabled=True):
        layout = self.dayWidget.layout()
        entry = AgendaEntry(self.dayWidget)
        entry.setText(text)
        entry.setTime(time)
        entry.setEnableBooking(bookingEnabled)
        entry.sigBookClicked.connect(self.slotBookEntry)
        entry.sigBlockClicked.connect(self.slotBlockEntry)
        entry.sigCancelClicked.connect(self.slotCancelEntry)
        layout.addWidget(entry)

    @pyqtSlot()
    def slotBookEntry(self):
        entryTime = self.sender().time
        appointment = datetime.combine(self.day, entryTime)
        self.patientStore.addAppointment(self.patientStore.activePatient, appointment)

    @pyqtSlot()
    def slotBlockEntry(self):
        entryTime = self.sender().time
        appointment = datetime.combine(self.day, entryTime)
        self.patientStore.addAppointment(self.patientStore._patientList[0], appointment)

    @pyqtSlot()
    def slotCancelEntry(self):
        entryTime = self.sender().time
        appointment = datetime.combine(self.day, entryTime)
        self.patientStore.removeAppointment(appointment)
