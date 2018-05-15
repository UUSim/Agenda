""" Qt widget for editing patient details. """

from PyQt5.QtWidgets import QDialogButtonBox, QWidget
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from agenda import UIPATH
from agenda.misc import popupWarning, popupInfo

class PatientEditWidget(QWidget):
    sigBusy = pyqtSignal()
    sigDone = pyqtSignal()
    sigSave = pyqtSignal()

    def _disableInputFields(self):
        self._ui.name.setEnabled(False)
        self._ui.textEdit.setEnabled(False)

    def _enableInputFields(self):
        self._ui.name.setEnabled(True)
        self._ui.textEdit.setEnabled(True)
        self._ui.name.setFocus()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ui = uic.loadUi(UIPATH + '/patientedit.ui', self)


        self._ui.buttonBox.accepted.connect(self._savePatient)
        self._ui.buttonBox.rejected.connect(self._clearPatient)

        self._ui.name.textEdited.connect(self._patientNameChanged)
        self._ui.textEdit.textChanged.connect(self._patientNoteChanged)
        self._disableButtons()
        self._disableInputFields()
        self._activePatient = None

    def _disableButtons(self):
        self._ui.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
        self._ui.buttonBox.button(QDialogButtonBox.Cancel).setEnabled(False)

    def _checkButtons(self):
        save = False
        if self._ui.name.text()!=self._activePatient.name \
        or self._ui.textEdit.toPlainText()!=self._activePatient.note:
            save = True
        self._ui.buttonBox.button(QDialogButtonBox.Save).setEnabled(save)

    def openPatient(self, patient):
        self._activePatient = patient
        self._ui.name.setText(patient.name)
        self._ui.textEdit.setText(patient.note)
        self._disableButtons()
        self._ui.buttonBox.button(QDialogButtonBox.Cancel).setEnabled(True)
        self._enableInputFields()

        #TODO: Fancy up appointment list
        appListText = "Appointments:\n"
        if patient.appointments:
            appListText += "\n".join([str(app) for app in patient.appointments])
        else:
            appListText += "none"
        self.appointmentListBox.setPlainText(appListText)
        self.sigBusy.emit()

    @pyqtSlot(str)
    def _patientNameChanged(self, _):
        self._checkButtons()

    @pyqtSlot()
    def _patientNoteChanged(self):
        self._checkButtons()

    @pyqtSlot()
    def _savePatient(self):
        assert self._activePatient is not None
        try:
            self._activePatient.name = self._ui.name.text()
        except AssertionError as ex:
            popupWarning(ex)
            return
        try:
            self._activePatient.note = self._ui.textEdit.toPlainText()
        except AssertionError as ex:
            popupWarning(ex)
            return
            
        popupInfo("Patient information was updated successfully")
        self.sigSave.emit()
        self._clearPatient()
        
    def _clearPatient(self):
        self._ui.name.clear()
        self._ui.textEdit.clear()
        self.appointmentListBox.clear()
        self._activePatient = None
        self._disableButtons()
        self._disableInputFields()
        self.sigDone.emit()
