"""
Manage the api address
"""
import urllib.parse
import json
import ssl
from urllib.request import urlopen
from qgis.core import Qgis, QgsMessageLog
from qgis.PyQt.QtWidgets import QTableWidgetItem
from PyQt5.Qt import QApplication, QUrl, QDesktopServices
from qgis.PyQt.QtCore import QTranslator, QCoreApplication

from .networkaccessmanager import NetworkAccessManager, RequestsException


class ApiAddress:
    """ This class manage the methods for api
        url: https://geo.api.gouv.fr/adresse
    """
    def __init__(self, dialog=None):
        self.dialog = dialog
        self.zoom_to_map = 19
        self.REVERSE_URL = "https://api-adresse.data.gouv.fr/reverse/"
        self.SEARCH_URL = "https://api-adresse.data.gouv.fr/search/"
        self.MAP_URL = "https://adresse.data.gouv.fr/base-adresse-nationale/"
        self.USER_AGENT = b'Mozilla/5.0 QGIS LocatorFilter'
        self.headers = {b'User-Agent': self.USER_AGENT}
        self.url = ""
        self.content = ""
        self.json_data = ""
        self.search_coordinates = ""
        self.my_context = ssl._create_unverified_context()
        self.latitude = ""
        self.longitude = ""
        self.dictionnary_data = {}
        self.reverse_label = {}
        self.reverse_properties = {}
        self.reverse_coordinates = {}

        self.nam = NetworkAccessManager()

        self.error_message_no_address_locate = "Pas d'adresse trouvé avec ces coordonnées"
        self.error_message_no_address_found = "Pas d'adresse avec ces critères"
        self.error_message_connection = "La connexion a échouée"
        self.success_message_connection = "Connexion établie"

    def tr(self, message):
        return QCoreApplication.translate('FrenchAddress', message)

    def set_reverse_url(self, longitude, latitude):
        """Set the reverse url with the longitude and latitude"""
        lon = str(longitude)
        lat = str(latitude)
        self.url = self.REVERSE_URL + '?lon=' + lon + '&lat=' + lat
        return self.url

    def set_map_url(self, longitude_house, latitude_house, id_house):
        """Set the reverse url with the longitude and latitude"""
        lon = str(longitude_house)
        lat = str(latitude_house)
        id = id_house
        url_for_map = self.MAP_URL + str(id) + '#' + str(self.zoom_to_map) + '/' + lat + '/' + lon
        return url_for_map

    def open_map_url(self, url_for_map):
        url = QUrl(url_for_map)
        QDesktopServices.openUrl(url)

    def test_request(self):
        """test if the request is OK"""
        try:
            headers = {b'User-Agent': self.USER_AGENT}
            (response, content) = self.nam.request(self.url, headers=headers, blocking=True)
            #urlopen(self.url, context=self.my_context)
            self.message_log(f'{self.success_message_connection}: {self.url}')
            return True
        except:
            self.message_log(f'{self.error_message_connection}: {self.url}')
            return False

    def set_request(self):
        """Open the url"""
        headers = {b'User-Agent': self.USER_AGENT}
        (response, content) = self.nam.request(self.url, headers=headers, blocking=True)
        self.content = content
        return self.content

    def decode_response(self):
        """decode with the utf-8 encodage, the response"""
        self.json_data = self.content.decode('utf-8')
        return self.json_data

    def json_to_dictionnary(self):
        """Return a dictionnaire from json"""
        self.dictionnary_data = json.loads(self.json_data)
        return self.dictionnary_data

    def take_reverse_response_label(self):
        """Return the label of the request"""
        try:
            self.reverse_label = \
            self.dictionnary_data['features'][0]['properties']['label']
            return self.reverse_label
        except:
            self.message_log(self.error_message_no_address_locate)
            return False

    def take_reverse_response_properties(self):
        """Return the label of the request"""
        try:
            self.reverse_properties = \
            self.dictionnary_data['features'][0]['properties']
            return self.reverse_properties
        except:
            self.message_log(self.error_message_no_address_locate)
            return False

    def take_reverse_response_coordinates(self):
        """Return the label of the request"""
        try:
            self.reverse_coordinates = \
            self.dictionnary_data['features'][0]['geometry']
            return self.reverse_coordinates
        except:
            self.message_log(self.error_message_no_address_locate)
            return False

    def set_search_url(self, house_number, name_road, post_code):
        """Set the search url with the longitude and latitude """

        name_parse = urllib.parse.quote(name_road, safe='\'')

        self.url = self.SEARCH_URL \
                                    + '?q=' + house_number \
                                    + '%20' + name_parse \
                                    + post_code \
                                    + '&type=housenumber' \
                                    + '&autocomplete=1'
        return self.url

    def take_search_response_coordinates(self):
        """Return the coordinates of the request"""
        try:
            self.search_coordinates = self.dictionnary_data['features'][0]['geometry']['coordinates']
        except:
            self.message_log(self.error_message_no_address_found)

        return self.search_coordinates

    def initialize_table_widget(self):
        self.dialog.tw_details.clear()
        self.dialog.tw_details.setRowCount(0)
        self.dialog.tw_details.setColumnCount(2)
        head_attribute = self.tr("attribute")
        head_value = self.tr("value")
        self.dialog.tw_details.setHorizontalHeaderItem(0, QTableWidgetItem(head_attribute))
        self.dialog.tw_details.setHorizontalHeaderItem(1, QTableWidgetItem(head_value))

    def populate_table_widget(self, datas):
        self.dialog.tw_details.setRowCount(len(datas))

        i = 0
        for attribute, value in datas.items():
            self.dialog.tw_details.setItem(i, 0, QTableWidgetItem(str(attribute)))
            self.dialog.tw_details.setItem(i, 1, QTableWidgetItem(str(value)))
            i += 1

    def message_log(self, msg=""):
        QgsMessageLog.logMessage('{} {}'.format(self.__class__.__name__, msg), 'FrenchAddress', Qgis.Info)
