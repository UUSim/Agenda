""" Data model and data store. """
import datetime
import logging

from PyQt5.QtCore import QObject, pyqtSignal  #pylint: disable=no-name-in-module

logger = logging.getLogger(__name__)

class Patient(QObject):
    MINNAMELENGTH = 3
    MAXNOTELENGTH = 100

    sigInfoUpdated = pyqtSignal()

    def __init__(self, name=None, note=None):
        super().__init__()
        self._name = name
        self._note = note

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert bool(value), "Name cannot be empty"
        assert isinstance(value, str), "Name must be of type str"
        #TODO: ValueErrors instead of assert?
        assert len(value) >= Patient.MINNAMELENGTH, \
            "Name must contain at least {} characters".format(Patient.MINNAMELENGTH)
        self._name = value
        self.sigInfoUpdated.emit()

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, value):
        assert isinstance(value, str), "Note must be of type str"
        assert len(value) <= Patient.MAXNOTELENGTH, \
            "Note may not be longer than {} characters".format(Patient.MAXNOTELENGTH)
        self._note = value
        self.sigInfoUpdated.emit()

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Patient: {!r}>".format(self.name)


class PatientStore(QObject):
    sigUpdated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._patientList = []

        self._appointments = {}

        # List of possible time slots which can be booked during a day
        self._daySlots = [
            datetime.time(9, 0),
            datetime.time(10, 0),
            datetime.time(11, 0),
            datetime.time(12, 0),
            datetime.time(14, 0),
            datetime.time(15, 0),
            datetime.time(16, 0),
            datetime.time(17, 0),
            ]

        # Put some fake data in for demo
        self._createSampleData() # TODO: Remove

    def _createSampleData(self):
        # Create sample data
        p0 = Patient('Reserved',        'Patient for internal use (holidays etc)')
        p1 = Patient('Jan',             'test')
        p2 = Patient('Piet',            'test2')
        p3 = Patient('K. Laas',         'test3')
        p4 = Patient('V. Olgeboekt',    'test4')
        self.addPatient(p0)
        self.addPatient(p1)
        self.addPatient(p2)
        self.addPatient(p3)
        self.addPatient(p4)

        self.addAppointment(p1, datetime.datetime(2018, 6, 13, 14, 0))
        self.addAppointment(p1, datetime.datetime(2018, 6, 14, 14, 0))
        self.addAppointment(p2, datetime.datetime(2018, 6, 13, 15, 0))
        self.addAppointment(p3, datetime.datetime(2018, 6, 14, 16, 0))
        self.addAppointment(p3, datetime.datetime(2018, 6, 11, 15, 0))

        # De,p day off
        for slot in self.getDayAvailableTimeSlots(datetime.date(2018, 6, 29)):
            self.addAppointment(p0, slot)

        p4slots = self.getDayAvailableTimeSlots(datetime.date(2018, 6, 22))
        for slot in p4slots[4:]:
            self.addAppointment(p4, slot)

        p3slots = self.getDayAvailableTimeSlots(datetime.date(2018, 6, 23))
        for slot in p3slots[:4]:
            self.addAppointment(p3, slot)


    @classmethod
    def Instance(cls):
        """ Retrieve singleton instance. """
        try:
            return cls._instance
        except AttributeError:
            # No instance created yet, create it now
            cls._instance = PatientStore()
            return cls._instance        

    def patientExists(self, patient):
        return patient in self._patientList

    def getPatient(self, name):
        return next((patient for patient in self._patientList if patient.name==name), None)

    def addPatient(self, patient):
        if patient in self._patientList:
            logger.warning('Patient added to store duplicate')
            return
        assert patient.name not in self.getPatientNames(), "Patient name must be unique"
        self._patientList.append(patient)
        patient.sigInfoUpdated.connect(self.sigUpdated)
        self.sigUpdated.emit()

    def getPatientNames(self):
        return sorted([patient.name for patient in self._patientList])

    def addAppointment(self, patient, appointment):
        assert appointment not in self._appointments.keys(), "Slot already booked"
        self._appointments[appointment] = patient
        print("added:", appointment, patient)

    def getDayAppointments(self, searchDay):
        """ Get list of appointments per day """
        assert isinstance(searchDay, datetime.date), \
            "Incorrect type: {}".format(type(searchDay))
        return sorted([(appointment, patient) for (appointment, patient) in self._appointments.items() \
                       if appointment.date()==searchDay])

    def getPatientAppointments(self, searchPatient):
        """ Read-only list of appointments """
        assert isinstance(searchPatient, Patient), \
            "Incorrect type: {}".format(type(searchPatient))
        return sorted([appointment for (appointment, patient) in self._appointments.items() \
                       if patient==searchPatient])

    def getDayAvailableTimeSlots(self, searchDay):
        # Disable scheduling appointments during weekends
        if searchDay.weekday() >= 5:
            # Skip weekends (5, 6 -> sat, sun)
            return []
        dayAppointments = [slot.time() for (slot, _) in self.getDayAppointments(searchDay)]
        availableSlots = [datetime.datetime.combine(searchDay, slot) \
                          for slot in self._daySlots if slot not in dayAppointments]
        return availableSlots
