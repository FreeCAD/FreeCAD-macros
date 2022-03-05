# -*- coding: utf-8 -*-

# compatible to Python 3

import os
import FreeCAD as app
import FreeCADGui as gui
from FreeCAD import Vector, Rotation
import Part
import math


iconPath = os.path.dirname(__file__)

epsilon = 1e-7      
        
class LasercutterTechdrawExportItem:
    def __init__(self, 
                 fp,    # an instance of Part::FeaturePython
                 Part = None,
                 BeamWidth = 0.2,
                 Normal = Vector(0, 0, 0),
                 method = 'auto'):
        self.updating = False
        fp.addProperty('App::PropertyLink', 'Part',  'LasercutterTechdrawExport',  'Selected part').Part = Part
        fp.addProperty('App::PropertyVector', 'Normal', 'LasercutterTechdrawExport',  'vertical vector. (0, 0, 0) = rotate the part that it fits best').Normal = Normal
        fp.addProperty('App::PropertyFloat', 'BeamWidth', 'LasercutterTechdrawExport',  'Laser beam width in mm').BeamWidth = BeamWidth
        fp.addProperty('App::PropertyEnumeration', 'Method', 'LasercutterTechdrawExport',  'How to create the outline').Method = ['auto', '2D', '3D', 'face', 'normal']
        fp.Method = method
        fp.Proxy = self
    
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        if fp.Part and fp.Normal and (not self.updating):
            self.make_outline(fp)
        
    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        props = ['Part', 'BeamWidth', 'Normal', 'Method']
        if prop in props:
            self.execute(fp)         
            
    def make_outline(self, fp): 
        self.updating = True 
        
        if fp.Method == 'normal': 
            outline = fp.Part.Shape.makeOffsetShape(fp.BeamWidth / 2, 1e-7)
        elif fp.Method == '2D':
            outline = fp.Part.Shape.makeOffset2D(fp.BeamWidth / 2) 
            fp.Normal = self.getNormal(fp.Part) 
        elif fp.Method == '3D':
            outline = fp.Part.Shape.makeOffsetShape(fp.BeamWidth / 2, 1e-7)
            fp.Normal = self.getNormal(fp.Part) 
        else:
            face = self.get_biggest_face(fp.Part)
            if face:
                outline = face.makeOffset2D(fp.BeamWidth / 2)
                fp.Normal = face.normalAt(0, 0)
            elif fp.Method == 'auto':
                try:
                    outline = fp.Part.Shape.makeOffset2D(fp.BeamWidth / 2) 
                except Exception as ex:
                    outline = fp.Part.Shape.makeOffsetShape(fp.BeamWidth / 2, 1e-7)   
                    
                fp.Normal = self.getNormal(fp.Part)   
            
        fp.Shape = Part.Compound(outline.Wires);
        fp.Label = fp.Part.Label + ' offset'
        fp.Placement = outline.Placement
        
        if fp.Placement.Rotation.Axis.z < 0:
            fp.Placement.Rotation.Axis = fp.Placement.Rotation.Axis * -1
        
        if fp.Method != 'normal':      
            if fp.Normal.z < 0:
                fp.Normal = fp.Normal * -1
                
            rotation_to_apply = Rotation(fp.Normal, Vector(0, 0, 1))    
            new_rotation = rotation_to_apply.multiply(fp.Placement.Rotation)
            fp.Placement.Rotation = new_rotation
        
            self.rotate_biggest_side_up(fp)
            
        self.updating = False
        
    def get_biggest_face(self, part):
        max_area = 0
        max_face = None
        for face in part.Shape.Faces:
            if face and face.Area > max_area:
                max_area = face.Area
                max_face = face
    
        if max_face:
            return max_face
        
    def rotate_biggest_side_up(self, fp):
        bbox = fp.Shape.optimalBoundingBox()
        xmin = bbox.XLength
        angle = 0.0
        r = fp.Placement.Rotation
        r_best = r
        step = 180 / 16
        while angle + step < 180:   
            angle = angle + step 
            rotation_to_apply = Rotation()
            rotation_to_apply.Axis = Vector(0, 0, 1)             
            rotation_to_apply.Angle = math.radians(angle)              
            fp.Placement.Rotation = rotation_to_apply.multiply(r)
            bbox = fp.Shape.optimalBoundingBox()
    
            if xmin > bbox.XLength:
                xmin = bbox.XLength
                r_best = fp.Placement.Rotation
                 
        fp.Placement.Rotation = r_best
        
    def getNormal(self, obj):
        if hasattr(obj, 'Dir'):
            return obj.Dir
        else:
            bbox = obj.Shape.BoundBox
            if bbox.XLength < epsilon: return Vector(1.0,0.0,0.0)
            elif bbox.YLength < epsilon: return Vector(0.0,1.0,0.0)
            elif bbox.ZLength < epsilon: return Vector(0.0,0.0,1.0)
            return obj.Placement.Rotation.multVec(Vector(0, 0, 1))


