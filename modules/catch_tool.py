"""Manage the tool"""
from qgis.gui import QgsMapTool
from qgis.core import Qgis
from qgis.PyQt.QtCore import Qt
from .coordinates import Coordinates
from .message_handler import MessageHandler
from .api_address import ApiAddress


class PointTool(QgsMapTool):
    """Point tool"""

    def __init__(self, iface, dialog):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.canvas = iface.mapCanvas()
        self.iface = iface
        self.dialog = dialog
        self.coord = Coordinates(self.dialog)
        self.message_handler = MessageHandler(self.dialog)
        self.api_address = ApiAddress(self.dialog)

    def canvasReleaseEvent(self, event):
        """Get the clic from the mouss"""
        response = ""

        if self.dialog.cb_clic_map.isChecked():
            x = event.pos().x()
            y = event.pos().y()
            self.coord.set_canvas_project(self.canvas)
            self.coord.set_destination_crs()
            self.coord.set_x_transform()
            point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            self.coord.set_point_to_wgs84(point)
            self.coord.set_latitude_longitude_wgs84()
            self.api_address.set_reverse_url(
                self.coord.longitude,
                self.coord.latitude,
                )

            if self.api_address.test_request():
                self.api_address.set_request()
                self.api_address.encode_response()
                self.api_address.jso_to_dictionnary()
                response = self.api_address.take_reverse_response_label()
                self.dialog.le_input_address.setText(response)

    def activate(self):
        self.iface.messageBar().pushMessage('Info',
                                            'Click on the map to start capture...',
                                            level=Qgis.Info,
                                            )
        self.canvas.setCursor(Qt.CrossCursor)

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()