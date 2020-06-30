
import xml.etree.ElementTree as ET
import os
import gzip
import shutil
from typing import List,Dict

import plotly.graph_objects as go


class _SvgPath():
    """
    Generic SVGpath. Geometry defined by attribute 'd'
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d

    MoveTo: M, m
    LineTo: L, l, H, h, V, v
    Cubic Bézier Curve: C, c, S, s
    Quadratic Bézier Curve: Q, q, T, t
    Elliptical Arc Curve: A, a
    ClosePath: Z, z

    Note: 
    Commands are case-sensitive. An upper-case command specifies absolute coordinates,
    while a lower-case command specifies coordinates relative to the current position
    """

    def __init__(self):
        self.d = None
        self.stroke = '#000000'
        self.fill = None

    def is_valid(self):
        return self.d is not None

    def to_dash_dict(self):
        return dict (
            type = 'path',
            path = self.d,
            line_color = 'Black', 
            fillcolor = self.fill
        )


class GraphSvg():

    def __init__(self, filepath :str):
        self.filepath = filepath
        self.paths = []


    def traces_from_svg_file(self, origin = None, flip_x = False, flip_y = False) -> List[Dict]:
        """
        returns plotly shapes as array of dicts
        use '

        """

        # unzip .svgz file into .svg
        if isinstance(self.filepath, str) and os.path.splitext(self.filepath[1].lower() == ".svgz"):
            with gzip.open(self.filepath, 'rb') as f_in, open(self.filepath[:-1], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            self.filepath = self.filepath[:-1]
    
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        for child in root:
            if child.tag.endswith('path'):
                path = _SvgPath()
                if 'd' in child.attrib:
                    #Note: 
                    # Commands are case-sensitive. An upper-case command specifies absolute coordinates, 
                    # while a lower-case command specifies coordinates relative to the current position
                    path.d = child.attrib['d']
                if 'stroke' in child.attrib:
                    path.stroke = child.attrib['stroke']           
                if 'fill' in child.attrib:
                    path.fill =  child.attrib['fill']
                if 'stroke-width' in child.attrib:
                    path.stroke_width = child.attrib['stroke-width']
                
                if path.is_valid():
                    self.paths.append(path)


        shapes = []
        for path in self.paths:
            shapes.append(path.to_dash_dict())

        print (shapes)
        return shapes




    