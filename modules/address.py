"""
Manage the addresses
"""

import re

from .message_handler import MessageHandler

class Address:
    """This class manage the methods for coordinates"""

    def __init__(self, dialog):
        self.dialog = dialog
        self.house_number = ""
        self.name_road = ""
        self.postcode = ""
        self.city = ""
        self.pattern_address = r"(?P<num>^[0-9]*)([,]*[ ]*)(?P<name>\D*)(?P<city_code>[0-9]*)([,]*[ ]*)(?P<city>\D*)"
        self.address_entry = ""
        self.entry = ""
        self.message_handler = MessageHandler(self.dialog)

    def test_address_entry(self, entry):
        """Test the entry return True if the address format is correct"""

        if re.match(self.pattern_address, str(entry)) is not None:
            self.address_entry = entry
            self.entry = re.match(self.pattern_address, str(entry))
            flag = True
        else:
            self.message_handler.send_logs_messages(
                'error', 'Le format de l\'adresse n\'est pas respecté \n \
                exemple: 20 Avenue de Ségur 75007 Paris')
            flag = False
        return flag

    def format_address_entry(self):
        """format the address entry"""

        self.house_number = str(self.entry.group('num'))
        self.name_road = str(self.entry.group('name'))
        self.postcode = str(self.entry.group('city_code'))
        self.city = str(self.entry.group('city'))

    def test_obligatory_field(self):
        """test the presence of the obligatory field"""

        test = True

        if not self.house_number:
            test = False
            self.message_handler.send_logs_messages(
                'error',
                'Il faut un numéro de rue \n \
                exemple: 20 Avenue de Ségur 75007')

        if not self.name_road:
            test = False
            self.message_handler.send_logs_messages(
                'error',
                'Il manques un nom de rue \n \
                exemple: 20 Avenue de Ségur 75007')

        if not self.postcode:
            test = False
            self.message_handler.send_logs_messages(
                'error',
                'Il manques le code postal \n \
                exemple: 20 Avenue de Ségur 75007')

        if test:
            self.message_handler.send_logs_messages('ok',\
                f'L\'adresse {self.address_entry}, est complète')

        return test
