"""
Manage the coordinates
"""
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsRectangle,
)


class Coordinates:
    """This class manage the methods for coordinates"""

    def __init__(self, dialog):
        self.dialog = dialog
        self.longitude = 0.0
        self.latitude = 0.0
        self.deci_latitude = 0.0
        self.deci_longitude = 0.0
        self.scale = 0.0003
        self.project_canvas = ""
        self.destination_crs = ""
        self.x_transform = ""
        self.x_transform_reverse = ""
        self.epsg_project = ""
        self.point_wgs84 = []
        self.point_crs = []

    def set_canvas_project(self, canvas):
        """Return the canvas of the project"""
        self.project_canvas = canvas.mapSettings().destinationCrs()
        return self.project_canvas

    def set_destination_crs(self):
        """Return the wgs84 crs"""
        self.destination_crs = QgsCoordinateReferenceSystem(4326)
        return self.destination_crs

    def set_x_transform(self):
        """Return the x transform from two crs"""
        self.x_transform = QgsCoordinateTransform(
            self.project_canvas,
            self.destination_crs,
            QgsProject.instance())
        return self.x_transform

    def set_x_transform_reverse(self):
        """Return the x transform from two crs"""
        self.x_transform_reverse = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem(4326),
            QgsCoordinateReferenceSystem(self.epsg_project),
            QgsProject.instance())
        return self.x_transform_reverse

    def set_latitude_longitude_wgs84(self):
        """Set the latitude and the longitude coordinates"""
        self.longitude = self.point_wgs84[0]
        self.latitude = self.point_wgs84[1]

    def set_latitude_longitude_crs(self, point):
        """Set the latitude and the longitude coordinates"""
        self.longitude = point[0]
        self.latitude = point[1]

    def set_point_to_wgs84(self, point):
        """Transform the crs point to the wgs84 crs"""
        self.point_wgs84 = self.x_transform.transform(point)
        return self.point_wgs84

    def set_point_to_crs_project(self, point):
        """Transform the crs point to the wgs84 crs"""
        self.point_crs = self.x_transform_reverse.transform(point)
        return self.point_crs

    def zoom_to_canvas(self, canvas):
        """The function permit to zoom on the canvas.
        """
        rectangle = self.x_transform_reverse.transform(QgsRectangle(
            self.longitude - self.scale,
            self.latitude - self.scale,
            self.longitude + self.scale,
            self.latitude + self.scale,
        ))
        canvas.setExtent(rectangle)
        canvas.refresh()

    def take_crs_from_project(self, iface):
        """Take the EPSG from the project
        Returns:
            [object]
        """
        self.epsg_project = iface \
            .mapCanvas()\
            .mapSettings()\
            .destinationCrs()\
            .authid()
        return self.epsg_project
