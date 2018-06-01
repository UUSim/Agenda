#!/usr/bin/env python3
""" Entry point for Agenda application."""

import logging

from PyQt5.QtWidgets import QApplication  #pylint: disable=no-name-in-module
from PyQt5 import uic

from agenda import UIPATH
logger = logging.getLogger('agenda_app')

def main():
    """ Start the application."""

    logger.info('Starting application')
    app = QApplication([])
    mainWindow = uic.loadUi(UIPATH + "/mainwindow.ui")
#     mainWindow.tabWidget.setCurrentIndex(1)
    mainWindow.show()
    
    return app.exec_()

if __name__=='__main__':
    exit(main())
