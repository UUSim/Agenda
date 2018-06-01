""" Overview widget with list of patients. """

from PyQt5.QtWidgets import QListWidgetItem, QWidget  #pylint: disable=no-name-in-module
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot  #pylint: disable=no-name-in-module

from agenda import UIPATH
from agenda.patient import PatientStore, Patient
from agenda.misc import popupInfo

class PatientOverview(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi(UIPATH + '/PatientOverview.ui', self)

        self.patientStore = PatientStore.Instance()
        self.activePatient = None

        self.updatePatientList()

        # Connect ui signals
        self.ui.listWidget.currentItemChanged.connect(self.selectPatient)
        self.ui.pushButton.clicked.connect(self.newPatient)
        self.patientStore.sigUpdated.connect(self.updatePatientList)

        self.patientEditWidget.sigBusy.connect(self._disableNewButton)
        self.patientEditWidget.sigDone.connect(self._enableNewButton)

    @pyqtSlot()
    def _disableNewButton(self):
        self.ui.pushButton.setEnabled(False)
        self.ui.listWidget.setEnabled(False)

    @pyqtSlot()
    def _enableNewButton(self):
        self.ui.pushButton.setEnabled(True)
        self.ui.listWidget.setEnabled(True)

    @pyqtSlot()
    def newPatient(self):
        self.activePatient = Patient()
        self.ui.patientEditWidget.openPatient(self.activePatient)
        self.ui.patientEditWidget.sigSave.connect(self.saveNewPatient)

    @pyqtSlot()
    def saveNewPatient(self):
        self.patientStore.addPatient(self.activePatient)
        popupInfo("New patient '{}' was saved".format(self.activePatient))
        self.ui.patientEditWidget.sigSave.disconnect(self.saveNewPatient)

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def selectPatient(self, item, _):
        if item is not None: # In case list is cleared no patient is selected
            selectedPatient = self.patientStore.getPatient(item.text())
            self.ui.patientEditWidget.openPatient(selectedPatient)

    @pyqtSlot()
    def updatePatientList(self):
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(self.patientStore.getPatientNames())
