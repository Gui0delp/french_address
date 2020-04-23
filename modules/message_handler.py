"""Manage the hangler message"""

from PyQt5.QtCore import QTime
from qgis.PyQt.QtCore import Qt

class MessageHandler:
    """This class manage the methods for messages """

    def __init__(self, dialog):

        self.dialog = dialog
        self.time = ""

    def send_logs_messages(self, message_type, message):
        """Send messages to the logs"""

        self.time = self.set_current_time()

        if message_type == 'ok':
            self.dialog.pte_logs_event.setStyleSheet('color: green')
            logs_message = "{} | {} : {}".format(self.time, 'OK', message)
        elif message_type == 'error':
            self.dialog.pte_logs_event.setStyleSheet('color: red')
            logs_message = "{} | {} : {}".format(self.time, 'ERROR', message)
        else:
            self.dialog.pte_logs_event.setStyleSheet('color: auto')
            logs_message = "{} | {} : {}".format(self.time, 'Info', message)

        return self.dialog.pte_logs_event.appendPlainText(logs_message)

    def set_current_time(self):
        """Set current time"""
        self.time = QTime.currentTime().toString(Qt.ISODate)
        return self.time
