from typing import Dict, List

import plotly.graph_objects as go 

import cad_to_shapely

import shapely.geometry as sgeo
from shapely import ops


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
        self.fillrule = 'evenodd'

    def is_valid(self):
        return self.d is not None

    def to_dash_dict(self):
        return dict (
            type = 'path',
            path = self.d,
            line_color = 'Black', 
            fillcolor = self.fill,
            fillrule = self.fillrule
        )


    @classmethod
    def from_shapely_geometry(cls, geometry : sgeo.base.BaseGeometry, settings : Dict[str,object] = None):
        """
        Converts shapely geometry (linestringto SVG path. 
        Shapely can produce SVG output using linestring._repr_svg_() but it
        produces an SVG XML using polygon, not (more generic) 'path'

        TODO add points, circles, rectangles
        """
        c = cls()
        c.d = ''
        if isinstance(geometry,sgeo.LineString) or isinstance(geometry,sgeo.LinearRing):
            for i,p in enumerate(geometry.coords):
                if i==0:
                    c.d +='M {:f} {:f} '.format(p[0],p[1]) 
                else:
                    c.d +='L {:f} {:f} '.format(p[0],p[1]) 
            if geometry.is_closed:
                c.d += 'Z'
                c.fill = '#000000'
        elif isinstance(geometry,sgeo.Polygon):  
        
            #TODO polygons - holes and fill
            c.fillrule = 'evenodd'
            c.fill = 'Red'
            for i,p in enumerate(geometry.exterior.coords):
                if i==0:
                    c.d +='M {:f} {:f} '.format(p[0],p[1]) 
                else:
                    c.d +='L {:f} {:f} '.format(p[0],p[1]) 

            c.d += 'Z  '
            for hole in geometry.interiors:
                for i, p in enumerate(hole.coords):
                    if i==0:
                        c.d +='M {:f} {:f} '.format(p[0],p[1]) 
                    else:
                        c.d +='L {:f} {:f} '.format(p[0],p[1]) 
                c.d += 'Z  '

        return c


class CadGeometry():

    def __init__(self, file : str):

        self.file = file
        self.importer = cad_to_shapely.dxf.DxfImporter(file) 


    def load(self):
        self.importer.process()
        self.importer.cleanup()

        
    @property
    def bounds(self) -> tuple:
        """
        Bounding box for imported cad geometry

        Returns:
            minimum bounding region (minx, miny, maxx, maxy)

        """
        
        multiline = sgeo.MultiLineString(self.importer.geometry)
        merge = ops.linemerge(multiline)

        return merge.bounds


    def add_to_figure(self, fig :go.Figure, use_clean :bool = False, single_closed_polygon :bool= False) -> go.Figure:
        """
        Will add (svg path) shapes to passed plotly.graph_objects.Figure
        This populated Figure is returned. 

        args:
            use_clean: use the cleaned geometry - polygons
            single_closed_polygon: special use case.
        """
        shapes = []

        if not single_closed_polygon:
            if not use_clean:
                geometry = self.importer.geometry
            else:
                geometry = self.importer.polygons
                
            for g in geometry:
                p = _SvgPath.from_shapely_geometry(g)
                shapes.append(p.to_dash_dict())

        else: # single_closed_polygon true
            polygon = cad_to_shapely.utils.find_holes(self.importer.polygons)
            p = _SvgPath.from_shapely_geometry(polygon)
            shapes.append(p.to_dash_dict())


        # Add shapes
        fig.update_layout(
            shapes=shapes
        )

        return fig

    
    def set_figure_to_bounds(self, fig : go.Figure) -> go.Figure:

        xmin,ymin,xmax,ymax = self.bounds
        # Update axes properties
        fig.update_xaxes(
            range=[xmin, xmax],
            zeroline=False,
        )

        fig.update_yaxes(
            range=[ymin, ymax],
            zeroline=False,
        )

        return fig