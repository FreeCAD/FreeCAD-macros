
# -*- coding: utf-8 -*-
# Macro_CartoucheFC.py
# Remplir les zones du cartouche de la feuille originale de FreeCAD
# http://www.freecadweb.org/wiki/index.php?title=Macro_CartoucheFC/fr
# il faut que la page (drawing viewer) s'appelle " Page " qui est le nom par défaut du module Drawing
# Fill the area of the cartridge
# http://www.freecadweb.org/wiki/index.php?title=Macro_CartoucheFC
# It is necessary that the page (drawing viewer) is called "Page", which is the default name of the Drawing module
# ver 0.3
# Created: 02/07/2014
# Created:  by mario52
# PyQt and PySide

#OS: Windows Vista
#Word size: 32-bit
#Version: 0.14.3700 (Git)
#Branch: releases/FreeCAD-0-14
#Hash: 32f5aae0a64333ec8d5d160dbc46e690510c8fe1
#Python version: 2.6.2
#Qt version: 4.5.2
#Coin version: 3.1.0
#SoQt version: 1.4.1

# see http://www.freecadweb.org/wiki/index.php?title=Macro_CartoucheFC

try:
    import PyQt4
    from PyQt4 import QtCore, QtGui

except Exception:
    import PySide
    from PySide import QtCore, QtGui

import Draft, Part, FreeCAD, math, PartGui, FreeCADGui
from math import sqrt, pi, sin, cos, asin
from FreeCAD import Base

global  path

path = FreeCAD.ConfigGet("AppHomePath")

def heure():
    return QtCore.QTime().currentTime().toString('hh:mm:ss')

def dateEu():
    return QtCore.QDate().currentDate().toString('dd/MM/yyyy') # forme euro

def dateUs():
    return QtCore.QDate().currentDate().toString('MM/dd/yyyy') # forme us

def dateComp():
    return QtCore.QDate().currentDate().toString('dddd d MMMM yyyy') # Retourne "dimanche 20 Juillet 69"

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

def errorDialog(msg):
    # Create a simple dialog QMessageBox
    # The first argument indicates the icon used: one of QtGui.QMessageBox.{NoIcon, Information, Warning, Critical, Question}
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,u"Error Message",msg)
    try:
        diag.setWindowFlags(PyQt4.QtCore.Qt.WindowStaysOnTopHint)  #PyQt4 cette fonction met la fenêtre en avant
    except Exception:
        diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint) #PySide cette fonction met la fenêtre en avant
    #diag.setWindowModality(QtCore.Qt.ApplicationModal) # la fonction a été désactivée pour favoriser "WindowStaysOnTopHint"
    diag.exec_()

def symbol_EU(depx,depy):    #symbol_EU
    try:
        App.getDocument(App.ActiveDocument.Name).removeObject("Symbol_US")
    except:
        None
    try:
        App.getDocument(App.ActiveDocument.Name).removeObject("Symbol_EU")
    except:
        None
    try:
        App.getDocument(App.ActiveDocument.Name).removeObject("SymbolUS")
    except:
        None
    try:
        App.getDocument(App.ActiveDocument.Name).removeObject("SymbolEU")
    except:
        None
    App.activeDocument().addObject('Sketcher::SketchObject','Symbol_EU')
    App.activeDocument().Symbol_EU.Placement = App.Placement(App.Vector(0.0,0.0,0.0),App.Rotation(0.000000,0.000000,0.000000,1.000000))
    App.ActiveDocument.Symbol_EU.addGeometry(Part.Line(App.Vector(-7.5,0.0,0.0),App.Vector(20.0,0.0,0.0)))

    App.ActiveDocument.Symbol_EU.Placement = App.Placement(App.Vector(0.0,0.0),App.Rotation(0.000000,0.000000,0.000000,1.000000))
    App.ActiveDocument.Symbol_EU.addGeometry(Part.Line(App.Vector(12.50,-7.5,0),App.Vector(12.50,7.5,0.0)))
    App.ActiveDocument.Symbol_EU.addGeometry(Part.Circle(App.Vector(12.50,0.0,0),App.Vector(0,0,1),2.5))
    App.ActiveDocument.Symbol_EU.addGeometry(Part.Circle(App.Vector(12.50,0.0,0),App.Vector(0,0,1),5.0))

    App.ActiveDocument.Symbol_EU.addGeometry(Part.Line(App.Vector(5.0,5.0,0.0),App.Vector(-5.0,2.5,0.0)))
    App.ActiveDocument.Symbol_EU.addGeometry(Part.Line(App.Vector(-5.0,-2.5,0.0),App.Vector(-5.0,2.5,0.0)))
    App.ActiveDocument.Symbol_EU.addGeometry(Part.Line(App.Vector(5.0,-5.0,0.0),App.Vector(-5.0,-2.5,0.0)))
    App.ActiveDocument.Symbol_EU.addGeometry(Part.Line(App.Vector(5.0,-5.0,0.0),App.Vector(5.0,5.0,0.0)))
    Gui.getDocument(App.ActiveDocument.Name).resetEdit()
    FreeCADGui.getDocument(App.ActiveDocument.Name).getObject("Symbol_EU").LineColor = (0.00,0.00,0.00)
    App.ActiveDocument.recompute()

    App.activeDocument().addObject('Drawing::FeatureViewPart','SymbolEU')
    App.activeDocument().SymbolEU.Source = App.activeDocument().Symbol_EU
    App.activeDocument().SymbolEU.Direction = (0.0,0.0,1.0)
    App.activeDocument().SymbolEU.X = depx
    App.activeDocument().SymbolEU.Y = depy
    App.activeDocument().SymbolEU.Scale = 0.8
    App.activeDocument().Page.addObject(App.activeDocument().SymbolEU)
    App.ActiveDocument.recompute()
