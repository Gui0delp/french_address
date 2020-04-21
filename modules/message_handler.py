from PyQt5.QtCore import QTime
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt

class MessageHandler:
    """This class manage the methods for messages """

    def __init__(self, dialog):
  
        self.dialog = dialog
        self.time = ""

    def send_logs_messages(self, message_type, message):
        """Send messages to the logs"""

        self.time = self.set_current_time()

        if message_type == 'ok':
            logs_message = "{} | {} : {}".format(self.time, 'OK', message)
        elif message_type == 'error':
            logs_message = "{} | {} : {}".format(self.time, 'ERROR', message)
        else:
            logs_message = "{} | {} : {}".format(self.time, 'Info', message)

        return self.dialog.pte_logs_event.appendPlainText(logs_message)

    def set_current_time(self):
        """Set current time"""
        self.time = QTime.currentTime().toString(Qt.ISODate)
        return self.time
