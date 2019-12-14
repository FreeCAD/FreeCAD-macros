
import FreeCAD
from FreeCAD import Vector
import Draft
import BOPTools.JoinFeatures


#drawSides = [top, bottom, left, right, front, back]
#overhangTop = [top left, top right, top front, top back]
#overhangBottom = [bottom left, bottom right, bottom front, bottom back]
def create_box(materialWidth, 
               boxWidth, boxHeight, boxLength, 
               notchWidth, 
               drawSides=[True, True, True, True, True, True], 
               overhangTop=[0.0, 0.0, 0.0, 0.0], 
               overhangBottom=[0.0, 0.0, 0.0, 0.0],
               doc = FreeCAD.activeDocument()):
    
    boxobjects = []

    # top and bottom side
    if drawSides[1]:
        side1 = draw_bottom(doc, 'bottom', materialWidth, boxWidth, boxLength, notchWidth, drawSides, overhangBottom)
        boxobjects.append(side1)

    if drawSides[0]:
        side2 = draw_bottom(doc, 'top', materialWidth, boxWidth, boxLength, notchWidth, drawSides, overhangTop)
        Draft.move([side2], FreeCAD.Vector(0.0, 0.0, boxHeight - materialWidth), copy=False)
        boxobjects.append(side2)

    if drawSides[2]:
        side3 = draw_left(doc, 'left', materialWidth, boxHeight, boxLength, notchWidth, drawSides)
        boxobjects.append(side3)
        
    if drawSides[3]:
        side4 = draw_left(doc, 'right', materialWidth, boxHeight, boxLength, notchWidth, drawSides)
        Draft.move([side4], FreeCAD.Vector(boxWidth - materialWidth, 0.0, 0.0), copy=False)
        boxobjects.append(side4)

    if drawSides[4]:
        side5 = draw_front(doc, 'front', materialWidth, boxWidth, boxHeight, notchWidth, drawSides)
        boxobjects.append(side5)
    
    if drawSides[5]:
        side6 = draw_front(doc, 'back', materialWidth, boxWidth, boxHeight, notchWidth, drawSides)
        Draft.move([side6], FreeCAD.Vector(0.0, boxLength - materialWidth, 0.0), copy=False)
        boxobjects.append(side6)

    comp1 = doc.addObject('Part::Compound', 'Box')
    comp1.Links = boxobjects

    doc.recompute()
    return comp1


#drawSides = [top, bottom, left, right, front, back]
#overhang = [left, right, front, back]
def draw_bottom(doc, partname, materialWidth, boxWidth, boxLength, notchWidth, drawSides=[True, True, True, True, True, True], overhang=[0.0, 0.0, 0.0, 0.0]):
    lines = []

    if overhang[2] > 0:
        lines1 = notch_holes(boxWidth, notchWidth, materialWidth, overhang[2], drawSides[4], overhang[0], overhang[1])
    else:
        lines1 = [notch_line(boxWidth, notchWidth, materialWidth, False, drawSides[4])]

    lines.extend(lines1)

    if overhang[1] > 0:
        lines2 = notch_holes(boxLength, notchWidth, materialWidth, overhang[1], drawSides[3], overhang[2], overhang[3])
    else:
        lines2 = [notch_line(boxLength, notchWidth, materialWidth, False, drawSides[3])]

    Draft.rotate(lines2, 90.0, FreeCAD.Vector(0.0, 0.0, 0.0), axis=FreeCAD.Vector(0.0, 0.0, 1.0), copy=False)
    Draft.move(lines2, FreeCAD.Vector(boxWidth, 0.0, 0.0), copy=False)
    lines.extend(lines2)

    if overhang[3] > 0:
        lines3 = notch_holes(boxWidth, notchWidth, materialWidth, overhang[3], drawSides[5], overhang[1], overhang[0])
    else:
        lines3 = [notch_line(boxWidth, notchWidth, materialWidth, False, drawSides[5])]

    Draft.rotate(lines3, 180.0, FreeCAD.Vector(boxWidth / 2, 0.0, 0.0), axis=FreeCAD.Vector(0.0, 0.0, 1.0), copy=False)
    Draft.move(lines3, FreeCAD.Vector(0.0, boxLength, 0.0), copy=False)
    lines.extend(lines3)

    if overhang[0] > 0:
        lines4 = notch_holes(boxLength, notchWidth, materialWidth, overhang[0], drawSides[2], overhang[3], overhang[2])
    else:
        lines4 = [notch_line(boxLength, notchWidth, materialWidth, False, drawSides[2])]

    Draft.rotate(lines4, 270.0, FreeCAD.Vector(0.0, 0.0, 0.0), axis=FreeCAD.Vector(0.0, 0.0, 1.0), copy=False)
    Draft.move(lines4, FreeCAD.Vector(0.0, boxLength, 0.0), copy=False)
    lines.extend(lines4)

    doc.recompute()
    side1 = extrudeLines(partname, lines, materialWidth)
    return side1