#    App.getDocument(App.ActiveDocument.Name).removeObject("Symbol_EU")
    FreeCADGui.getDocument(App.ActiveDocument.Name).getObject("Symbol_EU").Visibility = False

def symbol_US(depx,depy):    #symbol_US
    try:
        App.getDocument(App.ActiveDocument.Name).removeObject("Symbol_US")
    except:
        None
    try:
        App.getDocument(App.ActiveDocument.Name).removeObject("Symbol_EU")
    except:
        None
    try:
        App.getDocument(App.ActiveDocument.Name).removeObject("SymbolUS")
    except:
        None
    try:
        App.getDocument(App.ActiveDocument.Name).removeObject("SymbolEU")
    except:
        None
    App.activeDocument().addObject('Sketcher::SketchObject','Symbol_US')
    App.activeDocument().Symbol_US.Placement = App.Placement(App.Vector(0.0,0.0,0.0),App.Rotation(0.000000,0.000000,0.000000,1.000000))
    App.ActiveDocument.Symbol_US.addGeometry(Part.Line(App.Vector(-7.5,0.0,0.0),App.Vector(20.0,0.0,0.0)))

    App.ActiveDocument.Symbol_US.Placement = App.Placement(App.Vector(0.0,0.0),App.Rotation(0.000000,0.000000,0.000000,1.000000))
    App.ActiveDocument.Symbol_US.addGeometry(Part.Line(App.Vector(0.0,-7.5,0.0),App.Vector(0.0,7.5,0.0)))
    App.ActiveDocument.Symbol_US.addGeometry(Part.Circle(App.Vector(0.0,0.0,0.0),App.Vector(0,0,1),2.5))
    App.ActiveDocument.Symbol_US.addGeometry(Part.Circle(App.Vector(0.0,0.0,0.0),App.Vector(0,0,1),5.0))

    App.ActiveDocument.Symbol_US.addGeometry(Part.Line(App.Vector(17.5,5.0,0.0),App.Vector(7.5,2.5,0.0)))
    App.ActiveDocument.Symbol_US.addGeometry(Part.Line(App.Vector(7.5,-2.5,0.0),App.Vector(7.5,2.5,0.0)))
    App.ActiveDocument.Symbol_US.addGeometry(Part.Line(App.Vector(17.5,-5.0,0.0),App.Vector(7.5,-2.5,0.0)))
    App.ActiveDocument.Symbol_US.addGeometry(Part.Line(App.Vector(17.5,-5.0,0.0),App.Vector(17.5,5.0,0.0)))
    Gui.getDocument(App.ActiveDocument.Name).resetEdit()
    FreeCADGui.getDocument(App.ActiveDocument.Name).getObject("Symbol_US").LineColor = (0.00,0.00,0.00)
    App.ActiveDocument.recompute()

    App.activeDocument().addObject('Drawing::FeatureViewPart','SymbolUS')
    App.activeDocument().SymbolUS.Source = App.activeDocument().Symbol_US
    App.activeDocument().SymbolUS.Direction = (0.0,0.0,1.0)
    App.activeDocument().SymbolUS.X = depx
    App.activeDocument().SymbolUS.Y = depy
    App.activeDocument().SymbolUS.Scale = 0.8
    App.activeDocument().Page.addObject(App.activeDocument().SymbolUS)
    App.ActiveDocument.recompute()
#    App.getDocument(App.ActiveDocument.Name).removeObject("Symbol_US")
    FreeCADGui.getDocument(App.ActiveDocument.Name).getObject("Symbol_US").Visibility = False

try:
    DESIGNED_BY = App.activeDocument().getObject("Page").EditableTexts[0] #lineEdit01 DESIGNED_BY
    CREATION_DATE = App.activeDocument().getObject("Page").EditableTexts[1] #lineEdit02 CREATION_DATE date
    CREA_DATE = CREATION_DATE[0:10] # lineEdit02h date
    CREA_TIME = CREATION_DATE[13:21] # lineEdit02h heure
    CHECKED_BY = App.activeDocument().getObject("Page").EditableTexts[2] # lineEdit03
    CHECK_DATE = App.activeDocument().getObject("Page").EditableTexts[3] # lineEdit04 date
    CHEC_DATE = CHECK_DATE[0:10] # lineEdit04 date
    CHEC_TIME = CHECK_DATE[13:21] # lineEdit04h heure
    SIZE = "A3"  # lineEdit05
    SCALE = App.activeDocument().getObject("Page").EditableTexts[4] # lineEdit06
    WEIGHT = App.activeDocument().getObject("Page").EditableTexts[5] # lineEdit07
    DRAWING_NUMBER = App.activeDocument().getObject("Page").EditableTexts[6] # lineEdit08
    SHEET = App.activeDocument().getObject("Page").EditableTexts[7] # lineEdit09
    TITLE = App.activeDocument().getObject("Page").EditableTexts[8] # textEdit_01
    DESCRIPTION = App.activeDocument().getObject("Page").EditableTexts[9] # textEdit_02

