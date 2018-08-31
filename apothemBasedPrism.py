# # # # # # # # # # #
#
# Apothem Based Prism
#
# This script will take the input of the distance between flats, (apothem, aka inradius),
# and the number of sidesfor a regular polygon along with a height and produce a
# correctly sized prism derived from the circumradius.
#
# # # # # # # # # # #

__Name__ = 'Apothem Based Prism'
__Comment__ = ''
__License__ = ''
__Web__ = 'http://www.freecadweb.org/wiki/Macro_Apothem_Based_Prism_GUI'
__Wiki__ = 'http://www.freecadweb.org/wiki/Macro_Apothem_Based_Prism_GUI'
__Icon__ = ''
__Help__ = ''
__Author__ = ''
__Version__ = ''
__Status__ = ''
__Requires__ = ''
__Files__ = ''


import FreeCAD, FreeCADGui, Part, PartGui, math
from FreeCAD import Base
from PySide import QtGui, QtCore
from math import cos, radians
App = FreeCAD
Gui = FreeCADGui

class p():


    def priSm(self):

        try:
            dbf = float(self.d1.text())
            nos = int(self.d2.text())
            hth = float(self.d3.text())
            aR = dbf / 2
            op1 = 180/float(nos)
            coS = cos(math.radians(op1))
            cR = aR / coS
            prism=App.ActiveDocument.addObject("Part::Prism","Prism")
            prism.Polygon=nos
            prism.Circumradius=cR
            prism.Height=hth
            prism.Placement=Base.Placement(Base.Vector(0.00,0.00,0.00),Base.Rotation(0.00,0.00,0.00,1.00))
            prism.Label='Prism'
            App.ActiveDocument.recompute()
            Gui.SendMsgToActiveView("ViewFit")
        except:
            FreeCAD.Console.PrintError("Unable to complete task")

            self.close()

    def close(self):
        self.dialog.hide()


#
# Make dialog box and get input for distance between flats, number of sides, and height
#

    def __init__(self):
        self.dialog = None

        self.dialog = QtGui.QDialog()
        self.dialog.resize(280,110)

        self.dialog.setWindowTitle("Apothem Based Prism")
        la = QtGui.QVBoxLayout(self.dialog)

        iN1 = QtGui.QLabel("Distance Between Flats")
        la.addWidget(iN1)
        self.d1 = QtGui.QLineEdit()
        la.addWidget(self.d1)

        iN2 = QtGui.QLabel("Number Of Sides (Best results - use even numbers)")
        la.addWidget(iN2)
        self.d2 = QtGui.QLineEdit()
        la.addWidget(self.d2)

        iN3 = QtGui.QLabel("Prism Height")
        la.addWidget(iN3)
        self.d3 = QtGui.QLineEdit()
        la.addWidget(self.d3)

        okbox = QtGui.QDialogButtonBox(self.dialog)
        okbox.setOrientation(QtCore.Qt.Horizontal)
        okbox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        la.addWidget(okbox)
        QtCore.QObject.connect(okbox, QtCore.SIGNAL("accepted()"), self.priSm)
        QtCore.QObject.connect(okbox, QtCore.SIGNAL("rejected()"), self.close)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)
        self.dialog.show()
        self.dialog.exec_()


p()
