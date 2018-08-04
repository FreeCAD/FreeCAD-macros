# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- makecamera2dview
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
# create a 2dview object from the camera position

__Comment__ = 'create a 2dview object from the camera position'
__Web__ = ""
__Wiki__ = ""
__Icon__  = ""
__Help__ = "select an object"
__Author__ = "microelly"
__Version__ = 0.1
__Status__ = 'alpha'
__Requires__ = 'numpy'




import numpy as np
from pivy import coin
import FreeCAD,Draft,FreeCADGui
import PySide

def errorDialog(msg):
    diag = PySide.QtGui.QMessageBox(PySide.QtGui.QMessageBox.Critical,u"Error Message",msg )
    diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()

try:
    sel = FreeCADGui.Selection.getSelection()[0]
    c=Draft.clone(sel)
except Exception:
    errorDialog( "Select one object")
    raise Exception()


camera = FreeCADGui.ActiveDocument.ActiveView.getCameraNode()
# camera.position.setValue(FreeCAD.Vector(100,50,10))
camera.pointAt(coin.SbVec3f(0,0,0),coin.SbVec3f(0,0,1))

al=str(camera.position.getValue().toString()).split(' ')
vec2=FreeCAD.Vector(float(al[0]),float(al[1]),float(al[2]))
print al

gier=np.arctan2(vec2.x,vec2.y) *180/np.pi
steig=np.arctan2(vec2.z,np.sqrt(vec2.x**2 + vec2.y**2)) *180/np.pi
print  gier
print steig

pla1=App.Placement(App.Vector(0,0,0), App.Rotation(0,0,-90), App.Vector(0,0,0))
pla2=App.Placement(App.Vector(0,0,0), App.Rotation(0,180+gier,0), App.Vector(0,0,0)).multiply(pla1)
pla3=App.Placement(App.Vector(0,0,0), App.Rotation(0,0,steig), App.Vector(0,0,0)).multiply(pla2)

c.Placement=pla3
c.ViewObject.Visibility=False
v=Draft.makeShape2DView(c)

print vec2
print pla1
print pla2
print pla3
