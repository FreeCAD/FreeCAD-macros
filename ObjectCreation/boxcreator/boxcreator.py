import FreeCAD as app
from FreeCAD import Vector, Rotation
import Draft
import BOPTools.JoinFeatures


def create_box(materialWidth,
               boxWidth, boxHeight, boxLength,
               notchWidth,
               drawSides=[True, True, True, True, True, True],
               overhangTop=[0.0, 0.0, 0.0, 0.0],
               overhangBottom=[0.0, 0.0, 0.0, 0.0],
               doc=None):
    """Create a box  with interlocked notches.

    Parameters
    ----------
    - drawSides: [top, bottom, left, right, front, back]
    - overhangTop: [top left, top right, top front, top back]
    - overhangBottom: [bottom left, bottom right, bottom front, bottom back]
    """

    if doc is None:
        doc = app.activeDocument()

    if doc is None:
        doc = app.newDocument()

    if doc is None:
        app.Console.PrintError('Could not get a document where to create the box')
        return

    boxobjects = []

    if drawSides[1]:
        side1 = draw_top_bottom(doc, 'bottom', materialWidth, boxWidth, boxLength, notchWidth, drawSides, overhangBottom)
        boxobjects.append(side1)

    if drawSides[0]:
        side2 = draw_top_bottom(doc, 'top', materialWidth, boxWidth, boxLength, notchWidth, drawSides, overhangTop)
        side2.Placement.Base.z += boxHeight - materialWidth
        boxobjects.append(side2)

    if drawSides[2]:
        side3 = draw_left_right(doc, 'left', materialWidth, boxHeight, boxLength, notchWidth, drawSides)
        boxobjects.append(side3)

    if drawSides[3]:
        side4 = draw_left_right(doc, 'right', materialWidth, boxHeight, boxLength, notchWidth, drawSides)
        Draft.move([side4], Vector(boxWidth - materialWidth, 0.0, 0.0), copy=False)
        boxobjects.append(side4)

    if drawSides[4]:
        side5 = draw_front_back(doc, 'front', materialWidth, boxWidth, boxHeight, notchWidth, drawSides)
        boxobjects.append(side5)

    if drawSides[5]:
        side6 = draw_front_back(doc, 'back', materialWidth, boxWidth, boxHeight, notchWidth, drawSides)
        Draft.move([side6], Vector(0.0, boxLength - materialWidth, 0.0), copy=False)
        boxobjects.append(side6)

    comp1 = doc.addObject('Part::Compound', 'Box')
    comp1.Links = boxobjects

    doc.recompute()
    return comp1


def draw_top_bottom(doc, partname, materialWidth, boxWidth, boxLength, notchWidth, drawSides=[True, True, True, True, True, True], overhang=[0.0, 0.0, 0.0, 0.0]):
    """Create the top or bottom part of the box.

    Parameters
    ----------
    - drawSides = [top, bottom, left, right, front, back]
    - overhang = [left, right, front, back]
    """
    lines = []

    if overhang[2] > 0:
        lines += _notch_holes(boxWidth, notchWidth, materialWidth, Vector(0, 0, 0), overhang[2], drawSides[4], overhang[0], overhang[1])
    else:
        lines.append(_notch_line(boxWidth, notchWidth, materialWidth, Vector(0, 0, 0), False, False, drawSides[4]))

    if overhang[1] > 0:
        lines2 = _notch_holes(boxLength, notchWidth, materialWidth, Vector(0, 0, 90), overhang[1], drawSides[3], overhang[2], overhang[2])
        for line in lines2:
            line.Placement.Base.x += boxWidth
            lines.append(line)
    else:
        lines2 = _notch_line(boxLength, notchWidth, materialWidth, Vector(0, 0, 90), False, False, drawSides[3])
        lines2.Placement.Base.x += boxWidth
        lines.append(lines2)

    if overhang[3] > 0:
        lines3 = _notch_holes(boxWidth, notchWidth, materialWidth, Vector(0, 0, 180), overhang[3], drawSides[5], overhang[1], overhang[0])
        for line in lines3:
            line.Placement.Base.x += boxWidth
            line.Placement.Base.y += boxLength
            lines.append(line)
    else:
        lines3 = _notch_line(boxWidth, notchWidth, materialWidth, Vector(0, 0, 180), False, False, drawSides[5])
        lines3.Placement.Base.x += boxWidth
        lines3.Placement.Base.y += boxLength
        lines.append(lines3)

    if overhang[0] > 0:
        lines4 = _notch_holes(boxLength, notchWidth, materialWidth, Vector(0, 0, 270), overhang[0], drawSides[2], overhang[3], overhang[3])
        for line in lines4:
            line.Placement.Base.y += boxLength
            lines.append(line)
    else:
        lines4 = _notch_line(boxLength, notchWidth, materialWidth, Vector(0, 0, 270), False, False, drawSides[2])
        lines4.Placement.Base.y += boxLength
        lines.append(lines4)

    doc.recompute()
    side1 = _extrude_lines(doc, partname, lines, materialWidth)
    return side1


