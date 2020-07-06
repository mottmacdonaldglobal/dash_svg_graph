import os


import numpy as np  

from geomdl import NURBS, BSpline, utilities
import ezdxf
from ezdxf.addons import Importer
import ezdxf.entities as dxf 
import shapely.geometry as sg
from shapely import ops

from importer import GeometryImporter
from svg import _SvgPath 


class DxfImporter(GeometryImporter):

    def __init__(self,filename : str):
        super().__init__(filename)
        self.paths = []

    def _process_2d_polyline(self,polyline):
        svg = ''
        xy = []
        for i, location in enumerate(polyline.points()): 
            xy.append([location.x, location.y])


            if i==0:
                svg +='M {:f} {:f} '.format(location.x,location.y) 
            else:
                svg +='L {:f} {:f} '.format(location.x,location.y) 
        path = _SvgPath()
        path.d= svg
        pl = sg.LineString(xy)
        self.geometry.append(pl)
        return path    
        

    def _process_2d_spline(self,spline : dxf.Spline, delta = 0.1):
        """
        Uses geomdl module to create intermediary b-spline from dxf spline.
        This is then samples and 
        """
        svg = ''

        curve = NURBS.Curve()
        curve.degree = spline.dxf.degree
        curve.ctrlpts = spline.control_points
        
        curve.weights = [1] * spline.control_point_count()#spline.weights
        #curve.weights = spline.weights + [1] * np.array(spline.control_point_count()- len(spline.weights))
        curve.knotvector = spline.knots
 
        curve.delta = delta # TODO sampling - this could get out of hand depending on model dims and scale

        #TODO conditional delta: min length, n and check for straight lines

        xyz = np.array(curve.evalpts)
        xy = list([x[:-1] for x in xyz]) #remove z data

        pl = sg.LineString(xy)
        
        for i,p in enumerate(xy):
            if i==0:
                svg +='M {:f} {:f} '.format(p[0],p[1]) 
            else:
                svg +='L {:f} {:f} '.format(p[0],p[1]) 

        self.geometry.append(pl)
        path = _SvgPath()
        path.d= svg
        return path    

    def process(self, fillcolor = '#ff0000'):
        """
        implement superclass abstract method
        uses ezdxf to read dxf file and populate geometry
        """
        sdoc = ezdxf.readfile(self.filename)

        ents = sdoc.modelspace().query('CIRCLE LINE ARC POLYLINE ELLIPSE SPLINE SHAPE')

        for e in ents:
            path = None
            if isinstance(e, dxf.Spline) and e.dxf.flags >= ezdxf.lldxf.const.PLANAR_SPLINE:
                path = self._process_2d_spline(e)
                
            elif isinstance(e, dxf.Polyline):
                if e.get_mode() == 'AcDb2dPolyline':
                    path = self._process_2d_polyline(e)
                else:
                    pass

            if path and path.is_valid():
                self.paths.append(path)


        shapes = []
        for path in self.paths:
            shapes.append(path.to_dash_dict())

        multiline = sg.MultiLineString(self.geometry)
        merge = ops.linemerge(multiline)
        polygon = ops.polygonize_full(merge)
  
        if isinstance(merge,sg.LineString):
            svg_path = _SvgPath.from_linestring(merge)
            svg_path.fill = fillcolor
            return [svg_path.to_dash_dict()]
        return shapes

