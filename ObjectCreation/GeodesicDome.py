# -*- coding: utf-8 -*-

# ************************************************************************
# * Copyright (c)2015 Ulrich Brammer <ulrich1a[at]users.sourceforge.net> *
# *                                                                      *
# * This file is a supplement to the FreeCAD CAx development system.     *
# *                                                                      *
# * This program is free software; you can redistribute it and/or modify *
# * it under the terms of the GNU Lesser General Public License (LGPL)   *
# * as published by the Free Software Foundation; either version 2 of    *
# * the License, or (at your option) any later version.                  *
# * for detail see the LICENCE text file.                                *
# *                                                                      *
# * This software is distributed in the hope that it will be useful,     *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of       *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
# * GNU Library General Public License for more details.                 *
# *                                                                      *
# * You should have received a copy of the GNU Library General Public    *
# * License along with this macro; if not, write to the Free Software    *
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 *
# * USA                                                                  *
# *                                                                      *
# ************************************************************************

__Name__ = 'Geodesic Dome'
__Comment__ = 'Geodesic Dome'
__Author__ = 'Ulrich Brammer'
__Version__ = '0.0.3'
__Date__ = '2019-03-08'
__License__ = 'LGPL-2.0-or-later'
__Web__ = ''
__Wiki__ = ''
__Icon__ = ''
__Help__ = ''
__Status__ = ''
__Requires__ = ''
__Communication__ = 'https://github.com/FreeCAD/FreeCAD-macros/issues/'
__Files__ = ''

import math
import sys

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import Part

