"""
Manage the api address
"""
import sys
import urllib.parse
import json
import ssl
from urllib.request import urlopen
from qgis.core import Qgis, QgsMessageLog
from PyQt5.Qt import QApplication, QUrl, QDesktopServices


class ApiAddress:
    """ This class manage the methods for api
        url: https://geo.api.gouv.fr/adresse
    """
    def __init__(self):
        self.zoom_to_map = 19
        self.reverse_url = "https://api-adresse.data.gouv.fr/reverse/"
        self.search_url = "https://api-adresse.data.gouv.fr/search/"
        self.map_url = "https://adresse.data.gouv.fr/base-adresse-nationale/"
        self.url = ""
        self.response = ""
        self.json_data = ""
        self.search_label = ""
        self.my_context = ssl._create_unverified_context()
        self.latitude = ""
        self.longitude = ""
        self.dictionnary_data = {}
        self.reverse_label = {}
        self.reverse_properties = {}

        self.error_message_no_address_locate = "No address found at this coordinates"
        self.error_message_no_address_found = "There is no address with this entry"
        self.error_message_connection = 'The connection failed'
        self.success_message_connection = 'Connection established'

    def set_reverse_url(self, longitude, latitude):
        """Set the reverse url with the longitude and latitude"""
        lon = str(longitude)
        lat = str(latitude)
        self.url = self.reverse_url + '?lon=' + lon + '&lat=' + lat
        return self.url

    def set_map_url(self, longitude_house, latitude_house, id_house):
        """Set the reverse url with the longitude and latitude"""
        lon = str(longitude_house)
        lat = str(latitude_house)
        id = id_house
        url_for_map = self.map_url + str(id) + '#' + str(self.zoom_to_map) + '/' + lon + '/' + lat
        return url_for_map

    def open_map_url(self, url_for_map):
        url = QUrl(url_for_map)
        QDesktopServices.openUrl(url)

    def test_request(self):
        """test if the request is OK"""
        try:
            urlopen(self.url, context=self.my_context)
            self.message_log(f'{self.success_message_connection}: {self.url}')
            return True
        except:
            self.message_log(f'{self.error_message_connection}: {self.url}')
            return False

    def set_request(self):
        """Open the url"""
        self.response = urlopen(self.url, context=self.my_context)
        return self.response

    def decode_response(self):
        """decode with the utf-8 encodage, the response"""
        self.json_data = self.response.read().decode('utf-8')
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

    def set_search_url(self, house_number, name_road, post_code):
        """Set the search url with the longitude and latitude """

        name_parse = urllib.parse.quote(name_road, safe='\'')

        self.url = self.search_url \
                                    + '?q=' + house_number \
                                    + '%20' + name_parse \
                                    + post_code \
                                    + '&type=housenumber' \
                                    + '&autocomplete=1'
        return self.url

    def take_search_response_label(self):
        """Return the label of the request"""
        try:
            self.search_label = \
            self.dictionnary_data['features'][0]['geometry']['coordinates']
        except:
            self.message_log(self.error_message_no_address_found)

        return self.search_label

    def message_log(self, msg=""):
        QgsMessageLog.logMessage('{} {}'.format(self.__class__.__name__, msg), 'FrenchAddress', Qgis.Info)
