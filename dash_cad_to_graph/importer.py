"""
Generic implementation of geometry. 
"""
import abc
from typing import List
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

