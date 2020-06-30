import os


import ezdxf
from ezdxf.addons import Importer
import ezdxf.entities as dxf 

from models import Import
import geometry as g

class DxfImport(Import):

    def __init__(self,filename : str):
        super().__init__(filename)

    def _process_2d_polyline(self,polyline):
        pl = g.Polyline()
        for i, location in enumerate(polyline.points()):
            p = g.Point(location.x, location.y)
            pl.add_point(p)

    def _process_2d_spline(self,spline : dxf.Spline):
        #print (spline.dxf.flags) 
        pass

    def process(self):
        """
        implement superclass abstract method
        uses ezdxf to read dxf file and populate geometry
        """
        sdoc = ezdxf.readfile(self.filename)
        tdoc = ezdxf.new()

        importer = Importer(sdoc, tdoc)

        # import all geometry entities from source modelspace into an arbitrary target layout.
        # create target layout
        tblock = tdoc.blocks.new('SOURCE_ENTS')

        ents = sdoc.modelspace().query('CIRCLE LINE ARC POLYLINE ELLIPSE SPLINE SHAPE')

        for e in ents:
            if isinstance(e, dxf.Spline) and e.dxf.flags >= ezdxf.lldxf.const.PLANAR_SPLINE:
                self._process_2d_spline(e)
            elif isinstance(e, dxf.Polyline):
                if e.get_mode() == 'AcDb2dPolyline':
                    self._process_2d_polyline(e)
                else:
                    pass


        # import source entities into target block
        importer.import_entities(ents, tblock)