except:
    errorDialog("erreur cartouche")

try:
    try:
        lineEdit18 = App.activeDocument().getObject("Note_I").Text[0]
    except:
        lineEdit18 = ""
    try:
        lineEdit17 = App.activeDocument().getObject("Note_H").Text[0]
    except:
        lineEdit17 = ""
    try:
        lineEdit16 = App.activeDocument().getObject("Note_G").Text[0]
    except:
        lineEdit16 = ""
    try:
        lineEdit15 = App.activeDocument().getObject("Note_F").Text[0]
    except:
        lineEdit15 = ""
    try:
        lineEdit14 = App.activeDocument().getObject("Note_E").Text[0]
    except:
        lineEdit14 = ""
    try:
        lineEdit13 = App.activeDocument().getObject("Note_D").Text[0]
    except:
        lineEdit13 = ""
    try:
        lineEdit12 = App.activeDocument().getObject("Note_C").Text[0]
    except:
        lineEdit12 = ""
    try:
        lineEdit11 = App.activeDocument().getObject("Note_B").Text[0]
    except:
        lineEdit11 = ""
    try:
        lineEdit10 = App.activeDocument().getObject("Note_A").Text[0]
    except:
        lineEdit10 = ""
    try:
        lineEdit20 = App.activeDocument().getObject("CopyRight").Text[0]
    except:
        lineEdit20 = ""
except:
    errorDialog("erreur note")

class Ui_MainWindow(object):

    def __init__(self, MainWindow):
        self.window = MainWindow
#___________________________________________________________________________________

        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(810, 440)
        MainWindow.setMaximumSize(QtCore.QSize(810, 480))
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))

