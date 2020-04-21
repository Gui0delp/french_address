from qgis.gui import QgsMapTool
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
)
from .coordinates import Coordinates
class PointTool(QgsMapTool):
    """Point tool"""

    def __init__(self, canvas, dialog):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.dialog = dialog
        self.latitude = 0.0
        self.longitude = 0.0
        self.coord = Coordinates(self.dialog)

    def canvasReleaseEvent(self, event):
        """Get the clic from the mouss"""
        x = event.pos().x()
        y = event.pos().y()
        self.coord.set_canvas_project(self.canvas)
        self.coord.set_destination_crs()
        xform = self.coord.set_x_transform()

        if self.dialog.cb_clic_map.isChecked():
            point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            point_wgs84 = xform.transform(point)
            self.coord.set_latitude_longitude_wgs84(point_wgs84)