def draw_left(doc, partname, materialWidth, boxHeight, boxLength, notchWidth, drawSides=[True, True, True, True, True, True]):
    line1 = notch_line(boxHeight, notchWidth, materialWidth, True, drawSides[5])
    Draft.move([line1], FreeCAD.Vector(materialWidth, boxLength - materialWidth, 0.0), copy=False)

    line2 = notch_line(boxLength, notchWidth, materialWidth, True, drawSides[1])
    Draft.rotate([line2], 90.0, FreeCAD.Vector(0.0, 0.0, 0.0), axis=FreeCAD.Vector(0.0, 0.0, 1.0), copy=False)
    Draft.move([line2], FreeCAD.Vector(materialWidth, materialWidth, 0.0), copy=False)

    line3 = notch_line(boxHeight, notchWidth, materialWidth, True, drawSides[4])
    Draft.rotate([line3], 180.0, FreeCAD.Vector(0.0, 0.0, 0.0), axis=FreeCAD.Vector(0.0, 0.0, 1.0), copy=False)
    Draft.move([line3], FreeCAD.Vector(boxHeight - materialWidth, materialWidth, 0.0), copy=False)

    line4 = notch_line(boxLength, notchWidth, materialWidth, True, drawSides[0])
    Draft.rotate([line4], 270.0, FreeCAD.Vector(0.0, 0.0, 0.0), axis=FreeCAD.Vector(0.0, 0.0, 1.0), copy=False)
    Draft.move([line4], FreeCAD.Vector(boxHeight - materialWidth, boxLength - materialWidth, 0.0), copy=False)

    Draft.rotate([line1, line2, line3, line4], 270.0, FreeCAD.Vector(0.0, 0.0, 0.0), axis=FreeCAD.Vector(0.0, 1.0, 0.0), copy=False)
    doc.recompute()
    
    lines = [line1, line2, line3, line4]

    side3 = extrudeLines(partname, lines, materialWidth)
    return side3


def draw_front(doc, partname, materialWidth, boxWidth, boxHeight, notchWidth, drawSides=[True, True, True, True, True, True]):
    line1 = notch_line(boxWidth, notchWidth, materialWidth, False, drawSides[0])
    Draft.move([line1], FreeCAD.Vector(0.0, boxHeight - materialWidth, 0.0), copy=False)

    line2 = notch_line(boxHeight, notchWidth, materialWidth, True, drawSides[3])
    Draft.rotate([line2], 90.0, FreeCAD.Vector(0.0, 0.0, 0.0), axis=FreeCAD.Vector(0.0, 0.0, 1.0), copy=False)
    Draft.move([line2], FreeCAD.Vector(boxWidth, materialWidth, 0.0), copy=False)

    line3 = notch_line(boxWidth, notchWidth, materialWidth, False, drawSides[1])
    Draft.rotate([line3], 180.0, FreeCAD.Vector(0.0, 0.0, 0.0), axis=FreeCAD.Vector(0.0, 0.0, 1.0), copy=False)
    Draft.move([line3], FreeCAD.Vector(boxWidth, materialWidth, 0.0), copy=False)

    line4 = notch_line(boxHeight, notchWidth, materialWidth, True, drawSides[2])
    Draft.rotate([line4], 270.0, FreeCAD.Vector(0.0, 0.0, 0.0), axis=FreeCAD.Vector(0.0, 0.0, 1.0), copy=False)
    Draft.move([line4], FreeCAD.Vector(0.0, boxHeight - materialWidth, 0.0), copy=False)

    Draft.rotate([line1, line2, line3, line4], 90.0, FreeCAD.Vector(0.0, 0.0, 0.0), axis=FreeCAD.Vector(1.0, 0.0, 0.0), copy=False)

    doc.recompute()
    lines = [line1, line2, line3, line4]

    side5 = extrudeLines(partname, lines, materialWidth)
    return side5


