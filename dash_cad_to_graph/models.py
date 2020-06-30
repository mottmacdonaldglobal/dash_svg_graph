import abc
from typing import List

from geometry import Geometry

class Import(abc.ABC):

    def __init__(self,filename : str):
        self.filename = filename
        self.geometry : List[Geometry] = []
    
    @abc.abstractmethod
    def process(self):
        pass

