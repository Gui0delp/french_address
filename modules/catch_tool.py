"""Manage the tool"""
from qgis.gui import QgsMapTool
from qgis.core import Qgis, QgsMessageLog
from .coordinates import Coordinates
from .api_address import ApiAddress


class CatchTool(QgsMapTool):
    def __init__(self, iface, dialog, fr_ad_instance):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.canvas = iface.mapCanvas()
        self.iface = iface
        self.dialog = dialog
        self.fr_ad_instance = fr_ad_instance
        self.coord = Coordinates(self.dialog)
        self.api_address = ApiAddress()

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
            self.api_address.json_to_dictionnary()
            if self.api_address.take_reverse_response_label():
                response_label = self.api_address.take_reverse_response_label()
                self.dialog.le_input_address.setText(response_label)
            else:
                message_error = f' no address found at this coordinates EPSG:4326 lon,lat = ' \
                                f'{self.coord.longitude},{self.coord.latitude}'
                self.message_log(message_error)
                self.iface.messageBar().pushMessage('Warning',
                                                    message_error,
                                                    level=Qgis.Warning,
                                                    )

    def activate(self):
        self.iface.messageBar().pushMessage('Info',
                                            ' click on the map to capture an address...',
                                            level=Qgis.Info,
                                            )

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.dialog.tb_catch_tool.setChecked(False)
        self.dialog.pb_locate_search.setEnabled(True)
        self.fr_ad_instance.catch_tool_activate = False
        self.fr_ad_instance.tool = None
        self.deactivated.emit()

    def message_log(self, msg=""):
        QgsMessageLog.logMessage('{} {}'.format(self.__class__.__name__, msg), 'FrenchAddress', Qgis.Info)