def notch_line(length, notchWidth, materialWidth, inside=False, drawNotches=True):
    doc = FreeCAD.activeDocument()
    if not drawNotches:
        if inside:
            len2 = length - 2 * materialWidth
        else:
            len2 = length

        points = [FreeCAD.Vector(0.0, 0.0, 0.0),
                  FreeCAD.Vector(len2, 0.0, 0.0)]
        line = Draft.makeWire(points, closed=False, face=False, support=None)
        doc.recompute()
        return line

    nrNotches = int((length - 2 * materialWidth) / (notchWidth * 2))
    edgeLen = (length - (notchWidth * (nrNotches * 2 - 1))) / 2
    if inside:
        edgeLen = edgeLen - materialWidth

    points = [FreeCAD.Vector(0, 0, 0)]
    x = edgeLen

    for count in range(0, nrNotches):
        points.append(FreeCAD.Vector(x, 0, 0))
        points.append(FreeCAD.Vector(x, materialWidth, 0))
        x = x + notchWidth
        points.append(FreeCAD.Vector(x, materialWidth, 0))
        points.append(FreeCAD.Vector(x, 0, 0))
        x = x + notchWidth

    points.append(FreeCAD.Vector(x - notchWidth + edgeLen, 0, 0))
    line = Draft.makeWire(points, closed=False, face=False, support=None)
    Draft.autogroup(line)
    doc.recompute()
    return line


def notch_holes(length, notchWidth, materialWidth, overhang, drawHoles=True, overhangLeft=0, overhangRight=0):
    nrNotches = int((length - 2 * materialWidth) / (notchWidth * 2))
    x = (length - (notchWidth * (nrNotches * 2 - 1))) / 2
    lines = []

    if drawHoles:
        for count in range(0, nrNotches):
            points = [FreeCAD.Vector(x, 0, 0), FreeCAD.Vector(x, materialWidth, 0), FreeCAD.Vector(x + notchWidth, materialWidth, 0), FreeCAD.Vector(x + notchWidth, 0, 0)]
            line = Draft.makeWire(points, closed=True, face=False, support=None)
            Draft.autogroup(line)
            lines.append(line)
            x = x + notchWidth * 2

    points = [FreeCAD.Vector(-overhangLeft, 0, 0),
              FreeCAD.Vector(-overhangLeft, -overhang, 0),
              FreeCAD.Vector(length + overhangRight, -overhang, 0),
              FreeCAD.Vector(length + overhangRight, 0, 0)]
    ohline = Draft.makeWire(points, closed=False, face=False, support=None)
    lines.append(ohline)
    doc = FreeCAD.activeDocument()
    doc.recompute()
    return lines


def extrudeLines(extrudename, lines, materialWidth):
    doc = FreeCAD.activeDocument()

    j = BOPTools.JoinFeatures.makeConnect(name='Outline')
    j.Objects = lines
    j.Proxy.execute(j)
    j.purgeTouched()
    for obj in j.ViewObject.Proxy.claimChildren():
        obj.ViewObject.hide()

    f = doc.addObject('Part::Extrusion', extrudename)
    f.Base = j
    f.DirMode = 'Normal'
    f.DirLink = None
    f.LengthFwd = materialWidth
    f.LengthRev = 0
    f.Solid = True
    f.Reversed = False
    f.Symmetric = False
    f.TaperAngle = 0
    f.TaperAngleRev = 0
    f.Base.ViewObject.hide()
    return f


def create_compartment(box, 
                       direction, 
                       offset, 
                       materialWidth, 
                       notchWidth, 
                       drawSides=[True, True, True, True, True, True],
                       doc = FreeCAD.activeDocument()):
    
    cpos = direction * offset
    mybox = None
    if len(box) == 1 and hasattr(box[0], 'Links'):
        parts = box[0].Links
        mybox = box[0]
    elif isinstance(box, list):
        parts = box
    else:
        parts = [box]
        
    boxsize = Vector(0, 0, 0)
    for side in parts:
        if hasattr(side, 'Shape'):
            bbox = side.Shape.BoundBox
            if bbox.XLength > boxsize.x: boxsize.x = bbox.XLength
            if bbox.YLength > boxsize.y: boxsize.y = bbox.YLength
            if bbox.ZLength > boxsize.z: boxsize.z = bbox.ZLength
            
    if direction == Vector(1, 0, 0):
        compartment = draw_left(doc, 'compartmentX', materialWidth, boxsize.z, boxsize.y, notchWidth, drawSides)
    elif direction == Vector(0, 1, 0):
        compartment = draw_front(doc, 'compartmentY', materialWidth, boxsize.x, boxsize.z, notchWidth, drawSides)
    elif direction == Vector(0, 0, 1):
        compartment = draw_bottom(doc, 'compartmentZ', materialWidth, boxsize.x, boxsize.y, notchWidth, drawSides)
    else:
        return None
    
    Draft.move([compartment], cpos, copy=False)
            
    if mybox:
        compartment.adjustRelativeLinks(mybox)
        mybox.ViewObject.dropObject(compartment,None,'',[])
        doc.recompute()
        return mybox
    
    doc.recompute()
    return compartment
