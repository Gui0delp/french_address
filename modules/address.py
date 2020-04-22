"""
Manage the addresses
"""

import re

from .message_handler import MessageHandler

class Address:
    """This class manage the methods for coordinates """

    def __init__(self, dialog):
        self.dialog = dialog
        self.house_number = ""
        self.name_road = ""
        self.postcode = ""
        self.city = ""
        self.pattern_address = r"(?P<num>^[0-9]*)([,]*[ ]*)(?P<type>\D\S*)(?P<name>\D*)(?P<city_code>[0-9]*)([,]*[ ]*)(?P<city>\D*)"
        self.entry = ""
        self.message_handler = MessageHandler(self.dialog)

    def test_address_entry(self, entry):
        """Test the entry return True if the address format is correct"""
        
        if re.match(self.pattern_address, str(entry)) is not None:
            self.entry = entry
            flag = True
        else:
            flag = False
        return flag

    def format_address_entry(self):
        """format the address entry"""

