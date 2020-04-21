from qgis.gui import QgsMapTool

from .coordinates import Coordinates
from .message_handler import MessageHandler
class PointTool(QgsMapTool):
    """Point tool"""

    def __init__(self, canvas, dialog):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.dialog = dialog
        self.coord = Coordinates(self.dialog)
        self.message_handler = MessageHandler(self.dialog)

    def canvasReleaseEvent(self, event):
        """Get the clic from the mouss"""

        if self.dialog.cb_clic_map.isChecked():
            x = event.pos().x()
            y = event.pos().y()
            self.coord.set_canvas_project(self.canvas)
            self.coord.set_destination_crs()
            self.coord.set_x_transform()
            point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            self.coord.set_point_to_wgs84(point)
            self.coord.set_latitude_longitude_wgs84()
            message = "{} | {}".format(str(self.coord.latitude), str(self.coord.longitude))
            self.message_handler.send_logs_messages('ok', message)
