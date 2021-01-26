"""
Manage the addresses
"""

import re
from qgis.core import Qgis, QgsMessageLog


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

    def test_address_entry(self, entry):
        """Test the entry return True if the address format is correct"""

        if re.match(self.pattern_address, str(entry)) is not None:
            self.address_entry = entry
            self.entry = re.match(self.pattern_address, str(entry))
            flag = True
        else:
            self.message_log('Le format de l\'adresse n\'est pas respecté \n \
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
            self.message_log('Il faut un numéro de rue \n \
                exemple: 20 Avenue de Ségur 75007')

        if not self.name_road:
            test = False
            self.message_log('Il manques un nom de rue \n \
                exemple: 20 Avenue de Ségur 75007')

        if not self.postcode:
            test = False
            self.message_log('Il manques le code postal \n \
                exemple: 20 Avenue de Ségur 75007')

        if test:
            self.message_log(f'L\'adresse {self.address_entry}, est complète')

        return test

    def message_log(self, msg=""):
        QgsMessageLog.logMessage('{} {}'.format(self.__class__.__name__, msg), 'FrenchAddress', Qgis.Info)