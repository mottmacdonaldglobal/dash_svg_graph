import random
from shapely.geometry import Point

def point_in_polygon(polygon, limit = 1000):
    """
    Find a point in a polygon
    """
    i = 0 
    minx, miny, maxx, maxy = polygon.bounds
    while i < limit:
        i +=1
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            return pnt
    return None