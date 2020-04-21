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
        self.point_wgs84 = []
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

    def set_latitude_longitude_wgs84(self):
        """Set the latitude and the longitude coordinates"""
        self.longitude = self.point_wgs84[0]
        self.latitude = self.point_wgs84[1]

    def set_point_to_wgs84(self, point):
        """Transform the crs point to the wgs84 crs"""
        self.point_wgs84 = self.x_transform.transform(point)
        return self.point_wgs84