def draw_left_right(doc, partname, materialWidth, boxHeight, boxLength, notchWidth, drawSides=[True, True, True, True, True, True]):
    """Create the left or right part of the box.

    Also used to create the compartment separators inside the box.

    Parameters
    ----------
    - drawSides = [top, bottom, left, right, front, back]
    """
    line1 = _notch_line(boxLength, notchWidth, materialWidth, Vector(0, 270, 90), drawSides[4], drawSides[5], drawSides[1])
    if drawSides[1]:
        line1.Placement.Base.z += materialWidth

    line2 = _notch_line(boxHeight, notchWidth, materialWidth, Vector(90, 90, 90), drawSides[1], drawSides[0], drawSides[4])
    if drawSides[4]:
        line2.Placement.Base.y += materialWidth

    line3 = _notch_line(boxLength, notchWidth, materialWidth, Vector(0, 90, 90), drawSides[4], drawSides[5], drawSides[0])
    line3.Placement.Base.z += boxHeight
    if drawSides[0]:
        line3.Placement.Base.z -= materialWidth

    line4 = _notch_line(boxHeight, notchWidth, materialWidth, Vector(90, 270, 90), drawSides[1], drawSides[0], drawSides[5])
    line4.Placement.Base.y += boxLength
    if drawSides[5]:
        line4.Placement.Base.y -= materialWidth

    lines = [line1, line2, line3, line4]

    side3 = _extrude_lines(doc, partname, lines, materialWidth)
    return side3


def draw_front_back(doc, partname, materialWidth, boxWidth, boxHeight, notchWidth, drawSides=[True, True, True, True, True, True]):
    """Create the front or back part of the box."""
    line1 = _notch_line(boxWidth, notchWidth, materialWidth, Vector(270, 0, 0), False, False, drawSides[1])
    if drawSides[1]:
        line1.Placement.Base.z += materialWidth

    line2 = _notch_line(boxHeight, notchWidth, materialWidth, Vector(90, 0, 270), drawSides[0], drawSides[1], drawSides[2])
    line2.Placement.Base.z += boxHeight

    line3 = _notch_line(boxWidth, notchWidth, materialWidth, Vector(90, 0, 0), False, False, drawSides[0])
    line3.Placement.Base.z += boxHeight
    if drawSides[0]:
        line3.Placement.Base.z -= materialWidth

    line4 = _notch_line(boxHeight, notchWidth, materialWidth, Vector(90, 0, 90), drawSides[1], drawSides[0], drawSides[3])
    line4.Placement.Base.x += boxWidth

    doc.recompute()
    lines = [line1, line2, line3, line4]

    side5 = _extrude_lines(doc, partname, lines, materialWidth)
    return side5


