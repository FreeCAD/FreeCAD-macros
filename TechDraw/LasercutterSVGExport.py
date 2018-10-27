# -*- coding: utf-8 -*-

import FreeCAD
import FreeCADGui
import Part
import TechDraw
import math
from operator import itemgetter, attrgetter
from FreeCAD import Base

# creates contourlines for all selected objects to a TechDraw page
def selected_to_techdraw(cutterDiameter):
    doc = FreeCAD.ActiveDocument
    selection = FreeCADGui.Selection.getSelection() 

    # get existing Techdraw page 'LaserCutterExport' or create a new one 
    techdraw = doc.getObject('LaserCutterExport')
    if techdraw == None:
        techdraw = doc.addObject('TechDraw::DrawPage','LaserCutterExport')
        template = doc.addObject('TechDraw::DrawSVGTemplate','Template')
        techdraw.Template = template

    # make a folder for some objects we will create
    group = doc.getObject('LaserCutterExportObjects')
    if group == None:
        group = doc.addObject("App::DocumentObjectGroup","LaserCutterExportObjects")

    x = float(techdraw.Template.Width) + cutterDiameter

    for sel in selection:
        # create a contour line object for every selected object        
        offset = doc.addObject("Part::Offset", sel.Label + "_offset")
        offset.Source = sel
        offset.Value = cutterDiameter / 2
        offset.Mode = 0
        offset.Join = 2
        offset.Intersection = False
        offset.SelfIntersection = False
        offset.ViewObject.Visibility=False

        # rotate biggest face into xy-plane
        group.addObject(offset)
        doc.recompute()
        rotate_biggest_face_up(offset)
        doc.recompute()
        bbox = offset.Shape.BoundBox

        # add a 2D view to the TechDraw page right of the last part
        maxheight = bbox.YLength + 4 * cutterDiameter
        if maxheight > techdraw.Template.Height:
            techdraw.Template.Height = maxheight

        techdraw.Template.Width = x + bbox.XLength + cutterDiameter

        view = doc.addObject('TechDraw::DrawViewPart', sel.Label + "_contour")
        view.CoarseView = True
        view.ViewObject.LineWidth = cutterDiameter
        view.Source = offset
        view.Direction = FreeCAD.Vector(0, 0, 1)
        techdraw.addView(view)
        doc.recompute()
        view.X = x + bbox.XLength / 2 - bbox.Center.x
        view.Y = bbox.YLength + (bbox.YLength / 2 - bbox.Center.y) + cutterDiameter
        view.ScaleType = u"Custom"
        view.Scale = 1.00
        x = x + bbox.XLength + cutterDiameter

    doc.recompute()

# rotate biggest face into xy-plane
def rotate_biggest_face_up(part_feature):
    normal_face_prop = biggest_area_faces(part_feature.Shape)
    normal_ref = normal_face_prop[0]
    rotation_to_apply = FreeCAD.Rotation(normal_ref, FreeCAD.Vector(0, 0, 1))
    new_rotation = rotation_to_apply.multiply(part_feature.Placement.Rotation)
    part_feature.Placement.Rotation = new_rotation


def biggest_area_faces(freecad_shape):
    sorted_list = sort_area_shape_faces(freecad_shape)
    biggest_area_face = sorted_list[-1]
#       contains : 0:normal, 1:area mm2, 2; list of faces
    return biggest_area_face


#   Returns face grouping by normal,sorted by the amount of surface (descending)
def sort_area_shape_faces(shape):
    return sort_area_face_common(shape.Faces, compare_freecad_vector_direction)


def sort_area_shape_list(faces_list):
    return sort_area_face_common(faces_list, compare_freecad_vector)


def compare_freecad_vector_direction(vector1, vector2, epsilon=10e-6):
    return math.fabs(vector1.cross(vector2).Length) < epsilon


def get_local_axis_normalized(face):
    x_local, y_local_not_normalized, z_local_not_normalized = get_local_axis(face)
    y_local_not_normalized.normalize()
    z_local_not_normalized.normalize()
    return x_local, y_local_not_normalized, z_local_not_normalized


def compare_freecad_vector(vector1, vector2, epsilon=10e-6):
    vector = vector1.sub(vector2)
    if math.fabs(vector.x) < epsilon and math.fabs(vector.y) < epsilon and math.fabs(vector.z) < epsilon:
        return True
    return False


def compare_value(value1, value2, epsilon=10e-6):
    value = value1 - value2
    if math.fabs(value) < epsilon:
        return True
    return False


def sort_area_face_common(faces, test_function=compare_freecad_vector_direction):
    normal_area_list = []
    for face in faces:
        # print face
        normal = face.normalAt(0, 0)
        # print normal
        found = False
        for i in range(len(normal_area_list)):
            normal_test = normal_area_list[i][0]
            if test_function(normal, normal_test):
                found = True
                normal_area_list[i][1] += face.Area
                normal_area_list[i][2].append(face)
                tmp = sorted(normal_area_list[i][2], key=attrgetter('Area'),  reverse=True)
                normal_area_list[i][2] = tmp
                break
        if not found:
            normal_area_list.append([normal, face.Area, [face]])
    # print normal_area_list
    sorted_list = sorted(normal_area_list, key=itemgetter(1))
    return sorted_list


selected_to_techdraw(1)
