from qgis.gui import QgsMapTool

from .coordinates import Coordinates
from .message_handler import MessageHandler
from .api_address import ApiAddress
class PointTool(QgsMapTool):
    """Point tool"""

    def __init__(self, canvas, dialog):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
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
            self.api_address.set_reverse_url(self.coord.longitude, self.coord.latitude)
            if self.api_address.test_reverse_request():
                self.api_address.set_reverse_request()
                self.api_address.encode_response()
                self.api_address.jso_to_dictionnary()
                response = self.api_address.take_reverse_response_label()
                self.dialog.le_input_address.setText(response)