def makeDomeShape(domeRad, ny):
    #semi-global variables
    a = 0 #Strutlength of underlying icosahedron:
    icoFaces = [] # collects faces of the underlying icosahedron
    domeFaces = [] # collects the faces of the geodesic dome
    
    def makeFreqFaces(fPt, sPt, thPt, ny = 1):
        # makes the geodesic dome faces out of the points of an
        # icosahedron triangle
        b = a/ny # length of frequent triangles
        # definition of direction vectors
        growVec = (sPt - fPt)
        # growVec = (fPt - sPt)
        growVec.multiply(1.0/ny)
        crossVec = (thPt - sPt)
        # crossVec = (sPt - thPt)
        crossVec.multiply(1.0/ny)
        
        for k in range(ny):
            kThirdPt = fPt + growVec * (k+0.0)
            dThirdPt = FreeCAD.Vector(kThirdPt.x, kThirdPt.y, kThirdPt.z)
            dThirdPt = dThirdPt.normalize().multiply(domeRad)
            kSecPt = fPt + growVec * (k+1.0)
            dSecPt = FreeCAD.Vector(kSecPt.x, kSecPt.y, kSecPt.z)
            dSecPt = dSecPt.normalize().multiply(domeRad)
            # thirdEdge = Part.makeLine(kSecPt, kThirdPt)
            # thirdEdge = Part.makeLine(dSecPt, dThirdPt)
            for l in range(k+1):
                firstPt = kSecPt + crossVec *(l+1.0)
                dFirstPt = firstPt.normalize().multiply(domeRad)
                secPt = kSecPt + crossVec *(l+0.0)
                dSecPt =secPt.normalize().multiply(domeRad)
                thirdPt = kThirdPt + crossVec *(l+0.0)
                dThirdPt = thirdPt.normalize().multiply(domeRad)
                #thirdEdge = Part.makeLine(secPt, thirdPt)
                thirdEdge = Part.makeLine(dSecPt, dThirdPt)
                # Part.show(thirdEdge)
                if l > 0:
                    print("in l: ", l, " mod 2: ", l%2)
                    # What to do here?
                    #secEdge = Part.makeLine(oThirdPt,thirdPt)
                    secEdge = Part.makeLine(doThirdPt,dThirdPt)
                    # Part.show(secEdge)
                    #thirdEdge = Part.makeLine(secPt, thirdPt)
                    #thirdEdge = Part.makeLine(dSecPt, dThirdPt)
                    # Part.show(thirdEdge)
                    triWire = Part.Wire([firstEdge, secEdge, thirdEdge])
                    # Part.show(triWire)
                    triFace = Part.Face(triWire)
                    domeFaces.append(triFace)
                    #Part.show(triFace)
                
                oThirdPt = thirdPt
                doThirdPt = oThirdPt.normalize().multiply(domeRad)
                # oFirstPt = firstPt
                #firstEdge = Part.makeLine(thirdPt,firstPt)
                firstEdge = Part.makeLine(dThirdPt,dFirstPt)
                oFirstEdge = firstEdge
                #secEdge = Part.makeLine(firstPt,secPt)
                secEdge = Part.makeLine(dFirstPt,dSecPt)
                #Part.show(firstEdge)
                #Part.show(secEdge)
                #Part.show(thirdEdge)
                triWire = Part.Wire([firstEdge, secEdge, thirdEdge])
                triFace = Part.Face(triWire)
                domeFaces.append(triFace)
                #Part.show(triFace)
    
        
    a=(4.0*domeRad)/math.sqrt(2.0*math.sqrt(5.0)+10.0) 
    
    # icoAngle: angle of vertices of icosahedron points 
    # not a north or south pole
    icoAngle = math.atan(0.5)
    
    icoLat = domeRad * math.sin(icoAngle)
    latRad = domeRad * math.cos(icoAngle)
    ang36 = math.radians(36.0)
    
    # Calculation all points of the icosahedron
    icoPts = []
    icoPts.append(FreeCAD.Vector(0.0, 0.0, domeRad))
    
    for i in range(10):
        icoCos = latRad * math.cos(i*ang36)
        icoSin = latRad * math.sin(i*ang36)
        if i%2 == 0:
            icoPts.append(FreeCAD.Vector(icoSin, icoCos, icoLat))
        else:
            icoPts.append(FreeCAD.Vector(icoSin, icoCos, -icoLat))
    
    icoPts.append(FreeCAD.Vector(0.0, 0.0, -domeRad))
    
    # making the faces of the icosahedron
    
    
    thirdPt = icoPts[9]
    thirdEdge = Part.makeLine(icoPts[0],thirdPt)
    for i in range(5):
        j = i*2+1
        firstEdge = Part.makeLine(thirdPt,icoPts[j])
        secEdge = Part.makeLine(icoPts[j],icoPts[0])
        triWire = Part.Wire([firstEdge, secEdge, thirdEdge])
        triFace = Part.Face(triWire)
        icoFaces.append(triFace)
        # Part.show(triFace)
        makeFreqFaces(icoPts[j], icoPts[0], thirdPt, ny)
        
        thirdEdge = Part.makeLine(icoPts[0],icoPts[j])
        thirdPt = icoPts[j]
        
    thirdPt = icoPts[9]
    secPt = icoPts[10]
    thirdEdge = Part.makeLine(secPt,thirdPt)
    
    for i in range(10):
        j = i+1
        firstEdge = Part.makeLine(thirdPt,icoPts[j])
        secEdge = Part.makeLine(icoPts[j],secPt)
        triWire = Part.Wire([firstEdge, secEdge, thirdEdge])
        triFace = Part.Face(triWire)
        icoFaces.append(triFace)
        #Part.show(triFace)
        makeFreqFaces(icoPts[j], secPt, thirdPt, ny)
    
        thirdPt = secPt	
        secPt = icoPts[j]	
        thirdEdge = Part.makeLine(secPt,thirdPt)
    
    
    thirdPt = icoPts[10]
    thirdEdge = Part.makeLine(icoPts[11],thirdPt)
    for i in range(5):
        j = i*2+2
        firstEdge = Part.makeLine(thirdPt,icoPts[j])
        secEdge = Part.makeLine(icoPts[j],icoPts[11])
        triWire = Part.Wire([firstEdge, secEdge, thirdEdge])
        triFace = Part.Face(triWire)
        icoFaces.append(triFace)
        #Part.show(triFace)
        makeFreqFaces(icoPts[j], icoPts[11], thirdPt, ny)
        
        thirdEdge = Part.makeLine(icoPts[11],icoPts[j])
        thirdPt = icoPts[j]
    
    # Shell of a corresponding icosahedron	
    newShell = Part.Shell(icoFaces)
    #Part.show(newShell)
    
    # Shell of the geodesic dome
    #domeShell = Part.Shell(domeFaces)
    #Part.show(domeShell)
    return Part.Shell(domeFaces)
    
    # Shere with radius of geodesic dome for debugging purposes
    # testSphere = Part.makeSphere(domeRad)
    #Part.show(testSphere)