def _notch_line(length, notchWidth, materialWidth, rotation=Vector(0, 0, 0), insideLeft=False, insideRight=False, drawNotches=True):
    """Create the lines for the notches."""
    if not drawNotches:
        if insideLeft:  x = materialWidth
        else:           x = 0

        if insideRight: y = length - materialWidth
        else:           y = length

        points = _rotate_points([Vector(x, 0.0, 0.0),
                               Vector(y, 0.0, 0.0)],
                               rotation)

        line = Draft.makeWire(points, closed=False, face=False, support=None)
        return line

    nrNotches = int((length - 2 * materialWidth) / (notchWidth * 2))
    edgeLen = (length - (notchWidth * (nrNotches * 2 - 1))) / 2
    x = 0
    if insideLeft:
        x = materialWidth
        edgeLen -= materialWidth

    points = [Vector(x, 0, 0)]
    x += edgeLen
    for count in range(0, nrNotches):
        points.append(Vector(x, 0, 0))
        points.append(Vector(x, materialWidth, 0))
        x = x + notchWidth
        points.append(Vector(x, materialWidth, 0))
        points.append(Vector(x, 0, 0))
        x = x + notchWidth

    if insideLeft and not insideRight:
        edgeLen += materialWidth

    points.append(Vector(x - notchWidth + edgeLen, 0, 0))
    line = Draft.makeWire(_rotate_points(points, rotation), closed=False, face=False, support=None)
    Draft.autogroup(line)
    return line


def _draw_holes(length, notchWidth, materialWidth, rotation):
    """Create the lines for the notch holes in a part."""
    lines = []
    nrNotches = int((length - 2 * materialWidth) / (notchWidth * 2))
    x = (length - (notchWidth * (nrNotches * 2 - 1))) / 2
    for count in range(0, nrNotches):
        points = [Vector(x, 0, 0), Vector(x, materialWidth, 0), Vector(x + notchWidth, materialWidth, 0), Vector(x + notchWidth, 0, 0)]
        points = _rotate_points(points, rotation)
        line = Draft.makeWire(points, closed=True, face=False, support=None)
        line.Label = "hole"
        Draft.autogroup(line)
        lines.append(line)
        x = x + notchWidth * 2

    return lines


def _notch_holes(length, notchWidth, materialWidth, rotation=Vector(0, 0, 0), overhang=0, drawHoles=True, overhangLeft=0, overhangRight=0):
    lines = []

    if drawHoles:
        lines = _draw_holes(length, notchWidth, materialWidth, rotation)

    points = [Vector(-overhangLeft, 0, 0),
              Vector(-overhangLeft, -overhang, 0),
              Vector(length + overhangRight, -overhang, 0),
              Vector(length + overhangRight, 0, 0)]
    points = _rotate_points(points, rotation)
    ohline = Draft.makeWire(points, closed=False, face=False, support=None)
    lines.append(ohline)
    return lines


def _extrude_lines(doc, extrudename, lines, materialWidth):
    doc.recompute()
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


def _rotate_points(plist, axisdegree):
    """Return a list of points rotated around the origin

    The rotation is defined by three angles in degrees and the rotation order is
    z, y, x, each around the newly rotated axis.

    Parameters
    ----------
    - plist: list of Vector.
    - axisdegree: Vector with angles in deg.
    """
    newlist = []
    for v in plist:
        if axisdegree.z != 0:
            rota = Rotation(Vector(0, 0, 1), axisdegree.z)
            v = rota.multVec(v)

        if axisdegree.y != 0:
            rota = Rotation(Vector(0, 1, 0), axisdegree.y)
            v = rota.multVec(v)

        if axisdegree.x != 0:
            rota = Rotation(Vector(1, 0, 0), axisdegree.x)
            v = rota.multVec(v)

        newlist.append(v)

    return newlist


