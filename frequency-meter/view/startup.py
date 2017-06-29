#!/usr/bin/env python3
"""Application main executable, for initializing the whole program"""
# Standard libraries
import logging
import os
import sys
# Third party libraries
from PyQt4 import QtGui, QtCore
# Local libraries
from view import interface


# Create the application logger, with a previously defined configuration.
logger = logging.getLogger('view')

class AppLogHandler(logging.Handler):
    """
    Customized logging handler class, for printing on a PyQt Widget.
    """
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.widget = widget
        self.setLevel(logging.DEBUG)
        formatter = logging.Formatter(" %(asctime)s.%(msecs)03d %(levelname)8s:"
                                      " %(message)s", "%H:%M:%S")
        self.setFormatter(formatter)
        self.levelcolours = {
            logging.DEBUG: 'black',
            logging.INFO: 'blue',
            logging.WARN: 'orange',
            logging.ERROR: 'red',
        }
        parent_path = os.path.dirname(__file__)
        self.logsymbols = {
            logging.DEBUG: "{}/icons/debug.png".format(parent_path),
            logging.INFO: "{}/icons//info.png".format(parent_path),
            logging.WARN: "{}/icons//warning.png".format(parent_path),
            logging.ERROR: "{}/icons//error.png".format(parent_path),
        }

    def emit(self, record):
        """Override the logging.Handler.emit method.

        The received log message will be printed on the specified
        widget, tipically a TextBox.
        """
        new_log = self.format(record)
        self.widget.insertHtml('<img src={img} height="14" width="14"/>'
                               '<font color="{colour}">{log_msg}</font><br />'
                               .format(img=self.logsymbols[record.levelno],
                                       colour=self.levelcolours[record.levelno],
                                       log_msg=new_log))
        self.widget.moveCursor(QtGui.QTextCursor.End)


class MainWindow(QtGui.QMainWindow, interface.Ui_MainWindow):
    """
    Class for defining the behaviour of the User Interface main window.
    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.DebugButton.clicked.connect(self.debug)
        self.ErrorButton.clicked.connect(self.error)
        self.WarnButton.clicked.connect(self.warn)
        # Configure the logger, assigning an instance of AppLogHandler.
        log_handler = AppLogHandler(self.LoggerBrowser)
        # log_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(log_handler)
        logger.info("Initialized the Frequency-Metter Application")

    def debug(self):
        logger.debug("Pressed debug button")
        return

    def error(self):
        logger.error("Pressed error button")
        return

    def warn(self):
        logger.warn("Pressed error button")
        return


def run():
    # The QApplication object manages the application control flow and settings.
    app = QtGui.QApplication(sys.argv)
    # Set to a GTK allowed style in order to avoid annoying erros on Ubuntu.
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
