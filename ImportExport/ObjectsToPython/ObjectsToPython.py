# -*- coding: utf-8 -*-

__Name__ = 'Objects To Python'
__Comment__ = 'Exports objects from a FreeCAD project to a python script'
__Author__ = 'Christi'
__Version__ = '0.1'
__Date__ = '2019-03-02'
__License__ = 'LGPL-3.0-or-later'
__Web__ = ''
__Wiki__ = 'README.md'
__Icon__ = ''
__Help__ = ''
__Status__ = ''
__Requires__ = 'FreeCAD >= 0.17'
__Communication__ = ''
__Files__ = ''

VERSION_STRING = __Name__ + ' Macro v' + __Version__


import FreeCAD
import FreeCADGui
import Part
import re


def addScript(line):
    FreeCAD.Console.PrintMessage(line)
    FreeCAD.Console.PrintMessage("\n")


def toScript():
    doc =FreeCAD.ActiveDocument
    addScript("from FreeCAD import *");
    addScript("import Sketcher");
    addScript("import Part");
    addScript("")
    objectlist = []
    skipObjects = [('App::Line', 'X_Axis'), ('App::Line', 'Y_Axis'), ('App::Line', 'Z_Axis'),
                   ('App::Plane', 'XY_Plane'), ('App::Plane', 'XZ_Plane'), ('App::Plane', 'YZ_Plane'),
                   ('App::Origin', 'Origin')] 
    
    selection = FreeCADGui.Selection.getSelection() 
    if not selection:
        addScript("doc = App.newDocument('%s')"%doc.Name)
        selection = doc.Objects
    else:
        addScript("doc = App.ActiveDocument")
        expandSelection(selection)
        
    for obj in doc.Objects:  
        objectlist.append(doc.getObject(obj.Name)) 
         
    for obj in selection:    
        if (obj.TypeId, obj.Label) not in skipObjects:  
            addScript("%s = doc.addObject('%s', '%s')"%(obj.Label, obj.TypeId, obj.Label))
        
    for obj in selection: 
        if (obj.TypeId, obj.Label) not in skipObjects:
            addScript("")
            addObject(doc, obj, objectlist)
            
    addScript("\ndoc.recompute()")  
    
    
def expandSelection(selection):    
    addthis = []     
    for obj in selection:    
        if hasattr(obj, 'Group'):
            addthis += obj.Group
        if hasattr(obj, 'Source'):
            addthis.append(obj.Source)
        if hasattr(obj, 'Links'):
            addthis += obj.Links
            
    added = 0
    for a in addthis:
        if (not a in selection) and hasattr(obj, 'Name') and hasattr(obj, 'TypeId'):
            selection.insert(0, a)
            added = added + 1
            
    if added > 0:
        expandSelection(selection)
            

def addObject(doc, obj, objectlist): 
    defaultobj = doc.addObject(obj.TypeId, obj.Name + "Default")
    addProperties(obj, obj.Label, defaultobj, objectlist)
    addProperties(obj.ViewObject, obj.Label + ".ViewObject", defaultobj.ViewObject, [])                      
    doc.removeObject(obj.Name + "Default")             
    
    
def addProperties(obj, objname, refobj, objectlist):
    skipProperties = ["Label", "Shape", "Proxy", "AddSubShape"]
    skipObjProp = [("Sketcher::SketchObject", "Geometry"), ("Sketcher::SketchObject", "Constraints"),
        ('PartDesign::Body', 'Origin')]
    
    if obj.TypeId == "Spreadsheet::Sheet":
        addSpreadsheet(obj, objname)
        return
    
    if obj.TypeId == "Sketcher::SketchObject":
        addSketch(obj, objname)

    for propname in obj.PropertiesList:
        if not propname in skipProperties and not (obj.TypeId, propname) in skipObjProp:
            prop = obj.getPropertyByName(propname)  
            val = objectToText(prop, objectlist)
            
            try:
                refprop = refobj.getPropertyByName(propname)
                defaultval = objectToText(refprop, objectlist)
            except:
                defaultval = None
                
            if propname == "Support":
                val = val.replace("XY_Plane", "doc.XY_Plane")
                val = val.replace("XZ_Plane", "doc.XZ_Plane")
                val = val.replace("YZ_Plane", "doc.YZ_Plane")
                
            if propname == "ExpressionEngine":
                for expression in prop:
                    addScript("%s.setExpression%s"%(objname, expression))                                   
                                                    
            elif objectToText(prop, objectlist) is not None:   
                if defaultval is None: 
                    addScript("%s.set('%s', '%s')"%(objname, propname, val))                    
                elif val != defaultval:        
                    addScript("%s.%s = %s"%(objname, propname, val))   
                    
                                                                                                                            
