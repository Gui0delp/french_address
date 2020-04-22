"""
Manage the api address
"""
from urllib.request import urlopen
import json
from .message_handler import MessageHandler

class ApiAddress:
    """ This class manage the methods for api
        url: https://geo.api.gouv.fr/adresse
    """

    def __init__(self, dialog):
        self.dialog = dialog
        self.reverse_url = "https://api-adresse.data.gouv.fr/reverse/"
        self.search_url = "https:// api-adresse.data.gouv.fr/search/"
        self.url = ""
        self.response = ""
        self.json_data = ""
        self.dictionnary_data = ""
        self.reverse_label = ""
        self.message_handler = MessageHandler(self.dialog)

    def set_reverse_url(self, longitude, latitude):
        """Set the reverse url with the longitude and latitude"""
        lon = str(longitude)
        lat = str(latitude)
        self.url = self.reverse_url + '?lon=' + lon + '&lat=' + lat
        return self.url

    def set_reverse_request(self):
        """Open the url"""
        self.response = urlopen(self.url)
        return self.response

    def encode_response(self):
        """decode with the utf-8 encodage, the response"""
        self.json_data = self.response.read().decode('utf-8')
        return self.json_data

    def jso_to_dictionnary(self):
        """Return a dictionnaire from json"""
        self.dictionnary_data = json.loads(self.json_data)
        return self.dictionnary_data

    def take_reverse_response_label(self):
        """Return the label of the request"""
        try:
            self.reverse_label = self.dictionnary_data['features'][0]['properties']['label']
        except:
            self.message_handler.send_logs_messages('error', 'Il n\'y a pas d\'adresse à cet emplacement')

        return self.reverse_label

