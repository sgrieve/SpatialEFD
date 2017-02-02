import math
import shapefile as shp


def FixAngle(angle):
    '''
    Takes angle in radians and if it is less than 0 adds 2pi to keep the values
    between 0 and 2pi
    '''
    if (angle < 0.):
        angle += math.pi * 2.
    return angle


def AngleBetween(start_pt, end_pt):
    '''
    Gets the angle between 2 points given as tuples, converts this angle to an
    angle from north 0 (or 2pi) rather than east, and returns the eventual value
    as an angle in degrees between 0 and 360
    '''
    dx = end_pt[0] - start_pt[0]
    dy = end_pt[1] - start_pt[1]

    East_Angle = FixAngle(math.atan2(dy, dx))

    return math.degrees(FixAngle((math.pi / 2.) - East_Angle))


def downslope_orientation(filename, ID):

    sf = shp.Reader(filename)

    for shaperec in sf.shapeRecords():
        if shaperec.record[1] == ID:
            top = shaperec.shape.points[-1]
            bottom = shaperec.shape.points[0]
            return AngleBetween(top, bottom)

    print 'problem', ID
    return 0.0


def rotatePoint(centerPoint, point, angle):
    """
    Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise
    https://gist.github.com/somada141/d81a05f172bb2df26a2c
    """
    angle = math.radians(angle)
    temp_point = point[0] - centerPoint[0], point[1] - centerPoint[1]
    temp_point = (temp_point[0] * math.cos(angle) - temp_point[1] *
                  math.sin(angle), temp_point[0] * math.sin(angle) +
                  temp_point[1] * math.cos(angle))

    temp_point = temp_point[0] + centerPoint[0], temp_point[1] + centerPoint[1]
    return temp_point[0], temp_point[1]


def getBBox(x, y):
    xmin = min(x)
    ymin = min(y)

    xmax = max(x)
    ymax = max(y)

    return xmax - xmin, ymax - ymin, xmin, ymin