def objectToText(obj, objectlist = []):    
    if obj in objectlist:
        return obj.Label
    
    else:
        if hasattr(obj, 'Value') and hasattr(obj, 'Unit'):  # how can I test if type(obj) is Base.Quantity ?
            return "%s"%(obj.Value)
        else:     
            if isinstance(obj, str):
                return "\"%s\""%(obj)
                
            if isinstance(obj, bool):
                if obj:
                    return "True"
                else:
                    return "False"
            
            if isinstance(obj, int):
                return "%d"%(obj)
    
            if isinstance(obj, float):
                return "%f"%(obj)                                      
            
            if isinstance(obj, FreeCAD.Base.Placement):
                return "Placement(%s, %s)"%(obj.Base, obj.Rotation)
            
            if isinstance(obj, Part.Point):
                return "Part.Point(Vector(%f,%f,%f))"%(obj.X, obj.Y, obj.Z)
            
            if isinstance(obj, Part.LineSegment):
                return "Part.LineSegment(%s, %s)"%(obj.StartPoint, obj.EndPoint)
            
            if isinstance(obj, Part.Circle):
                return "Part.Circle(%s, %s, %f)"%(obj.Center, obj.Axis, obj.Radius)
            
            if isinstance(obj, Part.ArcOfCircle):
                #return "Part.ArcOfCircle(%s, %s, %s)"%(obj.Center, obj.StartPoint, obj.EndPoint)
                return "Part.ArcOfCircle(%s, %s, %s)"%(objectToText(obj.Circle), obj.FirstParameter, obj.LastParameter)
            
            if isinstance(obj, Part.Ellipse):
                return "Part.Ellipse(%s, %s, %s)"%(obj.Center, obj.MajorRadius, obj.MinorRadius)
            
            if isinstance(obj, Part.BSplineCurve):
                return "Part.BSplineCurve(%s)"%(obj.getPoles())

            liststart = ""
            if isinstance(obj, list):
                liststart = "["
                listend = "]"
                
            if isinstance(obj, tuple):
                liststart = "("
                listend = ")"
                
            if liststart != "":
                sline = liststart;
                comma = False
                for listele in obj:
                    if comma:
                        sline = sline + " ,"
                    else:
                        comma = True                
                
                    val = objectToText(listele, objectlist)
                    if val is not None:
                        sline = sline + val
                    
                sline += listend;
                return sline                  
            
            stringobj = "%s"%(obj)                            
            return stringobj
        
    
def addSketch(obj, objname): 
    prop = obj.getPropertyByName('Geometry')  
    for geo in prop:  
        addScript("%s.addGeometry(%s, %s)"%(objname, objectToText(geo), objectToText(geo.Construction)))  
    
    splinecount = 0   
    concount = 0
    prop = obj.getPropertyByName('Constraints')
    for con in obj.Constraints:
        conargs = ""
        contype = con.Type
        if con.Type == 'Coincident':
            conargs = "%d, %d, %d, %d"%(con.First, con.FirstPos, con.Second, con.SecondPos)
        elif con.Type == 'PointOnObject':
            conargs = "%d, %d, %d"%(con.First, con.FirstPos, con.Second)
        elif con.Type == 'Vertical':
            conargs = "%d"%(con.First)
        elif con.Type == 'Horizontal':
            conargs = "%d"%(con.First)
        elif con.Type == 'Parallel':
            conargs = "%d, %d"%(con.First, con.Second)
        elif con.Type == 'Perpendicular':
            conargs = "%d, %d"%(con.First, con.Second)
        elif con.Type == 'Tangent':
            if con.Second == -2000:
                conargs = "%d, %d"%(con.First, con.FirstPos)
            elif con.Third == -2000:
                conargs = "%d, %d, %d, %d"%(con.First, con.FirstPos, con.Second, con.SecondPos)
            else:
                contype = 'TangentViaPoint'
                conargs = "%d, %d, %d, %d"%(con.First, con.Second, con.Third, con.ThirdPos)
        elif con.Type == 'Equal':
            conargs = "%d, %d"%(con.First, con.Second)
        elif con.Type == 'Symmetric':
            conargs = "%d, %d, %d, %d, %d, %d"%(con.First, con.FirstPos, con.Second, con.SecondPos, con.Third, con.ThirdPos)
        elif con.Type == 'Block':
            conargs = "%d"%(con.First)
        elif con.Type == 'Distance':
            if con.Second == -2000:
                conargs = "%d, %f"%(con.First, con.Value)
            else:
                conargs = "%d, %d, %d, %d, %f"%(con.First, con.FirstPos, con.Second, con.SecondPos, con.Value)
        elif con.Type == 'DistanceX' or con.Type == 'DistanceY':
            if con.Second == -2000:
                conargs = "%d, %d, %f"%(con.First, con.FirstPos, con.Value)
            else:
                conargs = "%d, %d, %d, %d, %f"%(con.First, con.FirstPos, con.Second, con.SecondPos, con.Value)
        elif con.Type == 'Radius':
            conargs = "%d, %f"%(con.First, con.Value)
        elif con.Type == 'Angle':
            conargs = "%d, %d, %d, %d, %f"%(con.First, con.FirstPos, con.Second, con.SecondPos, con.Value)
        elif con.Type == 'InternalAlignment':
            contype = 'InternalAlignment:Sketcher::BSplineControlPoint'
            conargs = "%d, %d, %d, %d"%(con.First, con.FirstPos, con.Second, splinecount)
            splinecount = splinecount + 1
            
        if con.Type != 'InternalAlignment':
            splinecount = 0

        if conargs is not None:
            addScript("%s.addConstraint(Sketcher.Constraint('%s', %s))"%(objname, contype, conargs))
            
        if con.Name != "":
            addScript("%s.renameConstraint(%d, u'%s')"%(objname, concount, con.Name))
            
        concount = concount + 1
                   
                
def addSpreadsheet(obj, objname): 
    for propname in obj.PropertiesList:    
        match = re.search('[A-Z]+[0-9]+', propname)
        if match is not None:
            prop = obj.getPropertyByName(propname)
            val = objectToText(prop)
            addScript("%s.set('%s', '%s')"%(objname, propname, val))  
            alias = obj.getAlias(propname)
            if alias is not None:
                addScript("%s.setAlias('%s', '%s')"%(objname, propname, alias))
    
    addScript("doc.recompute()")   
      
        
toScript()
