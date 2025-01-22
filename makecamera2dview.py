#-------------------------------------------------
#-- makecamera2dview
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
# create a 2dview object from the camera position

__Name__ = 'Make Camera 2D View'
__Comment__ = 'create a 2DView object from the camera position'
__Web__ = ""
__Wiki__ = ""
__Icon__  = ""
__Help__ = "select an object"
__Author__ = "microelly"
__Version__ = "0.1.1"
__Status__ = 'alpha'
__Requires__ = 'numpy'

import Draft
import FreeCAD as app
import FreeCADGui as gui
import PySide  # FreeCAD's PySide!


import numpy as np
from pivy import coin


def errorDialog(msg):
    diag = PySide.QtGui.QMessageBox(PySide.QtGui.QMessageBox.Critical, "Error Message", msg)
    diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()


try:
    sel = gui.Selection.getSelection()[0]
    c = Draft.clone(sel)
except Exception:
    errorDialog("Select one object")
    raise Exception()


camera = gui.ActiveDocument.ActiveView.getCameraNode()
# camera.position.setValue(app.Vector(100,50,10))
camera.pointAt(coin.SbVec3f(0,0,0), coin.SbVec3f(0,0,1))

al = str(camera.position.getValue().toString()).split(' ')
vec2 = app.Vector(float(al[0]), float(al[1]), float(al[2]))

yaw_deg = np.degrees(np.arctan2(vec2.x, vec2.y))
pitch_deg = np.degrees(np.arctan2(vec2.z, np.sqrt(vec2.x**2 + vec2.y**2)))

pla1 = app.Placement(app.Vector(0, 0, 0), app.Rotation(0, 0, -90))
pla2 = app.Placement(app.Vector(0, 0, 0), app.Rotation(0, 180+yaw_deg, 0)).multiply(pla1)
pla3 = app.Placement(app.Vector(0, 0, 0), app.Rotation(0, 0, pitch_deg)).multiply(pla2)

c.Placement = pla3
c.ViewObject.Visibility = False
v = Draft.makeShape2DView(c)
