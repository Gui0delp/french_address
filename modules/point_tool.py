from qgis.gui import QgsMapTool
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
)

class PointTool(QgsMapTool):
    """Point tool"""

    def __init__(self, canvas, dialog):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.dialog = dialog
        self.latitude = 0.0
        self.longitude = 0.0

    def canvasPressEvent(self, event):
        pass

    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        """Get the clic from the mouss"""
        x = event.pos().x()
        y = event.pos().y()
        project_epsg = self.set_canvas_project(self.canvas)
        destination_epsg = self.set_destination_crs()
        xform = QgsCoordinateTransform(project_epsg, destination_epsg, QgsProject.instance())

        if self.dialog.cb_clic_map.isChecked():
            point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            point_wgs84 = xform.transform(point)
            self.set_latitude_longitude_wgs84(point_wgs84)

    def set_canvas_project(self, canvas):
        """Return the canvas of the project"""
        return canvas.mapSettings().destinationCrs()

    def set_destination_crs(self):
        """Return the current crs from the project"""
        return QgsCoordinateReferenceSystem(4326)

    def set_latitude_longitude_wgs84(self, point):
        """Set the latitude and the longitude coordinates"""
        self.longitude = point[0]
        self.latitude = point[1]
        print(self.latitude, self.longitude)

    def activate(self):
        pass

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True
