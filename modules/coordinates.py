"""
Manage the coordinates
"""
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
)

class Coordinates:
    """This class manage the methods for coordinates """

    def __init__(self, dialog):
        self.dialog = dialog
        self.longitude = 0.0
        self.latitude = 0.0
        self.project_canvas = ""
        self.destinatio_crs = ""
        self.x_transform = ""

    def set_canvas_project(self, canvas):
        """Return the canvas of the project"""
        self.project_canvas = canvas.mapSettings().destinationCrs()
        return self.project_canvas

    def set_destination_crs(self):
        """Return the current crs from the project"""
        self.destinatio_crs = QgsCoordinateReferenceSystem(4326)
        return self.destinatio_crs

    def set_x_transform(self):
        """Return the x transform from two crs"""
        self.x_transform = QgsCoordinateTransform(
            self.project_canvas,
            self.destinatio_crs,
            QgsProject.instance())
        return self.x_transform

    def set_latitude_longitude_wgs84(self, point):
        """Set the latitude and the longitude coordinates"""
        self.longitude = point[0]
        self.latitude = point[1]
        message = "{} | {}".format(str(self.latitude), str(self.longitude))
        self.dialog.pte_logs_event.appendPlainText(message)