def create_compartment(box,
                       direction,
                       offset,
                       materialWidth,
                       notchWidth,
                       drawSides=[True, True, True, True, True, True],
                       boxsize=Vector(0, 0, 0)):
    try:
        doc = box[0].Document
    except (IndexError, AttributeError) as e:
        app.Console.PrintError(
            f'Could not get a document where to create the compartment: {e}')
        return

    cpos = direction * offset
    mybox = None
    if len(box) == 1 and hasattr(box[0], 'Links'):
        parts = box[0].Links
        mybox = box[0]
    elif isinstance(box, list):
        parts = box
    else:
        parts = [box]

    if boxsize == Vector(0, 0, 0):
        for side in parts:
            if hasattr(side, 'Shape'):
                bbox = side.Shape.BoundBox
                if bbox.XLength > boxsize.x: boxsize.x = bbox.XLength
                if bbox.YLength > boxsize.y: boxsize.y = bbox.YLength
                if bbox.ZLength > boxsize.z: boxsize.z = bbox.ZLength

    holes = []
    if direction == Vector(1, 0, 0):
        if boxsize.z == 0 or boxsize.y == 0:
            app.Console.PrintError("select a box first !\n")
            return
        compartment = draw_left_right(doc, 'compartmentX' + str(offset), materialWidth, boxsize.z, boxsize.y, notchWidth, drawSides)
        if drawSides[4] or drawSides[5]:
            holes += _draw_holes(boxsize.y, notchWidth, materialWidth, Vector(0, 0, 90))
        if drawSides[2] or drawSides[3]:
            holes += _draw_holes(boxsize.z, notchWidth, materialWidth, Vector(90, 0, 90))

        for h in holes:
            h.Placement.Base.x += offset + materialWidth

    elif direction == Vector(0, 1, 0):
        if boxsize.z == 0 or boxsize.x == 0:
            app.Console.PrintError("select a box first !\n")
            return

        sides = [drawSides[0], drawSides[1], drawSides[4], drawSides[5], drawSides[2], drawSides[3]]
        compartment = draw_left_right(doc, 'compartmentY' + str(offset), materialWidth, boxsize.z, boxsize.x, notchWidth, sides)
        doc.recompute()
        Draft.rotate([compartment], 270.0, Vector(0, 0, 0), axis=Vector(0.0, 0.0, 1.0), copy=False)
        doc.recompute()
        Draft.move([compartment], Vector(0, materialWidth, 0), copy=False)
        doc.recompute()
        if drawSides[0] or drawSides[1]:
            holes += _draw_holes(boxsize.x, notchWidth, materialWidth, Vector(0, 0, 0))
        if drawSides[2] or drawSides[3]:
            holes += _draw_holes(boxsize.z, notchWidth, materialWidth, Vector(0, 270, 0))

        for h in holes:
            h.Placement.Base.y += offset

    elif direction == Vector(0, 0, 1):
        if boxsize.x == 0 or boxsize.y == 0:
            app.Console.PrintError("select a box first !\n")
            return

        sides = [drawSides[2], drawSides[3], drawSides[0], drawSides[1], drawSides[4], drawSides[5]]
        compartment = draw_left_right(doc, 'compartmentZ' + str(offset), materialWidth, boxsize.x, boxsize.y, notchWidth, sides)
        doc.recompute()
        Draft.rotate([compartment], 270.0, Vector(boxsize.x, 0, 0), axis=Vector(0.0, 1.0, 0.0), copy=False)
        doc.recompute()
        Draft.move([compartment], Vector(0, 0, boxsize.x), copy=False)
        doc.recompute()
        if drawSides[0] or drawSides[1]:
            holes += _draw_holes(boxsize.x, notchWidth, materialWidth, Vector(270, 0, 0))
        if drawSides[4] or drawSides[5]:
            holes += _draw_holes(boxsize.y, notchWidth, materialWidth, Vector(0, 270, 90))

        for h in holes:
            h.Placement.Base.z += offset + materialWidth
    else:
        return None

    Draft.move([compartment], cpos, copy=False)

    doc.recompute()
    _add_lines_to_box_side(parts, holes)

    if mybox:
        parts.append(compartment)
        mybox.Links = parts
        doc.recompute()
        return mybox

    doc.recompute()
    return compartment


def _add_lines_to_box_side(box, holes):
    epsilon = 1e-7
    for side in box:
        if hasattr(side, 'Base') and hasattr(side.Base, 'Objects')and not side.Name.startswith("compartment"):
            outline = side.Base
            obox = outline.Shape.BoundBox

            for h in holes:
                h.ViewObject.hide()
                hbox = h.Shape.BoundBox
                if (hbox.XLength < epsilon and obox.XLength < epsilon) or (hbox.YLength < epsilon and obox.YLength < epsilon) or (hbox.ZLength < epsilon and obox.ZLength < epsilon):
                    outline.Objects += [h]
                    outline.Proxy.execute(outline)
