"""
Generic implementation of geometry. 
"""
import abc
from typing import List

class Geometry(abc.ABC):
    """
    Abstract superclass.
    """
    pass


class Point(abc.ABC):

    def __init__(self, x : float, y : float):
        self.x : float = x
        self.y : float = y



class Polyline(Geometry):
    """
    Curve from drawing straight lines through points
    """

    def __init__(self):
        self.points : List[Point] = []

    def add_point(self, p : Point):
        self.points.append(p)