class LasercutterTechdrawExportItemViewProvider:
    def __init__(self, vobj):
        '''Set this object to the proxy object of the actual view provider'''
        vobj.Proxy = self
        self.Object = vobj.Object
            
    def getIcon(self):
        '''Return the icon which will FreeCADear in the tree view. This method is optional and if not defined a default icon is shown.'''
        return (os.path.join(iconPath, 'LasercutterTechdrawExport.svg'))

    def attach(self, vobj):
        '''Setup the scene sub-graph of the view provider, this method is mandatory'''
        self.Object = vobj.Object
        self.onChanged(vobj, 'Base')
 
    def updateData(self, fp, prop):
        '''If a property of the handled feature has changed we have the chance to handle this here'''
        pass
    
    def claimChildren(self):
        '''Return a list of objects that will be modified by this feature'''
        pass
        
    def onDelete(self, feature, subelements):
        '''Here we can do something when the feature will be deleted'''
        return True
    
    def onChanged(self, fp, prop):
        '''Here we can do something when a single property got changed'''
        pass
        
    def setEdit(self, vobj=None, mode=0):
        return False
        
    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        return None
 
    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None
        


def selected_to_techdraw(doc, offsets, techdraw, BeamWidth):
    x = BeamWidth
    y = 0
    
    for offset in offsets:
        viewname = offset.Label.replace('offset', 'contour')
        views = doc.getObjectsByLabel(viewname)
        if len(views) > 0:
            view = views[0]
        else:
            view = doc.addObject('TechDraw::DrawViewPart', viewname)
            techdraw.addView(view)
                   
        try:
            view.CoarseView = False
            view.ViewObject.LineWidth = BeamWidth
            view.Source = offset
            view.Direction = Vector(0, 0, 1)
            view.ScaleType = u'Custom'
            view.Scale = 1.00
        except Exception as ex:
            app.Console.PrintError('\nview for ' + viewname + ' cannot be created ! ')
            app.Console.PrintError(ex)
    
    for view in techdraw.Views:
        offset = view.Source[0]
        bbox = offset.Shape.BoundBox
        bsize = Vector(bbox.XLength, bbox.YLength, bbox.ZLength)
        
        # add a 2D view to the TechDraw page right of the last part
        maxheight = y + bsize.y + BeamWidth
        if maxheight > techdraw.Template.Height:
            techdraw.Template.Height = maxheight

        maxwidth = x + bsize.x + BeamWidth
        if maxwidth > techdraw.Template.Width:
            techdraw.Template.Width = maxwidth
                          
        view.X = x + bsize.x / 2
        view.Y = y + bsize.y - (bsize.y / 2)
        x = x + bsize.x + BeamWidth

def makeLasercutterTechdrawExport(parts, BeamWidth = 0.2, doc = app.activeDocument(), method = 'auto', normal = Vector(0, 0, 0)):
    if len(parts) == 0: return
             
    techdraw = doc.addObject('TechDraw::DrawPage','LasercutterTechdraw')
    template = doc.addObject('TechDraw::DrawSVGTemplate','Template')
    techdraw.Template = template
    doc.recompute()
    
    for p in parts:
        if len(p.Shape.Solids) > 1:
            for sol in p.Shape.Solids:
                sfp = doc.addObject('Part::Feature', p.Label) 
                sfp.Shape = Part.Shape(sol)
                sfp.ViewObject.hide()
                addToExportObjects(doc, sfp)
                addLasercutterTechdrawItem(techdraw, sfp, BeamWidth, doc, method, normal)
                
        else:
            addLasercutterTechdrawItem(techdraw, p, BeamWidth, doc, method, normal)
        
    doc.recompute() 
    techdraw.ViewObject.show() 
    return techdraw
    
    
def addLasercutterTechdrawItem(techdraw, part, BeamWidth = 0.2, doc = app.activeDocument(), method = 'auto', normal = Vector(0, 0, 0)):       
    ifp = doc.addObject('Part::FeaturePython', 'LasercutterTechdrawExport')
    LasercutterTechdrawExportItem(ifp, part, BeamWidth, method=method, Normal=normal)
    LasercutterTechdrawExportItemViewProvider(ifp.ViewObject)
    doc.recompute()
    selected_to_techdraw(doc, [ifp], techdraw, BeamWidth)
    addToExportObjects(doc, ifp)
    return ifp
    
def addToExportObjects(doc, ifp):
    LaserCutterExportObjects = doc.getObjectsByLabel('LaserCutterExportObjects')
    if len(LaserCutterExportObjects) == 0:
        LaserCutterExportObjects = doc.addObject('App::DocumentObjectGroup', 'LaserCutterExportObjects')
    else:
        LaserCutterExportObjects = LaserCutterExportObjects[0]
        
    LaserCutterExportObjects.Group = LaserCutterExportObjects.Group + [ifp]
    LaserCutterExportObjects.ViewObject.hide()
