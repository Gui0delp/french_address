from qgis.gui import QgsMapTool

from .coordinates import Coordinates
class PointTool(QgsMapTool):
    """Point tool"""

    def __init__(self, canvas, dialog):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.dialog = dialog
        self.coord = Coordinates(self.dialog)

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
