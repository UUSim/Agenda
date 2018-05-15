""" Data model and data store. """
import datetime
import logging

from PyQt5.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)

class Patient(QObject):
    MINNAMELENGTH = 3
    MAXNOTELENGTH = 100

    sigInfoUpdated = pyqtSignal()
    sigAppointmentsUpdated = pyqtSignal()

    def __init__(self, name=None, note=None):
        super().__init__()
        self._name = name
        self._note = note

        self._appointments = []

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

    def addAppointment(self, appointment):
        self._appointments.append(appointment)
        self.sigAppointmentsUpdated.emit()

    def removeAppointment(self, appointment):
        self._appointments.remove(appointment)
        self.sigAppointmentsUpdated.emit()

    @property
    def appointments(self):
        """ Read-only list of appointments """
        return self._appointments


class PatientStore(QObject):
    sigUpdated = pyqtSignal()

    WORKINGHOURS_START = datetime.time(13, 0)
    WORKINGHOURS_END   = datetime.time(15, 0)
    WORKINGHOURS_SLOT  = datetime.timedelta(minutes=50)

    def __init__(self):
        super().__init__()
        self._patientList = []

        self._appointmentCache = {}

        self._createSampleData()

    def _createSampleData(self):
        # Create sample data
        p1 = Patient('Jan',             'test')
        p2 = Patient('Piet',            'test2')
        p3 = Patient('K. Laas',         'test3')
        p4 = Patient('V. Olgeboekt',    'test4')
        self.addPatient(p1)
        self.addPatient(p2)
        self.addPatient(p3)
        self.addPatient(p4)

        p1.addAppointment(datetime.datetime(2018, 5, 16, 14, 0))
        p1.addAppointment(datetime.datetime(2018, 5, 17, 14, 0))
        p2.addAppointment(datetime.datetime(2018, 5, 16, 15, 0))
        p2.addAppointment(datetime.datetime(2018, 5, 17, 16, 0))
        p3.addAppointment(datetime.datetime(2018, 5, 14, 15, 0))
        p4slots = self.getDayAvailableTimeSlots(datetime.date(2018, 5, 22))

        for slot in p4slots:
            p4.addAppointment(slot)

        p3slots = self.getDayAvailableTimeSlots(datetime.date(2018, 5, 23))

        for slot in p3slots[:4]:
            p3.addAppointment(slot)


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
        patient.sigAppointmentsUpdated.connect(self._updateAppointmentCache)
        self.sigUpdated.emit()

    def getPatientNames(self):
        return sorted([patient.name for patient in self._patientList])

    def getDayAppointments(self, searchDay):
        """ Get list of appointments per day """
        assert isinstance(searchDay, datetime.date), \
            "Incorrect type: {}".format(type(searchDay))
        return sorted([appointment for appointment in self._appointmentCache \
                       if appointment.date()==searchDay])

    def getDayAvailableTimeSlots(self, searchDay):
        dayAppointments = self.getDayAppointments(searchDay)
        availableSlots = []
        slotTime = datetime.datetime.combine(searchDay, self.WORKINGHOURS_START)
        while slotTime < datetime.datetime.combine(searchDay, self.WORKINGHOURS_END):
#             print ("Search", slotTime)
            if slotTime not in dayAppointments:
#                 print ("Search found", slotTime)
                availableSlots.append(slotTime)
            slotTime += self.WORKINGHOURS_SLOT
        return availableSlots

    def _updateAppointmentCache(self):
        self._appointmentCache.clear()

        for patient in self._patientList:
            for appointment in patient.appointments:
                assert appointment not in self._appointmentCache, \
                    "Internal cache error (date '{}' booked twice? For {} and {})".format(
                        appointment, self._appointmentCache[appointment], patient)
                self._appointmentCache[appointment] = patient

#         print ("appointment cache", self._appointmentCache)