#        self.pushButton01 = QtGui.QPushButton(self.centralWidget)
#        self.pushButton01.setGeometry(QtCore.QRect(115, 360, 93, 28))
#        self.pushButton01.setObjectName(_fromUtf8("pushButton01"))
#        self.pushButton01.clicked.connect(self.on_pushButton01_clicked) #connection pushButton01

        self.pushButton02 = QtGui.QPushButton(self.centralWidget)
        self.pushButton02.setGeometry(QtCore.QRect(225, 360, 93, 28))
        self.pushButton02.setObjectName(_fromUtf8("pushButton02"))
        self.pushButton02.clicked.connect(self.on_pushButton02_clicked) #connection pushButton02

        self.pushButton03 = QtGui.QPushButton(self.centralWidget)
        self.pushButton03.setGeometry(QtCore.QRect(335, 360, 93, 28))
        self.pushButton03.setObjectName(_fromUtf8("pushButton03"))
        self.pushButton03.clicked.connect(self.on_pushButton03_clicked) #connection pushButton03

        self.pushButton04 = QtGui.QPushButton(self.centralWidget)
        self.pushButton04.setGeometry(QtCore.QRect(445, 360, 93, 28))
        self.pushButton04.setObjectName(_fromUtf8("pushButton04"))
        self.pushButton04.clicked.connect(self.on_pushButton04_clicked) #connection pushButton04

        self.pushButton05 = QtGui.QPushButton(self.centralWidget)
        self.pushButton05.setGeometry(QtCore.QRect(555, 360, 93, 28))
        self.pushButton05.setObjectName(_fromUtf8("pushButton05"))
        self.pushButton05.clicked.connect(self.on_pushButton05_clicked) #connection pushButton05

        self.pushButton06 = QtGui.QPushButton(self.centralWidget)
        self.pushButton06.setGeometry(QtCore.QRect(170, 56, 20, 20))
        self.pushButton06.setObjectName(_fromUtf8("pushButton06"))
        self.pushButton06.clicked.connect(self.on_pushButton06_clicked) #connection pushButton06

        self.pushButton07 = QtGui.QPushButton(self.centralWidget)
        self.pushButton07.setGeometry(QtCore.QRect(190, 56, 20, 20))
        self.pushButton07.setObjectName(_fromUtf8("pushButton07"))
        self.pushButton07.clicked.connect(self.on_pushButton07_clicked) #connection pushButton07

        self.pushButton08 = QtGui.QPushButton(self.centralWidget)
        self.pushButton08.setGeometry(QtCore.QRect(170, 136, 20, 20))
        self.pushButton08.setObjectName(_fromUtf8("pushButton08"))
        self.pushButton08.clicked.connect(self.on_pushButton08_clicked) #connection pushButton08

        self.pushButton09 = QtGui.QPushButton(self.centralWidget)
        self.pushButton09.setGeometry(QtCore.QRect(190, 136, 20, 20))
        self.pushButton09.setObjectName(_fromUtf8("pushButton09"))
        self.pushButton09.clicked.connect(self.on_pushButton09_clicked) #connection pushButton09

        self.pushButton10 = QtGui.QPushButton(self.centralWidget)
        self.pushButton10.setGeometry(QtCore.QRect(100, 220, 101, 20))
        self.pushButton10.setObjectName(_fromUtf8("pushButton10"))
        self.pushButton10.clicked.connect(self.on_pushButton10_clicked) #connection pushButton10

        self.lineEdit_01 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_01.setGeometry(QtCore.QRect(20, 20, 181, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.lineEdit_01.setFont(font)
        self.lineEdit_01.setObjectName(_fromUtf8("lineEdit_01"))
        self.lineEdit_01.setText(DESIGNED_BY)

        self.lineEdit_02 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_02.setGeometry(QtCore.QRect(20, 60, 82, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.lineEdit_02.setFont(font)
        self.lineEdit_02.setObjectName(_fromUtf8("lineEdit_02"))
        self.lineEdit_02.setText(CREA_DATE)

        self.lineEdit_02h = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_02h.setGeometry(QtCore.QRect(98, 60, 72, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.lineEdit_02h.setFont(font)
        self.lineEdit_02h.setObjectName(_fromUtf8("lineEdit_02h"))
        self.lineEdit_02h.setText(CREA_TIME)

        self.lineEdit_03 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_03.setGeometry(QtCore.QRect(20, 100, 181, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.lineEdit_03.setFont(font)
        self.lineEdit_03.setObjectName(_fromUtf8("lineEdit_03"))
        self.lineEdit_03.setText(CHECKED_BY)

        self.lineEdit_04 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_04.setGeometry(QtCore.QRect(20, 140, 82, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.lineEdit_04.setFont(font)
        self.lineEdit_04.setObjectName(_fromUtf8("lineEdit_04"))
        self.lineEdit_04.setText(CHEC_DATE)

        self.lineEdit_04h = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_04h.setGeometry(QtCore.QRect(98, 140, 72, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.lineEdit_04h.setFont(font)
        self.lineEdit_04h.setObjectName(_fromUtf8("lineEdit_04h"))
        self.lineEdit_04h.setText(CHEC_TIME)

        self.lineEdit_05 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_05.setGeometry(QtCore.QRect(20, 180, 61, 61))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_05.setFont(font)
        self.lineEdit_05.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_05.setObjectName(_fromUtf8("lineEdit_05"))
        self.lineEdit_05.setText(SIZE)

        self.lineEdit_06 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_06.setGeometry(QtCore.QRect(20, 280, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_06.setFont(font)
        self.lineEdit_06.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_06.setObjectName(_fromUtf8("lineEdit_06"))
        self.lineEdit_06.setText(SCALE)

        self.lineEdit_07 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_07.setGeometry(QtCore.QRect(100, 280, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_07.setFont(font)
        self.lineEdit_07.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_07.setObjectName(_fromUtf8("lineEdit_07"))
        self.lineEdit_07.setText(WEIGHT)

        self.lineEdit_08 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_08.setGeometry(QtCore.QRect(220, 280, 341, 41))
        self.lineEdit_08.setObjectName(_fromUtf8("lineEdit_08"))
        self.lineEdit_08.setText(DRAWING_NUMBER)

        self.lineEdit_09 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_09.setGeometry(QtCore.QRect(570, 280, 81, 41))
        self.lineEdit_09.setObjectName(_fromUtf8("lineEdit_09"))
        self.lineEdit_09.setText(SHEET)

        self.lineEdit_10 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_10.setGeometry(QtCore.QRect(690, 290, 101, 30))
        self.lineEdit_10.setObjectName(_fromUtf8("lineEdit_10"))
        self.lineEdit_10.setText(lineEdit10)

        self.lineEdit_11 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_11.setGeometry(QtCore.QRect(690, 260, 101, 30))
        self.lineEdit_11.setObjectName(_fromUtf8("lineEdit_11"))
        self.lineEdit_11.setText(lineEdit11)

        self.lineEdit_12 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_12.setGeometry(QtCore.QRect(690, 230, 101, 30))
        self.lineEdit_12.setObjectName(_fromUtf8("lineEdit_12"))
        self.lineEdit_12.setText(lineEdit12)

        self.lineEdit_13 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_13.setGeometry(QtCore.QRect(690, 200, 101, 30))
        self.lineEdit_13.setObjectName(_fromUtf8("lineEdit_13"))
        self.lineEdit_13.setText(lineEdit13)

        self.lineEdit_14 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_14.setGeometry(QtCore.QRect(690, 170, 101, 30))
        self.lineEdit_14.setObjectName(_fromUtf8("lineEdit_14"))
        self.lineEdit_14.setText(lineEdit14)

        self.lineEdit_15 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_15.setGeometry(QtCore.QRect(690, 140, 101, 30))
        self.lineEdit_15.setObjectName(_fromUtf8("lineEdit_15"))
        self.lineEdit_15.setText(lineEdit15)

        self.lineEdit_16 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_16.setGeometry(QtCore.QRect(690, 110, 101, 30))
        self.lineEdit_16.setObjectName(_fromUtf8("lineEdit_16"))
        self.lineEdit_16.setText(lineEdit16)

        self.lineEdit_17 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_17.setGeometry(QtCore.QRect(690, 80, 101, 30))
        self.lineEdit_17.setObjectName(_fromUtf8("lineEdit_17"))
        self.lineEdit_17.setText(lineEdit17)

        self.lineEdit_18 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_18.setGeometry(QtCore.QRect(690, 50, 101, 30))
        self.lineEdit_18.setObjectName(_fromUtf8("lineEdit_18"))
        self.lineEdit_18.setText(lineEdit18)

        self.lineEdit_20 = QtGui.QLineEdit(self.centralWidget) # Copyright
        self.lineEdit_20.setGeometry(QtCore.QRect(20, 330, 771, 22))
        self.lineEdit_20.setObjectName(_fromUtf8("lineEdit_20"))
        self.lineEdit_20.setText(lineEdit20)

        self.textEdit_01 = QtGui.QTextEdit(self.centralWidget)
        self.textEdit_01.setGeometry(QtCore.QRect(220, 20, 431,60 ))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_01.setFont(font)
        self.textEdit_01.setObjectName(_fromUtf8("textEdit_01"))
        self.textEdit_01.setText(TITLE)

        self.textEdit_02 = QtGui.QTextEdit(self.centralWidget)
        self.textEdit_02.setGeometry(QtCore.QRect(220, 90, 431, 60))
        self.textEdit_02.setObjectName(_fromUtf8("textEdit_02"))
        self.textEdit_02.setText(DESCRIPTION)

#        self.graphicsView_01 = QtGui.QGraphicsView(self.centralWidget)
#        self.graphicsView_01.setGeometry(QtCore.QRect(100, 160, 101, 81))
#        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
#        brush.setStyle(QtCore.Qt.NoBrush)
#        self.graphicsView_01.setBackgroundBrush(brush)
#        self.graphicsView_01.setObjectName(_fromUtf8("graphicsView_01"))

        self.textEdit_03 = QtGui.QTextEdit(self.centralWidget)
        self.textEdit_03.setGeometry(QtCore.QRect(100, 160, 101, 55))
        self.textEdit_03.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_03.setObjectName(_fromUtf8("textEdit_03"))
        self.textEdit_03.setText("Select your Symbol")

        self.graphicsView_02 = QtGui.QGraphicsView(self.centralWidget)
        self.graphicsView_02.setGeometry(QtCore.QRect(220, 160, 431, 81))#570, 160, 81, 81
        self.graphicsView_02.setObjectName(_fromUtf8("graphicsView_02"))

        self.label_01 = QtGui.QLabel(self.centralWidget)
        self.label_01.setGeometry(QtCore.QRect(20, 0, 91, 16))
        self.label_01.setObjectName(_fromUtf8("label_01"))

        self.label_02 = QtGui.QLabel(self.centralWidget)
        self.label_02.setGeometry(QtCore.QRect(20, 40, 53, 16))
        self.label_02.setObjectName(_fromUtf8("label_02"))

        self.label_03 = QtGui.QLabel(self.centralWidget)
        self.label_03.setGeometry(QtCore.QRect(20, 80, 101, 16))
        self.label_03.setObjectName(_fromUtf8("label_03"))

        self.label_04 = QtGui.QLabel(self.centralWidget)
        self.label_04.setGeometry(QtCore.QRect(20, 120, 91, 16))
        self.label_04.setObjectName(_fromUtf8("label_04"))

        self.label_05 = QtGui.QLabel(self.centralWidget)
        self.label_05.setGeometry(QtCore.QRect(20, 160, 53, 16))
        self.label_05.setObjectName(_fromUtf8("label_05"))

        self.label_06 = QtGui.QLabel(self.centralWidget)
        self.label_06.setGeometry(QtCore.QRect(20, 260, 53, 16))
        self.label_06.setObjectName(_fromUtf8("label_06"))

        self.label_07 = QtGui.QLabel(self.centralWidget)
        self.label_07.setGeometry(QtCore.QRect(100, 260, 101, 16))
        self.label_07.setObjectName(_fromUtf8("label_07"))

        self.label_08 = QtGui.QLabel(self.centralWidget)
        self.label_08.setGeometry(QtCore.QRect(220, 260, 121, 16))
        self.label_08.setObjectName(_fromUtf8("label_08"))

        self.label_09 = QtGui.QLabel(self.centralWidget)
        self.label_09.setGeometry(QtCore.QRect(570, 260, 53, 16))
        self.label_09.setObjectName(_fromUtf8("label_09"))

        self.label_10 = QtGui.QLabel(self.centralWidget)
        self.label_10.setGeometry(QtCore.QRect(670, 290, 16, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))

        self.label_11 = QtGui.QLabel(self.centralWidget)
        self.label_11.setGeometry(QtCore.QRect(670, 260, 16, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))

        self.label_12 = QtGui.QLabel(self.centralWidget)
        self.label_12.setGeometry(QtCore.QRect(670, 230, 16, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))

        self.label_13 = QtGui.QLabel(self.centralWidget)
        self.label_13.setGeometry(QtCore.QRect(670, 200, 18, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))

        self.label_14 = QtGui.QLabel(self.centralWidget)
        self.label_14.setGeometry(QtCore.QRect(670, 170, 15, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))

        self.label_15 = QtGui.QLabel(self.centralWidget)
        self.label_15.setGeometry(QtCore.QRect(670, 140, 14, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName(_fromUtf8("label_15"))

        self.label_16 = QtGui.QLabel(self.centralWidget)
        self.label_16.setGeometry(QtCore.QRect(670, 110, 18, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName(_fromUtf8("label_16"))

        self.label_17 = QtGui.QLabel(self.centralWidget)
        self.label_17.setGeometry(QtCore.QRect(670, 80, 18, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName(_fromUtf8("label_17"))

        self.label_18 = QtGui.QLabel(self.centralWidget)
        self.label_18.setGeometry(QtCore.QRect(670, 50, 10, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName(_fromUtf8("label_18"))

        self.label_19 = QtGui.QLabel(self.centralWidget)
        self.label_19.setGeometry(QtCore.QRect(720, 15, 100, 33))
        self.label_19.setObjectName(_fromUtf8("label_19"))

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 810, 26))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        try:
            MainWindow.setWindowFlags(PyQt4.QtCore.Qt.WindowStaysOnTopHint)  # PyQt4 cette fonction met la fenêtre en avant
        except Exception:
            MainWindow.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint) # PySide cette fonction met la fenêtre en avant

        MainWindow.setWindowTitle(_translate("MainWindow", "Cartouche", None))
#        self.pushButton01.setText(_translate("MainWindow", "Position", None))
        self.pushButton02.setText(_translate("MainWindow", "Quitter", None))
        self.pushButton03.setText(_translate("MainWindow", "Memo", None))
        self.pushButton04.setText(_translate("MainWindow", "Nettoyer", None))
        self.pushButton05.setText(_translate("MainWindow", "Appliquer", None))
        self.pushButton06.setText(_translate("MainWindow", "D.", None))
        self.pushButton07.setText(_translate("MainWindow", "H.", None))
        self.pushButton08.setText(_translate("MainWindow", "D.", None))
        self.pushButton09.setText(_translate("MainWindow", "H.", None))
        self.pushButton10.setText(_translate("MainWindow", "Symbole EU", None))


        self.label_01.setText(_translate("MainWindow", "Designed by :", None))
        self.label_02.setText(_translate("MainWindow", "Date :", None))
        self.label_03.setText(_translate("MainWindow", "Checked by :", None))
        self.label_04.setText(_translate("MainWindow", "Date :", None))
        self.label_05.setText(_translate("MainWindow", "Size :", None))
        self.label_06.setText(_translate("MainWindow", "Scale :", None))
        self.label_07.setText(_translate("MainWindow", "Weight (Kg) :", None))
        self.label_08.setText(_translate("MainWindow", "Drawing number :", None))
        self.label_09.setText(_translate("MainWindow", "Sheet :", None))
        self.label_10.setText(_translate("MainWindow", "A", None))
        self.label_11.setText(_translate("MainWindow", "B", None))
        self.label_12.setText(_translate("MainWindow", "C", None))
        self.label_13.setText(_translate("MainWindow", "D", None))
        self.label_14.setText(_translate("MainWindow", "E", None))
        self.label_15.setText(_translate("MainWindow", "F", None))
        self.label_16.setText(_translate("MainWindow", "G", None))
        self.label_17.setText(_translate("MainWindow", "H", None))
        self.label_18.setText(_translate("MainWindow", "I", None))
        self.label_19.setText(_translate("MainWindow", "Notes", None))
#______________________________________________________________________________________
    # Boutons
    def on_pushButton10_clicked(self):    # Bouton /Symbole
        if self.textEdit_03.toPlainText()=="Symbole US":
            self.pushButton10.setText(_translate("MainWindow", "Symbole US", None))
            self.textEdit_03.setText("Symbole EU")
            symbol_EU(247.5,263.5) #(247.5,263.5)
        else:
            self.pushButton10.setText(_translate("MainWindow", "Symbole EU", None))
            self.textEdit_03.setText("Symbole US")
            symbol_US(247.5,263.5) #(247.5,263.5)
    def on_pushButton09_clicked(self):    # Bouton /heure document
        self.lineEdit_04h.setText(str(heure()))
    def on_pushButton08_clicked(self):    # Bouton date/ document
        if self.textEdit_03.toPlainText()=="Symbole US":
            self.lineEdit_04.setText(str(dateUs()))
        else:
            self.lineEdit_04.setText(str(dateEu()))
    def on_pushButton07_clicked(self):    # Bouton /heure checked
        self.lineEdit_02h.setText(str(heure()))
    def on_pushButton06_clicked(self):    # Bouton date/ checked
        if self.textEdit_03.toPlainText()=="Symbole US":
            self.lineEdit_02.setText(str(dateUs()))
        else:
            self.lineEdit_02.setText(str(dateEu()))
    def on_pushButton05_clicked(self):    # Bouton Appliquer
        DESIGNED_BY = self.lineEdit_01.text()    
        CREATION_DATE = self.lineEdit_02.text()+" - "+self.lineEdit_02h.text()
        CHECKED_BY = self.lineEdit_03.text()
        CHECK_DATE = self.lineEdit_04.text()+" - "+self.lineEdit_04h.text()
        SIZE  = "A3" # self.lineEdit_05.text()
        SCALE = self.lineEdit_06.text()
        WEIGHT = self.lineEdit_07.text()
        DRAWING_NUMBER = self.lineEdit_08.text()
        SHEET = self.lineEdit_09.text()
        TITLE = self.textEdit_01.toPlainText()
        DESCRIPTION = self.textEdit_02.toPlainText()
        SYMBOL = self.textEdit_03.toPlainText()
        try:
            FreeCAD.getDocument (App.ActiveDocument.Name).getObject("Page").EditableTexts = [unicode(DESIGNED_BY, 'utf-8'), unicode(CREATION_DATE, 'utf-8'), unicode(CHECKED_BY, 'utf-8'), unicode(CHECK_DATE, 'utf-8'), unicode(SCALE, 'utf-8'), unicode(WEIGHT, 'utf-8'), unicode(DRAWING_NUMBER, 'utf-8'), unicode(SHEET, 'utf-8'), unicode(TITLE, 'utf-8'), unicode(DESCRIPTION, 'utf-8'),]
        except Exception:
            FreeCAD.getDocument (App.ActiveDocument.Name).getObject("Page").EditableTexts = [DESIGNED_BY.encode('utf-8'), CREATION_DATE.encode('utf-8'), CHECKED_BY.encode('utf-8'), CHECK_DATE.encode('utf-8'), SCALE.encode('utf-8'), WEIGHT.encode('utf-8'), DRAWING_NUMBER.encode('utf-8'), SHEET.encode('utf-8'), TITLE.encode('utf-8'), DESCRIPTION.encode('utf-8'),]

        #print App.ActiveDocument.Name
        try:
            App.activeDocument().removeObject('Note_I')
        except:
            None
        try:
            App.activeDocument().removeObject('Note_H')
        except:
            None
        try:
            App.activeDocument().removeObject('Note_G')
        except:
            None
        try:
            App.activeDocument().removeObject('Note_F')
        except:
            None
        try:
            App.activeDocument().removeObject('Note_E')
        except:
            None
        try:
            App.activeDocument().removeObject('Note_D')
        except:
            None
        try:
            App.activeDocument().removeObject('Note_C')
        except:
            None
        try:
            App.activeDocument().removeObject('Note_B')
        except:
            None
        try:
            App.activeDocument().removeObject('Note_A')
        except:
            None
        try:
            App.activeDocument().removeObject('CopyRight')
        except:
            None
        if self.lineEdit_18.text() != "":
            App.activeDocument().addObject('Drawing::FeatureViewAnnotation','Note_I')
            App.activeDocument().Note_I.X = 391.0
            App.activeDocument().Note_I.Y = 232
            App.activeDocument().Note_I.Scale = 3.0
            App.activeDocument().Note_I.Text = str(self.lineEdit_18.text())
            App.activeDocument().Page.addObject(App.activeDocument().Note_I)
        if self.lineEdit_17.text() != "":
            App.activeDocument().addObject('Drawing::FeatureViewAnnotation','Note_H')
            App.activeDocument().Note_H.X = 391.0
            App.activeDocument().Note_H.Y = 238.8
            App.activeDocument().Note_H.Scale = 3.0
            App.activeDocument().Note_H.Text = str(self.lineEdit_17.text())
            App.activeDocument().Page.addObject(App.activeDocument().Note_H)
        if self.lineEdit_16.text() != "":
            App.activeDocument().addObject('Drawing::FeatureViewAnnotation','Note_G')
            App.activeDocument().Note_G.X = 391.0
            App.activeDocument().Note_G.Y = 245.4
            App.activeDocument().Note_G.Scale = 3.0
            App.activeDocument().Note_G.Text = str(self.lineEdit_16.text())
            App.activeDocument().Page.addObject(App.activeDocument().Note_G)
        if self.lineEdit_15.text() != "":
            App.activeDocument().addObject('Drawing::FeatureViewAnnotation','Note_F')
            App.activeDocument().Note_F.X = 391.0
            App.activeDocument().Note_F.Y = 252
            App.activeDocument().Note_F.Scale = 3.0
            App.activeDocument().Note_F.Text = str(self.lineEdit_15.text())
            App.activeDocument().Page.addObject(App.activeDocument().Note_F)
        if self.lineEdit_14.text() != "":
            App.activeDocument().addObject('Drawing::FeatureViewAnnotation','Note_E')
            App.activeDocument().Note_E.X = 391.0
            App.activeDocument().Note_E.Y = 258.6
            App.activeDocument().Note_E.Scale = 3.0
            App.activeDocument().Note_E.Text = str(self.lineEdit_14.text())
            App.activeDocument().Page.addObject(App.activeDocument().Note_E)
        if self.lineEdit_13.text() != "":
            App.activeDocument().addObject('Drawing::FeatureViewAnnotation','Note_D')
            App.activeDocument().Note_D.X = 391.0
            App.activeDocument().Note_D.Y = 265.2
            App.activeDocument().Note_D.Scale = 3.0
            App.activeDocument().Note_D.Text = str(self.lineEdit_13.text())
            App.activeDocument().Page.addObject(App.activeDocument().Note_D)
        if self.lineEdit_12.text() != "":
            App.activeDocument().addObject('Drawing::FeatureViewAnnotation','Note_C')
            App.activeDocument().Note_C.X = 391.0
            App.activeDocument().Note_C.Y = 271.8
            App.activeDocument().Note_C.Scale = 3.0
            App.activeDocument().Note_C.Text =  str(self.lineEdit_12.text())
            App.activeDocument().Page.addObject(App.activeDocument().Note_C)
        if self.lineEdit_11.text() != "":
            App.activeDocument().addObject('Drawing::FeatureViewAnnotation','Note_B')
            App.activeDocument().Note_B.X = 391.0
            App.activeDocument().Note_B.Y = 278.4
            App.activeDocument().Note_B.Scale = 3.0
            App.activeDocument().Note_B.Text = str(self.lineEdit_11.text())
            App.activeDocument().Page.addObject(App.activeDocument().Note_B)
        if self.lineEdit_10.text() != "":
            App.activeDocument().addObject('Drawing::FeatureViewAnnotation','Note_A')
            App.activeDocument().Note_A.X = 391.0
            App.activeDocument().Note_A.Y = 285.0
            App.activeDocument().Note_A.Scale = 3.0
            App.activeDocument().Note_A.Text = str(self.lineEdit_10.text())
            App.activeDocument().Page.addObject(App.activeDocument().Note_A)
        if self.lineEdit_20.text() != "":
            App.activeDocument().addObject('Drawing::FeatureViewAnnotation','CopyRight')
            App.activeDocument().CopyRight.X = 221
            App.activeDocument().CopyRight.Y = 286
            App.activeDocument().CopyRight.Scale = 3.0
            App.activeDocument().CopyRight.Text = str(self.lineEdit_20.text())
            App.activeDocument().Page.addObject(App.activeDocument().CopyRight)

        App.ActiveDocument.recompute()

    def on_pushButton04_clicked(self):    # Bouton nettoyer
        try:
            App.getDocument(App.ActiveDocument.Name).removeObject("Symbol_US")
        except:
            None
        try:
            App.getDocument(App.ActiveDocument.Name).removeObject("Symbol_EU")
        except:
            None
        try:
            App.getDocument(App.ActiveDocument.Name).removeObject("SymbolUS")
        except:
            None
        try:
            App.getDocument(App.ActiveDocument.Name).removeObject("SymbolEU")
        except:
            None
        DESIGNED_BY = ""    ;self.lineEdit_01.setText("")
        CREATION_DATE = ""  ;self.lineEdit_02.setText("")
        self.lineEdit_02h.setText("")
        CHECKED_BY = ""     ;self.lineEdit_03.setText("")
        CHECK_DATE = ""     ;self.lineEdit_04.setText("")
        self.lineEdit_04h.setText("")
        SIZE  = "A3"        ;self.lineEdit_05.setText("A3")
        SCALE = ""          ;self.lineEdit_06.setText("")
        WEIGHT = ""         ;self.lineEdit_07.setText("")
        DRAWING_NUMBER = "" ;self.lineEdit_08.setText("")
        SHEET = ""          ;self.lineEdit_09.setText("")
        TITLE = ""          ;self.textEdit_01.setText("")
        DESCRIPTION = ""    ;self.textEdit_02.setText("")

        self.lineEdit_10.setText("")
        self.lineEdit_11.setText("")
        self.lineEdit_12.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_16.setText("")
        self.lineEdit_17.setText("")
        self.lineEdit_18.setText("")
        self.lineEdit_20.setText("")

    def on_pushButton03_clicked(self):    # Bouton Memo
        self.lineEdit_01.setText(DESIGNED_BY)
        self.lineEdit_02.setText(CREA_DATE)
        self.lineEdit_02h.setText(CREA_TIME)
        self.lineEdit_03.setText(CHECKED_BY)
        self.lineEdit_04.setText(CHEC_DATE)
        self.lineEdit_04h.setText(CHEC_TIME)
        self.lineEdit_05.setText(SIZE)
        self.lineEdit_06.setText(SCALE)
        self.lineEdit_07.setText(WEIGHT)
        self.lineEdit_08.setText(DRAWING_NUMBER)
        self.lineEdit_09.setText(SHEET)
        self.textEdit_01.setText(TITLE)
        self.textEdit_02.setText(DESCRIPTION)

        self.lineEdit_18.setText(lineEdit18)
        self.lineEdit_17.setText(lineEdit17)
        self.lineEdit_16.setText(lineEdit16)
        self.lineEdit_15.setText(lineEdit15)
        self.lineEdit_14.setText(lineEdit14)
        self.lineEdit_13.setText(lineEdit13)
        self.lineEdit_12.setText(lineEdit12)
        self.lineEdit_11.setText(lineEdit11)
        self.lineEdit_10.setText(lineEdit10)
        self.lineEdit_20.setText(lineEdit20)

    def on_pushButton02_clicked(self):    # Bouton Quitter
        App.Console.PrintMessage("Terminé\r\n")
        self.window.hide()
#    def on_pushButton01_clicked(self):    # Bouton appel de Position
#        MainWindow.resize(210, 480)
#        executer()
#        MainWindow.resize(810, 480)
#______________________________________________________________________________________

MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow(MainWindow)
MainWindow.show()
