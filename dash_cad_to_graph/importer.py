"""
Generic implementation of geometry. 
"""
import abc
from typing import List,Tuple
from shapely.geometry.base import BaseGeometry

class GeometryImporter(abc.ABC):

    def __init__(self,filename : str):
        self.filename = filename
        self.geometry : List[BaseGeometry] = []
    
    @abc.abstractmethod
    def process(self, **kwargs):
        """
        Converts CAD file formats geometry to our geometry.
        """
        pass

    def bounds(self) -> Tuple[float]:
        """
        Returns, as (xmin,ymin,xmax,ymax) tuple, the bounding box which envelopes
        this importer's geometry
        """
        for g in self.geometry:
            b = g.bounds
            pass