try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def tr(context, text):
        return QtGui.QApplication.translate(context, text, None, _encoding)
except AttributeError:
    def tr(context, text):
        return QtGui.QApplication.translate(context, text, None)

def say(s):
    FreeCAD.Console.PrintMessage(str(s)+"\n")

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(477, 188)
        self.dia = Dialog
        self.gridLayoutWidget = QtGui.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(19, 19, 440, 141))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        #self.lineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        fui = FreeCADGui.UiLoader()
        self.lineEdit = fui.createWidget("Gui::InputField")
        
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.gridLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons \
            (QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.retranslateUi(Dialog)      
        QtCore.QObject.connect(self.buttonBox, \
            QtCore.SIGNAL("accepted()"), self.makeSomething)
        QtCore.QObject.connect(self.buttonBox, \
            QtCore.SIGNAL("rejected()"), self.makeNothing)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(tr("GeodesicDome", "Geodesic Dome Creator"))
        self.label.setText(tr("GeodesicDome", "Dome Radius"))
        self.label_2.setText(tr("GeodesicDome",
                                "Frequency Parameter\n(Integer between 1 to 10)"))
        self.label_3.setText(tr("GeodesicDome",
                                "This Macro creates \na full geodesic dome shell.\nX-Y-symmetry plane \nfor even frequencies"))


    def makeSomething(self):
        say("Accepted! Dome radius: {} with frequency {}".format(
           self.lineEdit.property("text"),
           int(self.lineEdit_2.text())))
        
        if FreeCAD.ActiveDocument is None:
            FreeCAD.newDocument()
        doc = FreeCAD.ActiveDocument
        theDome = GeodesicDome(doc).host
        theDome.Radius = FreeCAD.Units.Quantity(self.lineEdit.property("text"))
        theDome.FrequencyParameter = int(self.lineEdit_2.text())
            
        self.dia.close()
        doc.recompute()
        
    def makeNothing(self):
        say("rejected!!")
        self.dia.close()

def showDialog():
    d = QtGui.QWidget()
    d.ui = Ui_Dialog()
    d.ui.setupUi(d)
    d.ui.lineEdit_2.setText("2")
    d.ui.lineEdit.setProperty("text", "2 m")
    
    d.show()
    

class GeodesicDome(object):
    host = None
    def __init__(self, doc):
        host = doc.addObject('Part::FeaturePython', 'GeoDome')
        self.host = host
        host.Proxy = self
        
        VPGeodesicDome(host.ViewObject)
        
        host.addProperty('App::PropertyLength', 'Radius', "Geodesic Dome", "")
        host.addProperty('App::PropertyInteger', 'FrequencyParameter', "Geodesic Dome", "Frequency Parameter (integer, 1 to 10). If even, the dome is symmetric against XY plane.")
        host.addProperty('App::PropertyEnumeration', 'ShapeType', "Geodesic Dome", "")
        host.ShapeType = ['Solid', 'Shell', 'Wireframe', 'Vertices']
    
    def execute(self, host):
        shell = makeDomeShape(host.Radius.getValueAs('mm'), host.FrequencyParameter)
        if host.ShapeType == 'Solid':
            host.Shape = Part.Solid(shell)
        elif host.ShapeType == 'Shell':
            host.Shape = shell
        elif host.ShapeType == 'Wireframe':
            host.Shape = Part.Compound(shell.Edges)
        elif host.ShapeType == 'Vertices':
            host.Shape = Part.Compound(shell.Vertexes)
        else:
            assert(False)

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None
    
class VPGeodesicDome(object):
    def __init__(self, host):
        host.Proxy = self
    
    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None

if __name__ == '__main__':
    #running as a macro. Load as module, to support save-restore.
    try:
        import GeodesicDome    
    except ImportError as err:
        FreeCAD.Console.PrintError("Macro Geodesic Dome: failed to import MacroGeodesicDome.py. The parametric object will lose functionality after saving-loading your project, sorry.")
        showDialog()
    else:
        GeodesicDome.showDialog()
