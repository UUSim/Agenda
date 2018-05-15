""" Popup widgets """
from PyQt5.QtWidgets import QMessageBox

def popupMessageBox_(message):
    """ Pops an message box, showing the given string"""
    msg = QMessageBox()
    msg.resize(1600,100)
    msg.setWindowTitle("Error")
    msg.setText(str(message))
    msg.setStandardButtons(QMessageBox.Close)
    return msg

def popupError(message):
    """ Pops an error model dialog, showing the given string"""
    msg = popupMessageBox_(str(message))
    msg.setIcon(QMessageBox.Critical)
    return msg.exec_()

def popupWarning(message):
    """ Pops a warning model dialog, showing the given string"""
    msg = popupMessageBox_(str(message))
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Warning")
    return msg.exec_()

def popupInfo(message):
    """ Pops an info model dialog, showing the given string"""
    msg = popupMessageBox_(str(message))
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Info")
    return msg.exec_()

def popupQuestion(message):
    """ Pops a message box, with OK/Cancel buttons """
    msg = popupMessageBox_(str(message))
    msg.setWindowTitle("Are you sure?")
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    return msg.exec_()