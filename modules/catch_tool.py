"""Manage the tool"""
from qgis.gui import QgsMapTool
from qgis.core import Qgis, QgsMessageLog
from .coordinates import Coordinates
from .api_address import ApiAddress


class CatchTool(QgsMapTool):
    def __init__(self, iface, dialog, setting_widget, fr_address_instance):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.canvas = iface.mapCanvas()
        self.iface = iface
        self.dialog = dialog
        self.setting_widget = setting_widget
        self.fr_address_instance = fr_address_instance
        self.coord = Coordinates(self.dialog)
        self.api_address = ApiAddress(self.dialog)

    def canvasReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.coord.set_canvas_project(self.canvas)
        self.coord.set_destination_crs()
        self.coord.set_x_transform()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        self.coord.set_point_to_wgs84(point)
        self.coord.set_latitude_longitude_wgs84()
        self.api_address.set_reverse_url(self.coord.longitude, self.coord.latitude)

        if self.api_address.test_request():
            self.api_address.set_request()
            self.api_address.decode_response()
            data = self.api_address.json_to_dictionnary()
            self.fr_address_instance.data_from_api = data
            self.api_address.initialize_table_widget()
            if self.api_address.take_reverse_response_label():
                response_label = self.api_address.take_reverse_response_label()
                response_properties = self.api_address.take_reverse_response_properties()
                response_coordinates = self.api_address.take_reverse_response_coordinates()
                response_properties.update(response_coordinates)
                response = self.choose_results(response_label, response_properties)
                self.dialog.le_input_address.setText(response)
                self.api_address.populate_table_widget(response_properties)
            else:
                message = "Pas d'adresse trouvé avec ces coordonnées"
                message_error = message + f'EPSG:4326 lon,lat = {self.coord.longitude},{self.coord.latitude}'
                self.message_log(message_error)
                self.iface.messageBar().pushMessage('Warning',
                                                    message_error,
                                                    level=Qgis.Warning,
                                                    )

    def activate(self):
        message = " cliquer sur la carte pour capturer l'adresse..."
        self.iface.messageBar().pushMessage('Info',
                                            message,
                                            level=Qgis.Info,
                                            )
        self.dialog.tb_catch_tool.setChecked(True)
        self.fr_address_instance.catch_tool_activate = True

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.dialog.tb_catch_tool.setChecked(False)
        self.dialog.pb_locate_search.setEnabled(True)
        self.fr_address_instance.catch_tool_activate = False
        self.deactivated.emit()

    def choose_results(self, response_label, response_properties):
        response = response_label

        if self.setting_widget.cbox_postcode.isChecked():
            response = response + ' ' + response_properties['postcode']

        if self.setting_widget.cbox_citycode.isChecked():
            response = response + ' ' + response_properties['citycode']

        if self.setting_widget.cbox_id.isChecked():
            response = response + ' ' + response_properties['id']

        if self.setting_widget.cbox_type.isChecked():
            response = response + ' ' + response_properties['context']

        return response

    def message_log(self, msg=""):
        QgsMessageLog.logMessage('{} {}'.format(self.__class__.__name__, msg), 'FrenchAddress', Qgis.Info)
