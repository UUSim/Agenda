""" QCalendarWidget-based month calendar with marked cells """

from PyQt5.QtWidgets import QCalendarWidget  #pylint: disable=no-name-in-module
from PyQt5.QtGui import QColor, QPalette  #pylint: disable=no-name-in-module

from agenda.patient import PatientStore

# from agenda import UIPATH

class AppointmentsCalendarWidget(QCalendarWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#         self._ui = uic.loadUi(UIPATH + '/agenda.ui', self)

        self.colorBooked = QColor(self.palette().color(QPalette.Window))
        self.colorPartiallyBooked = QColor(self.palette().color(QPalette.Base))
        self.colorFree = QColor(self.palette().color(QPalette.Highlight))

        self.colorBooked.setAlpha(250)
        self.colorPartiallyBooked.setAlpha(150)
        self.colorFree.setAlpha(150)

    def paintCell(self, painter, rect, date):
        """ Add marker """
        super().paintCell(painter, rect, date)

        #highlight a particular date
        searchDay    = date.toPyDate()
        patientStore = PatientStore.Instance()
        dayAppointments   = patientStore.getDayAppointments(searchDay)
        dayAvailableSlots = patientStore.getDayAvailableTimeSlots(searchDay)

        # print ("Appointments for {}: {}".format(date, dayAppointments))
        # print("slots ({}): {}".format(searchDay, dayAvailableSlots))

        if searchDay.weekday() >= 5:
            # Skip weekends (5, 6 -> sat, sun)
            return
        if not dayAvailableSlots:
            # Fully booked
            painter.fillRect(rect, self.colorBooked)
        elif dayAppointments:
            # Partially booked
            painter.fillRect(rect, self.colorPartiallyBooked)
        else:
            # Fully available
            painter.fillRect(rect, self.colorFree)
 
