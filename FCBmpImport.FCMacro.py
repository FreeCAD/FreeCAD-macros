# -*- coding: utf-8 -*-
"""
***************************************************************************
*   Copyright (c) 2018 <TheMarkster>                                      *
*                                                                         *
*   This file is a supplement to the FreeCAD CAx development system.      *
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU Lesser General Public License (LGPL)    *
*   as published by the Free Software Foundation; either version 2 of     *
*   the License, or (at your option) any later version.                   *
*                                                                         *
*   This software is distributed in the hope that it will be useful,      *
*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
*   GNU Library General Public License at http://www.gnu.org/licenses     *
*   for more details.                                                     *
*                                                                         *
*   For more information about the GNU Library General Public License     *
*   write to the Free Software Foundation, Inc., 59 Temple Place,         *
*   Suite 330, Boston, MA  02111-1307 USA                                 *
*                                                                         *
***************************************************************************
"""

#OS: Windows 10
#Word size of OS: 64-bit
#Word size of FreeCAD: 64-bit
#Version: 0.17.13509 (Git)
#Build type: Release
#Branch: releases/FreeCAD-0-17
#Hash: 0258808ccb6ba3bd5ea9312f79cd023f1a8671b7
#Python version: 2.7.14
#Qt version: 4.8.7
#Coin version: 4.0.0a
#OCC version: 7.2.0
#Locale: English/UnitedStates (en_US)

__title__ = "FCBmpImport"
__author__ = "TheMarkster"
__url__ = "http://www.freecadweb.org/"
__Wiki__ = "http://www.freecadweb.org/wiki/index.php"
__date__ = "2018.05.17" #year.month.date and optional a,b,c, etc. subrevision letter, e.g. 2018.10.16a
__version__ = "0."+__date__

VERSION_STRING = __title__ + ' Macro v' + __version__

#Translators: Do not modify any text except in the translation section
#which follows the QT Designer produced code
import FreeCAD
import Part
from FreeCAD import Base
import struct
import math
from time import sleep
from PySide import QtCore, QtGui
import sys
from itertools import groupby
import PartGui
import base64
import ast
import operator as op
import Mesh
import Draft
import OpenSCADUtils
import locale
import re



#from QTDesigner via PySide uic.py
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(591, 493)
        MainWindow.setDockNestingEnabled(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.imagePreviewLabel = QtGui.QLabel(self.centralwidget)
        self.imagePreviewLabel.setGeometry(QtCore.QRect(180, 0, 401, 20))
        self.imagePreviewLabel.setObjectName("imagePreviewLabel")
        self.verticalGroupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.verticalGroupBox_2.setGeometry(QtCore.QRect(410, 340, 171, 131))
        self.verticalGroupBox_2.setObjectName("verticalGroupBox_2")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalGroupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.previewButton = QtGui.QPushButton(self.verticalGroupBox_2)
        self.previewButton.setObjectName("previewButton")
        self.verticalLayout.addWidget(self.previewButton)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.importAsShapeButton = QtGui.QPushButton(self.verticalGroupBox_2)
        self.importAsShapeButton.setFlat(False)
        self.importAsShapeButton.setObjectName("importAsShapeButton")
        self.horizontalLayout_5.addWidget(self.importAsShapeButton)
        self.importAsMeshButton = QtGui.QPushButton(self.verticalGroupBox_2)
        self.importAsMeshButton.setObjectName("importAsMeshButton")
        self.horizontalLayout_5.addWidget(self.importAsMeshButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.importAsSolidButton = QtGui.QPushButton(self.verticalGroupBox_2)
        self.importAsSolidButton.setObjectName("importAsSolidButton")
        self.horizontalLayout_4.addWidget(self.importAsSolidButton)
        self.importAsSketchButton = QtGui.QPushButton(self.verticalGroupBox_2)
        self.importAsSketchButton.setObjectName("importAsSketchButton")
        self.horizontalLayout_4.addWidget(self.importAsSketchButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.importAsFaceButton = QtGui.QPushButton(self.verticalGroupBox_2)
        self.importAsFaceButton.setObjectName("importAsFaceButton")
        self.horizontalLayout_2.addWidget(self.importAsFaceButton)
        self.importAsWireButton = QtGui.QPushButton(self.verticalGroupBox_2)
        self.importAsWireButton.setObjectName("importAsWireButton")
        self.horizontalLayout_2.addWidget(self.importAsWireButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.offsetsGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.offsetsGroupBox.setGeometry(QtCore.QRect(10, 339, 391, 131))
        self.offsetsGroupBox.setTitle("")
        self.offsetsGroupBox.setObjectName("offsetsGroupBox")
        self.gridLayout = QtGui.QGridLayout(self.offsetsGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scaleLabel = QtGui.QLabel(self.offsetsGroupBox)
        self.scaleLabel.setObjectName("scaleLabel")
        self.verticalLayout_3.addWidget(self.scaleLabel)
        self.xOffsetLabel = QtGui.QLabel(self.offsetsGroupBox)
        self.xOffsetLabel.setObjectName("xOffsetLabel")
        self.verticalLayout_3.addWidget(self.xOffsetLabel)
        self.yOffsetLabel = QtGui.QLabel(self.offsetsGroupBox)
        self.yOffsetLabel.setObjectName("yOffsetLabel")
        self.verticalLayout_3.addWidget(self.yOffsetLabel)
        self.zOffsetLabel = QtGui.QLabel(self.offsetsGroupBox)
        self.zOffsetLabel.setObjectName("zOffsetLabel")
        self.verticalLayout_3.addWidget(self.zOffsetLabel)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scaleEdit = QtGui.QLineEdit(self.offsetsGroupBox)
        self.scaleEdit.setObjectName("scaleEdit")
        self.verticalLayout_4.addWidget(self.scaleEdit)
        self.xOffsetEdit = QtGui.QLineEdit(self.offsetsGroupBox)
        self.xOffsetEdit.setObjectName("xOffsetEdit")
        self.verticalLayout_4.addWidget(self.xOffsetEdit)
        self.yOffsetEdit = QtGui.QLineEdit(self.offsetsGroupBox)
        self.yOffsetEdit.setToolTip("")
        self.yOffsetEdit.setObjectName("yOffsetEdit")
        self.verticalLayout_4.addWidget(self.yOffsetEdit)
        self.zOffsetEdit = QtGui.QLineEdit(self.offsetsGroupBox)
        self.zOffsetEdit.setToolTip("")
        self.zOffsetEdit.setObjectName("zOffsetEdit")
        self.verticalLayout_4.addWidget(self.zOffsetEdit)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.baseNameEdit = QtGui.QLineEdit(self.offsetsGroupBox)
        self.baseNameEdit.setObjectName("baseNameEdit")
        self.verticalLayout_8.addWidget(self.baseNameEdit)
        self.shapeHeightEdit = QtGui.QLineEdit(self.offsetsGroupBox)
        self.shapeHeightEdit.setObjectName("shapeHeightEdit")
        self.verticalLayout_8.addWidget(self.shapeHeightEdit)
        self.recomputeIntervalEdit = QtGui.QLineEdit(self.offsetsGroupBox)
        self.recomputeIntervalEdit.setToolTip("")
        self.recomputeIntervalEdit.setObjectName("recomputeIntervalEdit")
        self.verticalLayout_8.addWidget(self.recomputeIntervalEdit)
        self.cheatFactorEdit = QtGui.QLineEdit(self.offsetsGroupBox)
        self.cheatFactorEdit.setObjectName("cheatFactorEdit")
        self.verticalLayout_8.addWidget(self.cheatFactorEdit)
        self.gridLayout.addLayout(self.verticalLayout_8, 0, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.baseNameLabel = QtGui.QLabel(self.offsetsGroupBox)
        self.baseNameLabel.setObjectName("baseNameLabel")
        self.verticalLayout_7.addWidget(self.baseNameLabel)
        self.shapeHeightLabel = QtGui.QLabel(self.offsetsGroupBox)
        self.shapeHeightLabel.setObjectName("shapeHeightLabel")
        self.verticalLayout_7.addWidget(self.shapeHeightLabel)
        self.recomputeIntervalLabel = QtGui.QLabel(self.offsetsGroupBox)
        self.recomputeIntervalLabel.setObjectName("recomputeIntervalLabel")
        self.verticalLayout_7.addWidget(self.recomputeIntervalLabel)
        self.cheatFactorLabel = QtGui.QLabel(self.offsetsGroupBox)
        self.cheatFactorLabel.setObjectName("cheatFactorLabel")
        self.verticalLayout_7.addWidget(self.cheatFactorLabel)
        self.gridLayout.addLayout(self.verticalLayout_7, 0, 3, 1, 1)
        self.progressGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.progressGroupBox.setGeometry(QtCore.QRect(10, 60, 161, 91))
        self.progressGroupBox.setTitle("")
        self.progressGroupBox.setObjectName("progressGroupBox")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.progressGroupBox)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.progressLabel = QtGui.QLabel(self.progressGroupBox)
        self.progressLabel.setObjectName("progressLabel")
        self.verticalLayout_6.addWidget(self.progressLabel)
        self.progressBar = QtGui.QProgressBar(self.progressGroupBox)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_6.addWidget(self.progressBar)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.abortButton = QtGui.QPushButton(self.progressGroupBox)
        self.abortButton.setObjectName("abortButton")
        self.horizontalLayout_3.addWidget(self.abortButton)
        self.exitButton = QtGui.QPushButton(self.progressGroupBox)
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout_3.addWidget(self.exitButton)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.staysOnTopCheckBox = QtGui.QCheckBox(self.centralwidget)
        self.staysOnTopCheckBox.setGeometry(QtCore.QRect(10, 10, 151, 17))
        self.staysOnTopCheckBox.setObjectName("staysOnTopCheckBox")
        self.wireEditGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.wireEditGroupBox.setGeometry(QtCore.QRect(10, 190, 160, 80))
        self.wireEditGroupBox.setObjectName("wireEditGroupBox")
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.wireEditGroupBox)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.selectOddPointsButton = QtGui.QPushButton(self.wireEditGroupBox)
        self.selectOddPointsButton.setObjectName("selectOddPointsButton")
        self.horizontalLayout_7.addWidget(self.selectOddPointsButton)
        self.cutSelectedButton = QtGui.QPushButton(self.wireEditGroupBox)
        self.cutSelectedButton.setObjectName("cutSelectedButton")
        self.horizontalLayout_7.addWidget(self.cutSelectedButton)
        self.verticalLayout_9.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.moveButton = QtGui.QPushButton(self.wireEditGroupBox)
        self.moveButton.setObjectName("moveButton")
        self.horizontalLayout_8.addWidget(self.moveButton)
        self.insertButton = QtGui.QPushButton(self.wireEditGroupBox)
        self.insertButton.setObjectName("insertButton")
        self.horizontalLayout_8.addWidget(self.insertButton)
        self.verticalLayout_9.addLayout(self.horizontalLayout_8)
        self.blackForegroundCheckbox = QtGui.QCheckBox(self.centralwidget)
        self.blackForegroundCheckbox.setGeometry(QtCore.QRect(10, 30, 140, 21))
        self.blackForegroundCheckbox.setObjectName("blackForegroundCheckbox")
        self.selectFacesButton = QtGui.QPushButton(self.centralwidget)
        self.selectFacesButton.setGeometry(QtCore.QRect(10, 160, 161, 23))
        self.selectFacesButton.setObjectName("selectFacesButton")
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(180, 20, 401, 311))
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.horizontalGroupBox.setGeometry(QtCore.QRect(10, 280, 161, 51))
        self.horizontalGroupBox.setObjectName("horizontalGroupBox")
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.zeroButton = QtGui.QPushButton(self.horizontalGroupBox)
        self.zeroButton.setObjectName("zeroButton")
        self.horizontalLayout_6.addWidget(self.zeroButton)
        self.defaultsButton = QtGui.QPushButton(self.horizontalGroupBox)
        self.defaultsButton.setObjectName("defaultsButton")
        self.horizontalLayout_6.addWidget(self.defaultsButton)
        self.offsetsGroupBoxLabel = QtGui.QLabel(self.centralwidget)
        self.offsetsGroupBoxLabel.setGeometry(QtCore.QRect(20, 330, 391, 16))
        self.offsetsGroupBoxLabel.setObjectName("offsetsGroupBoxLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.exitButton, QtCore.SIGNAL("clicked()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.imagePreviewLabel.setText(QtGui.QApplication.translate("MainWindow", "Image Preview:", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalGroupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Import Buttons", None, QtGui.QApplication.UnicodeUTF8))
        self.previewButton.setText(QtGui.QApplication.translate("MainWindow", "Preview Image", None, QtGui.QApplication.UnicodeUTF8))
        self.importAsShapeButton.setText(QtGui.QApplication.translate("MainWindow", "Extruded", None, QtGui.QApplication.UnicodeUTF8))
        self.importAsMeshButton.setText(QtGui.QApplication.translate("MainWindow", "Mesh", None, QtGui.QApplication.UnicodeUTF8))
        self.importAsSolidButton.setText(QtGui.QApplication.translate("MainWindow", "Solid", None, QtGui.QApplication.UnicodeUTF8))
        self.importAsSketchButton.setText(QtGui.QApplication.translate("MainWindow", "Sketch", None, QtGui.QApplication.UnicodeUTF8))
        self.importAsFaceButton.setText(QtGui.QApplication.translate("MainWindow", "Face", None, QtGui.QApplication.UnicodeUTF8))
        self.importAsWireButton.setText(QtGui.QApplication.translate("MainWindow", "Wire", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleLabel.setText(QtGui.QApplication.translate("MainWindow", "Scale Factor", None, QtGui.QApplication.UnicodeUTF8))
        self.xOffsetLabel.setText(QtGui.QApplication.translate("MainWindow", "X Offset", None, QtGui.QApplication.UnicodeUTF8))
        self.yOffsetLabel.setText(QtGui.QApplication.translate("MainWindow", "Y Offset", None, QtGui.QApplication.UnicodeUTF8))
        self.zOffsetLabel.setText(QtGui.QApplication.translate("MainWindow", "Z Offset", None, QtGui.QApplication.UnicodeUTF8))
        self.baseNameEdit.setText(QtGui.QApplication.translate("MainWindow", "Imported", None, QtGui.QApplication.UnicodeUTF8))
        self.baseNameLabel.setText(QtGui.QApplication.translate("MainWindow", "Base Name", None, QtGui.QApplication.UnicodeUTF8))
        self.shapeHeightLabel.setText(QtGui.QApplication.translate("MainWindow", "Shape Height", None, QtGui.QApplication.UnicodeUTF8))
        self.recomputeIntervalLabel.setText(QtGui.QApplication.translate("MainWindow", "Recompute Interval    ", None, QtGui.QApplication.UnicodeUTF8))
        self.cheatFactorLabel.setText(QtGui.QApplication.translate("MainWindow", "Cheat Factor", None, QtGui.QApplication.UnicodeUTF8))
        self.progressLabel.setText(QtGui.QApplication.translate("MainWindow", "Progress Bar", None, QtGui.QApplication.UnicodeUTF8))
        self.abortButton.setText(QtGui.QApplication.translate("MainWindow", "Abort", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.staysOnTopCheckBox.setText(QtGui.QApplication.translate("MainWindow", "Window Stays on Top", None, QtGui.QApplication.UnicodeUTF8))
        self.wireEditGroupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Wire Editing", None, QtGui.QApplication.UnicodeUTF8))
        self.selectOddPointsButton.setText(QtGui.QApplication.translate("MainWindow", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.cutSelectedButton.setText(QtGui.QApplication.translate("MainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.moveButton.setText(QtGui.QApplication.translate("MainWindow", "Move", None, QtGui.QApplication.UnicodeUTF8))
        self.insertButton.setText(QtGui.QApplication.translate("MainWindow", "Insert", None, QtGui.QApplication.UnicodeUTF8))
        self.blackForegroundCheckbox.setText(QtGui.QApplication.translate("MainWindow", "Black Foreground", None, QtGui.QApplication.UnicodeUTF8))
        self.selectFacesButton.setText(QtGui.QApplication.translate("MainWindow", "Select Objects", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalGroupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Defaults", None, QtGui.QApplication.UnicodeUTF8))
        self.zeroButton.setText(QtGui.QApplication.translate("MainWindow", "Zero Offsets", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultsButton.setText(QtGui.QApplication.translate("MainWindow", "Defaults", None, QtGui.QApplication.UnicodeUTF8))
        self.offsetsGroupBoxLabel.setText(QtGui.QApplication.translate("MainWindow", "various options", None, QtGui.QApplication.UnicodeUTF8))


#end QTDesigner produced code





#if anyone desires to translate this to another language, use these defines to
#do so
#you should not need to change any text anywhere else in the file
#modifying elsewhere might cause the macro to not function properly

#BEGIN TRANSLATION SECTION
importAsSolidButtonText = u'Solid'
importAsSketchButtonText = u'Sketch'
importAsMeshButtonText = u'Mesh'
importAsShapeButtonText = u'Extruded'
extrudeText = u'EXTRUDE'
faceText = u'FACE'
wireText = u'WIRE'
sketchSupportText = u'Sketch Support'
buildingShapesText = u'building shapes '
selectFacesButtonText = u'Select Objects'
selectFacesText = u'Select Axis'
exitButtonText = u'Exit'
progressLabelText = u'Progress Bar'
abortButtonText = u'Abort'
iambTip = u'Imports image as Mesh object'
importAsFaceButtonTip = u'Imports image as 2D Face objects'
importAsWireButtonTip = u'Imports image as DWire objects'
importAsShapeButtonTip = u'Imports as Extruded Shapes'
blackForegroundCheckboxText = u'Black Foreground'
imagePreviewLabelText = u'Image Preview'
offsetsGroupBoxText = u'Various Options (mouse over for tool tip help)'
scaleLabelText = u'Scale Factor'
recomputeIntervalLabelText = u'Recompute Interval'
xOffsetLabelText = u'X Offset'
yOffsetLabelText = u'Y Offset'
zOffsetLabelText = u'Z Offset'
staysOnTopText = u'Keep Window on Top'
baseNameLabelText = u'Base Name Label'
shapeHeightLabelText = u'Part Height'
sfTip = u'Select all the Part.Faces, Part.Edges, or Part.Vertexes objects that are at the same level relative to selected axis X,Y, or Z as currently selected object.  Useful for selecting faces for creating pocket paths.'
iasbTip = u'Imports image as a solid using Wedge primitives, which can optionaly be combined into a single compound, or fused into a single solid.'
iassbTip = u'Imports image as a sketch using unconstrained line segments.'
ebTip = u'Exits and closes main window.  You should abort any ongoing operations before exiting.'
seTip = u'Scales created objects.  Invalid values are ignored in favor of 1.  One example usage: if you are setup in mm, but want to use 3/4\" equivalent number of mm you could enter 25.4 * 3/4 to convert to 3/4 inch.'
riTip = u'Shapes are inserted multiple times in between calls to recompute().  This sets the interval.  Should be an int value. \n\
Lower values will call recompute() more often, resulting in reduced performance during import.'
yoeTip = zoeTip = xoeTip = u'Offset image to desired position relative to the origin, also used for wire point editing moves.'
bneTip = u'Base name applied to labels for most import types, e.g. Imported, Imported1, etc.'
cheTip = u'Z height for some import types. Scale Factor is NOT applied to part height, so this will be the final height.'
wirePointEditingText = u'Wire Point Editing'
selectErrorMessage = u'You must first select an existing face, edge, or vertex, so we know which x/y/zmin and x/y/zmax to look for'
abortedText = u'Aborted by user'
placingText = u"Processing "
previewButtonText = u'Preview Image'
previewButtonTip = u'Loads an image for preview in the preview panel, displays red and green cross to indicate origin (0,0) position'
graphicsExceptionText = u'\nGraphics exception displaying preview image.\n'
invalidFileText = u'File must be a monochrome BMP (black and white, monochrome, 1 bit-per-pixel only).'
openMonoFileText = u'Open bmp (monochrome) file'
parsingBmpText = u"Parsing image"
userErrorText = u'User error'
addingText = u'Adding '
lineSegmentsText = u' line segments'
examiningText = u'Examining '
objectsText = u' objects'
selectOddPointsErrorMessage = u'No points selected.  Select a point or points on a DWire object.'
scaleFactorErrorText = u'Error setting scale_factor, resetting to 1'
recomputeErrorText = u'Error setting recompute_interval, resetting to 10'
xOffsetErrorText = u'Error setting import_x_offset, resetting to 0'
yOffsetErrorText = u'Error setting import_y_offset, resetting to 0'
zOffsetErrorText = u'Error setting import_z_offset, resetting to 0'
baseNameErrorText = u'Error setting Shape Base Name, resetting to default Shape'
cheatFactorErrorText = u'Error setting Cheat Factor, resetting to default 0.0001'
wedgeHeightErrorText = u'Error setting Shape Height, resetting to 1'
applyingCheatsText = u'Applying cheats'
cheatFactorLabelText = u'Cheat Factor'
cfeTip = u'Should ordinarily be a very small floating point value.  Used for diagonally adjacent pixels in sketches, faces, wires, and extruded, to fuse them together, and also for meshes to keep diagonally adjacent pixels apart.  Set this to 0 if you do not want to use the cheating algorithm, but note: wire, face, and extruded require it.'
progressCompleteText = u'Process complete'
offsetsGroupBoxTipText = u'\
Math expressions are allowed, and will be converted to floating point values.\n\n\
Constants supported:\n\
e = math.e = Euler\'s constant = 2.718...\n\
pi = math.pi = 3.14159...\n\
phi = golden ratio, alternatively golden, golden_ratio = 1.618...\n\
inch = 25.4, alternatively inches, thou = .0254\n\n\
References supported:\n\
scale (value in scale factor edit box)\n\
x, y, z (current value in x, y, z offset)\n\
part_height, alternatively: part (value in part height edit box)\n\
recompute, alternatively: recompute_interval (value in recompute interval edit box)\n\
cheat, alternatively: cheat_factor (value in cheat factor edit box)\n\
zoom (current preview image zoom value, displayed as nnnx where nnn is the zoom factor)\n\
vx, vy (width and height of the image preview panel in pixels)\n\
px, py (number of pixels CAPABLE of being displayed in the preview panel at the current zoom)\n\
width, alternatively: w (width, including background pixels, of currently previewed image)\n\
height, alternatively: h (height, including background pixels, of currently previwed image)\n\n\
Note: references are TEMPORARY and are to current immediate values only.  Thus when original referenced\n\
value changes, the edit box using that reference is NOT updated.\n\n\
Math functions supported:\n\
cos, acos, sin, asin, tan, atan, log, tlog (Note: neither constants nor references can be used with these.)\n\n\
Examples:\n\n\
cos32p5d interpreted as cos(32.5 degrees)\n\
cos32r  interpreted as cos(32 radians)\n\
asin1p interpreted as asin(1 radians) (Note: radians is default if neither d nor r is appended to parameter.)\n\
sinpi (error, must use numbers for parameters)\n\
sin3p1415926r interpreted as sin(pi radians)\n\
cosx (error, must use numbers for parameters to trig functions)\n\
log7 (natural logarithm using base e, same as math.log(7))\n\
tlog10  (base 10 logarithm using base 10, same as math.log10(10)\n\
log10 (natural logarithm using base e, same as math.log(10))\n\
tlog23p5 (base 10 logarithm -- math.log10(23.5))\n\
-width/2, alternatively: -w/2 (if used in x offset would center axis cross in currently previewed image)\n\
-height/2, alternatively: -h/2 (if used in y offset box would center axis cross)\n\
250/width, alternatively: 250/w (if used in scale factor box would scale imported object to be 250 mm wide)\n\
25/scale (if used in part height box would ensure final part, for some import types, would be 25 mm in height.\n\
(5+1/2)*inches/w (if used in scale factor box would scale imported object to be 5 1/2 inches wide, presumes you are in mm units)\n\
2**3 (2 to the power of 3 = 8)\n\
2^3 (bitwise exclusive or function, NOT 2 to the power of 3!)\n\
2**(1/2) (square root of 2 = 1.414...)\n\
y**(1/3) (cube root of whatever value is currently in the y offset edit box)\n\
2+3*5 (17, NOT 25, usual algebraic order of operation is applied)\n\
10*phi, alternatively: 10*golden, alternatively 10*golden_ratio (10 * 1.618...)\n\
e**pi (e to the power of pi = 23.14...)\n\
'






importAsSketchButtonTip = u'Import image as Sketch made up exclusively of unconstrained line segments.'
cantImportText = u'Sorry, can\'t import as this type if Cheat Factor is set to 0'
meshObjectText = u'MESH OBJECT'
solidObjectText = u'MAKE ONE SOLID'
meshImportText = u'Mesh Import Options'
moveButtonText = u'Move'
moveButtonWaitingText = u'Waiting...'
moveButtonTipText=u'Move currently selected point by x,y,z offset, SHIFT+CLICK to go opposite direction (UNDO), CTRL+CLICK to setup mouse click destination, CLICK again to cancel.'
selectOddPointsButtonText=u'Select'
selectOddPointsButtonTipText = u'Select points on a DWire object, CLICK = every other point, SHIFT+CLICK = every point, CTRL+CLICK = smart select'
deleteButtonText = u'Cut'
deleteButtonTipText = u'Cuts previously selected points from DWire object (SHIFT+CLICK to undo last cut operation)'
insertButtonText = u'Insert'
insertButtonTipText = u'Insert a new point in between 2 previously selected points on a DWire object, SHIFT+CLICK to paste previously cut points.'
multipleSolidsText = u'MULTIPLE WEDGES'
solidImportText = u'Solid Import Options'
compoundSolidText = u'MAKE COMPOUND SOLID'
afcbTip = u'Checked = Use black as foreground, unchecked = use white as foreground color.'
select2PointsText=u'Select 2 adjacent points on the wire object.'
baseNameText = u'Imported'
zoomText = u'Zoom'
zeroText = u'Zero XYZ'
zeroButtonTipText = u'Zero out XYZ offsets'
defaultsButtonTipText = u'Resets all UI elements to default values (same as closing and restarting macro).  To change defaults you must edit the source code defaults section.'
#END TRANSLATION SECTION

#default constant defines
#change these for different ui starting values

BLACK_FOREGROUND = True  #foreground color will be black if True, else white
PART_HEIGHT = 1 #pixel height (z axis) for solid/mesh/extruded import types 
SHAPE_BASENAME = 'Imported'                   
IMPORT_X_OFFSET = 0 
IMPORT_Y_OFFSET = 0 
IMPORT_Z_OFFSET = 0 
SCALE_FACTOR = 1 
RECOMPUTE_INTERVAL = 100 
CHEAT_FACTOR = 7e-5 
WINDOW_STAYS_ON_TOP = False
SEPARATOR = locale.localeconv()['decimal_point']
SEPARATOR_STANDIN = 'p'
DEGREES_INDICATOR = 'd'
RADIANS_INDICATOR = 'r'


#some globals

boxes = []
vlines = [] #will contain list of VLine objects representing vertical lines in sketch
hlines = [] #horizontal lines
sketch = None 
raster_lines = 0
pixels_per_line = 0
preview_width = 0
preview_height = 0 
bit_array = None #[[]]
progress_abort = False #when user clicks abort button in progressLayout this gets set to True
preview_image = None
imageName = None
name = None
zoomFactor = 1.0
factor = None #related to preview image zoom level
actual_zoom = None
shownX = None #how many pixels currently showing in preview panel at this zoom level?
shownY = None
mouseEventCallBack = None
selPointIndex = None #used to keep track of which point was selected before mouseEventCallBack in move function
undoPoints=[] #to undo cut operation or for inserting using shift+insert
select_objects_axis = 'Z'
import_as_mesh = True
import_as_sketch = False
import_as_shape = True
shape_form = 'EXTRUDE'
one_solid = True 
make_compound_solid = True
sketch_support = 'XY_PLANE'
viewrectHeight = None
viewrectWidth = None
#apply default values
black_foreground = BLACK_FOREGROUND
foreground_color = 0 #0 = color 1, 1 = color 2 (gets changed if user changes black foreground checkbox)
shape_basename = SHAPE_BASENAME
import_x_offset = IMPORT_X_OFFSET
import_y_offset = IMPORT_Y_OFFSET
import_z_offset = IMPORT_Z_OFFSET
scale_factor = SCALE_FACTOR
recompute_interval = RECOMPUTE_INTERVAL
cheat_factor = CHEAT_FACTOR
window_stays_on_top = WINDOW_STAYS_ON_TOP
part_height = PART_HEIGHT


# for evaluating math expressions in gui input text fields
# credit "jfs" of stackoverflow for these 2 functions, which I modified for my needs
# supported operators


operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor, #ast.BitXor: op.pow would remap ^ to pow()
             ast.USub: op.neg}
#add some constants and references that might be useful for users of FCBmpImport
constants = {'pi':math.pi,'e':math.e, 'phi':16180339887e-10, 'golden':16180339887e-10,'golden_ratio':16180339887e-10,
             'inch':254e-1, 'inches':254e-1, 'thou':254e-4}
references= {'width':'preview_width', 'w':'preview_width', 'vx':'viewrectWidth', 'vy':'viewrectHeight', 'px':'shownX','py':'shownY',
            'height':'preview_height', 'h':'preview_height', 'x':'import_x_offset', 'y':'import_y_offset', 'z':'import_z_offset',
            'part_height':'part_height', 'part':'part_height', 'cheat':'cheat_factor', 'cheat_factor':'cheat_factor',
            'scale':'scale_factor', 'scale_factor':'scale_factor',
            'recompute':'recompute_interval', 'recompute_interval':'recompute_interval', 'zoom':'actual_zoom'}
maths = {'cos':'cos','acos':'acos','tan':'tan','atan':'atan','sin':'sin','asin':'asin','log':'log','tlog':'log10'}
def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
#provide support for constants and references
    elif node.id:
        if node.id in constants:
            return constants[node.id]
        elif node.id in references: #e.g. references[node.id] is a string, e.g. 'scale_factor' representing global variable scale_factor
            return globals()[references[node.id]]
        elif node.id[:3] in maths:
            func = getattr(math, maths[node.id[:3]])
            opstring = node.id[3:].replace(SEPARATOR_STANDIN,SEPARATOR)
            if opstring[-1:]==DEGREES_INDICATOR:
                opstring = opstring[:-1]
                return func(float(opstring)*math.pi/180.0)
            elif opstring[-1:]==RADIANS_INDICATOR:
                opstring = opstring[:-1]
                return func(float(opstring))  
            else:
                return func(float(opstring))
        elif node.id[:4] in maths:
            func = getattr(math, maths[node.id[:4]])
            opstring = node.id[4:].replace(SEPARATOR_STANDIN,SEPARATOR)
            if opstring[-1:]==DEGREES_INDICATOR:
                opstring = opstring[:-1]
                return func(float(opstring)*math.pi/180.0)
            elif opstring[-1:]==RADIANS_INDICATOR:
                opstring = opstring[:-1]
                return func(float(opstring)) 
            else:
                return func(float(opstring))
        else:
            App.Console.PrintMessage(u'unsupported token: '+node.id+u'\n')
    else:
        raise TypeError(node)




def on_exit(): #user presses exit button
    #could add progress_abort = True here to close any currently running process, but have decided not to
    pass
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





class Box(object):
    __slots__ = ('length', 'width', 'height', 'x', 'y', 'z','boxName')

class VLine(object):
    __slots__ = ('top_x', 'top_y', 'bottom_x', 'bottom_y', 'isExtensible')

class HLine(object):
    __slots__ = ('left_x', 'left_y', 'right_x', 'right_y','isExtensible')


class GraphicsView(QtGui.QGraphicsView): #subclass so we can handle mouse wheel movements for zooming preview
    def __init__ (self, parent=None):
        super(GraphicsView, self).__init__ (parent)
    def wheelEvent(self, evt):
        global zoomFactor
        inFactor = 10.0/9.0
        outFactor = 9.0/10.0
        modifiers = QtGui.QApplication.keyboardModifiers()

        if evt.delta() > 0:
            zoomFactor = zoomFactor * float(inFactor)
            if modifiers == QtCore.Qt.ShiftModifier or modifiers==QtCore.Qt.ShiftModifier.__or__(QtCore.Qt.ControlModifier): #zoom in until we have one more pixel shown in the preview panel
                if shownX:
                    targetX = round(shownX,0)-1
                    zoomFactor = 1/(targetX/viewrectWidth)/factor
            elif modifiers == QtCore.Qt.ControlModifier:
                if shownY:
                    targetY = round(shownY,0)-1
                    zoomFactor = 1/(targetY/viewrectHeight)/factor
        else:
            zoomFactor = zoomFactor*float(outFactor)
            if modifiers == QtCore.Qt.ShiftModifier or modifiers==QtCore.Qt.ShiftModifier.__or__(QtCore.Qt.ControlModifier):
                if shownX:
                    targetX = round(shownX,0)+1
                    zoomFactor = 1/(targetX/viewrectWidth)/factor
            elif modifiers == QtCore.Qt.ControlModifier:
                if shownY:
                    targetY = round(shownY,0)+1
                    zoomFactor = 1/(targetY/viewrectHeight)/factor
        try:
            scalePreview(pixmap, self, zoomFactor)
        except:
            raise StandardError('Exception in zooming preview, can probably be ignored.')
            

#for CTRL+MOVE operation in wire point editing tools
class ViewObserver:
   def __init__(self, view):
       self.view = view
   
   def logPosition(self, info):
       down = (info["State"] == "DOWN")
       pos = info["Position"]
       btn = info["Button"]
       if btn == 'BUTTON2': #right click to cancel operation and remove observer
           v=Gui.activeDocument().activeView()
           v.removeEventCallback("SoMouseButtonEvent",mouseEventCallBack)
           ui.moveButton.setText(moveButtonText)
           processEvents()

       if (down and btn != 'BUTTON2'):
           pnt = self.view.getPoint(pos)
           moveSelected(pnt)
           info = self.view.getObjectInfo(pos)
           v=Gui.activeDocument().activeView()
           v.removeEventCallback("SoMouseButtonEvent",mouseEventCallBack) 



#helper function for selecting multiple faces, edges, or points (on the same x, y, or zmin/zmax) of a
#complex object

def selectObjects():

    # select one face of the object
    # all other faces at that same zmin and zmax will be selected by this macro
    # example, if you have pocketed an imported image for an engraving job
    # at 1 mm beneath the surface of your stock piece you can select one
    # of the pockets, and then invoke the macro to select all the other
    # faces at that same 1 mm zmin/zmax 

    #see which face, if any, is already selected
    #and get zmin/zmax values

    global select_objects_axis

    selectionObject = FreeCADGui.Selection.getSelectionEx()
    if not selectionObject:
        msgDialog(selectErrorMessage,u'FCBmpImport',QtGui.QMessageBox.Critical)#no object selected
        return
    else:
        selObj = selectionObject[0]

    items = (u'Z', u'Y', u'X') #put Z first since it is most useful and likely to be most used
    item, ok = QtGui.QInputDialog.getItem(MainWindow, selectFacesText,selectFacesText, items, 0, False)
    if ok:
        select_objects_axis = item
    else:
        return



    documentName = selObj.DocumentName #'Unnamed' etc
    objectName = selObj.ObjectName #'Cut' 'Fusion001' etc
    subElementName = selObj.SubElementNames[-1] #(without the [0]) names of selected faces ['Face4','Face5'] etc
    faceSel = selObj.SubObjects[-1] #current face selected (list of Face objects without the [0])
    boundBox = faceSel.BoundBox
    typeId = faceSel.TypeId
    selectedObjects = []

    #zmin = boundBox.ZMin #if ZMin == ZMain this is a face on the xy plane at z=ZMin
    #zmax = boundBox.ZMax
    axismin = None
    axismax = None
    if select_objects_axis == 'Z':
        axismin = boundBox.ZMin
        axismax = boundBox.ZMax
    elif select_objects_axis == 'X':
        axismin = boundBox.XMin
        axismax = boundBox.XMax
    elif select_objects_axis == 'Y':
        axismin = boundBox.YMin
        axismax = boundBox.YMax


    #this might take some time, so add a progress dialog
    shapes = App.ActiveDocument.findObjects("Part::Feature")

    initProgressBar(examiningText + str(len(shapes)) + objectsText, len(shapes))
    progress = 0
    for sh in shapes:
        if sh.Label != objectName:
            progress +=1
            updateProgressBar(progress)
            continue
        objects=[]
        typeName = ''
        #handle some other types besides just faces
        if type(faceSel) is Part.Face:
            objects = ["Face%d" % (i + 1) for i in range(len(sh.Shape.Faces))]
            typeName = 'Faces'
        elif type(faceSel) is Part.Edge:
            objects = ["Edge%d" % (i + 1) for i in range(len(sh.Shape.Edges))]
            typeName = 'Edges'
        elif type(faceSel) is Part.Vertex:
            objects = ["Vertex%d" % (i + 1) for i in range(len(sh.Shape.Vertexes))]
            typeName = 'Vertexes' #you say vertexes i say vertices
            

        it = 0
        for f in objects:
            attr = getattr(sh.Shape,typeName)
            bb = attr[it].BoundBox

            
            if select_objects_axis == 'Z'and bb.ZMax == axismax and bb.ZMin == axismin:
                Gui.Selection.addSelection(sh, [objects[it]])

                selectedObjects.append((sh,objects[it]))
            elif select_objects_axis == 'X' and bb.XMax == axismax and bb.XMin == axismin:
                Gui.Selection.addSelection(sh, [objects[it]]) 
            elif select_objects_axis == 'Y' and bb.YMax == axismax and bb.YMin == axismin:
                Gui.Selection.addSelection(sh, [objects[it]]) 
            it += 1
        progress +=1
        updateProgressBar(progress)
    postSelObj = FreeCADGui.Selection.getSelectionEx()[0]

#end of selectObjects()

#WIRE POINT EDITING TOOLS


def insertPoint(): # add new point on wire in between the 2 selected points
                # or insert previously cut points if SHIFT+CLICK
    global undoPoints
    selectionObject = Gui.Selection.getSelectionEx()
    if selectionObject:
        selObj = selectionObject[0]
    else:
        msgDialog(selectOddPointsErrorMessage,u'FCBmpImport',QtGui.QMessageBox.Critical)#no object selected
        return
    subObjs = selObj.SubObjects
    objectName = selObj.ObjectName #e.g. 'DWire'
    picked = selObj.SubObjects
    if len(picked) != 2:
        msgDialog(select2PointsText)
        return
    doc = Gui.activeDocument()
    obj = doc.getObject(selObj.ObjectName)
    allPoints = obj.Object.Points #all the points in the selected wire
    modifiers = QtGui.QApplication.keyboardModifiers()


    outerPoints=[]

    for jj in range(len(allPoints)-1,-1,-1):
        for ii in range(len(picked)-1,-1,-1):
            if allPoints[jj].x == picked[ii].X and allPoints[jj].y == picked[ii].Y and allPoints[jj].z == picked[ii].Z:
                outerPoints.append(jj)

    start = outerPoints[0]
    end = outerPoints[1]
    
    if start > end:
        temp = start
        start = end
        end = temp    


    startPoint = allPoints[start]
    endPoint = allPoints[end]

    if modifiers == QtCore.Qt.ShiftModifier: #insert undoPoints if shift-clicked
        if len(undoPoints)==0:
            return
        else:
            for p in undoPoints:
                allPoints.insert(end,p)
            undoPoints = []
    else:


        newPoint = App.Vector(startPoint)
        newPoint.x = (startPoint.x + endPoint.x)/2.0
        newPoint.y = (startPoint.y + endPoint.y)/2.0
        newPoint.z = (startPoint.z + endPoint.z)/2.0
        idx = None
        if start == 0 and end == 1:
            allPoints.insert(1,newPoint)
            idx = 1
        elif start == 0 and end == len(allPoints) -1:
            allPoints.insert(end+1, newPoint)
            idx = end+1
        else:
            allPoints.insert(start+1,newPoint)
            idx = start+1

    obj.Object.Points = allPoints
    App.ActiveDocument.recompute()
    if modifiers != QtCore.Qt.ShiftModifier: 
        selectOddPoints(idx)



def cutSelected():
    global undoPoints
    selectionObject = Gui.Selection.getSelectionEx()
    if selectionObject:
        selObj = selectionObject[-1]
    else:
        msgDialog(selectOddPointsErrorMessage,u'FCBmpImport',QtGui.QMessageBox.Critical)#no object selected
        return

    subObjs = selObj.SubObjects
    picked = selObj.SubObjects

    doc = Gui.activeDocument()
    obj = doc.getObject(selObj.ObjectName)
    allPoints = obj.Object.Points #all the points in the selected wire
    modifiers = QtGui.QApplication.keyboardModifiers()
    if modifiers == QtCore.Qt.ShiftModifier: #undo deleted points if shift-clicked
        if len(undoPoints)!=0:
            obj.Object.Points = undoPoints
            App.ActiveDocument.recompute()
            undoPoints = []

        return
    else:
        #setup the undo operation
        undoPoints = []
        for p in obj.Object.Points:
            undoPoints.append(p)


    toBeRemoved=[]

    for jj in range(len(allPoints)-1,-1,-1):
        for ii in range(len(picked)-1,-1,-1):
            if abs(allPoints[jj].x -picked[ii].X)<cheat_factor and abs(allPoints[jj].y -picked[ii].Y)<cheat_factor and abs(allPoints[jj].z -picked[ii].Z)<cheat_factor:

                toBeRemoved.append(jj)


    for tbr in toBeRemoved: #because we have these in reverse order from end, larger indices first, this method can work
        allPoints.pop(tbr)

    obj.Object.Points = allPoints
    if len(allPoints) == 0:
        docName = App.ActiveDocument.Name
        App.getDocument(docName).removeObject(selObj.ObjectName)

    App.ActiveDocument.recompute()


def comparePoints(p1,p2,precision = cheat_factor/2.0):
    if math.fabs(p1[0]-p2[0])<precision:
        if math.fabs(p1[1]-p2[1])<precision:
            if math.fabs(p1[2]-p2[2])<precision:
                return True

    return False

def movePoint(p,bOpposite): #apply offsets and return new point
    newPoint = App.Vector(p)
    if not bOpposite:
        newPoint[0]+=import_x_offset
        newPoint[1]+=import_y_offset
        newPoint[2]+=import_z_offset
    else: #move in opposite direction (helps to undo back moves)
        newPoint[0]-=import_x_offset
        newPoint[1]-=import_y_offset
        newPoint[2]-=import_z_offset
    return newPoint


    #moveTo() function if user clicks Move with CTRL pressed
    #we setup the observer within movePoint
    #when the mouse is clicked the observer function sets up and calls moveSelected(x,y,z) using the mouse coords
    #upon return from moveSelected(x,y,z) the observer function removes itself from resident status
#App.newDocument()
#v=Gui.activeDocument().activeView()
 

def selectOddPoints(idx=None): #user selects 2 points on the same wire, we select the odd points in between
                                #or if shift+click and 2 points we select all points in between or..
                        #alternatively, user selects one point and we select all odd points (or even if the user selected even numbered point) or...
                        #user selects one point and shift+clicks and we select all points on the wire


    mod = None
    modifiers = QtGui.QApplication.keyboardModifiers()
    selectAll = False
    smartSelect = False
    if modifiers == QtCore.Qt.ShiftModifier: #select all points if shift-clicked
        selectAll = True
    elif modifiers == QtCore.Qt.ControlModifier: #ctrl-clicked, so do smart select
        smartSelect = True
        
    selectionObject = Gui.Selection.getSelectionEx()
    if selectionObject:
        selObj = selectionObject[-1]
    else:
        msgDialog(selectOddPointsErrorMessage,u'FCBmpImport',QtGui.QMessageBox.Critical)#no object selected
        return
    subObjs = selObj.SubObjects
    picked = selObj.PickedPoints #the point(s) the user selected
    objectName = selObj.ObjectName #e.g. 'DWire'
    doc = Gui.activeDocument()
    obj = doc.getObject(objectName)



    allPoints = obj.Object.Points #all the points in the selected wire

    

    startEndIndices=[] #should be 2 points in here after the jj and ii loops

    shapes = App.ActiveDocument.findObjects("Part::Part2DObject")
    names = []
    ourShape = None
    for sh in shapes:
        if sh.Label == objectName:
            names = ["Vertex%d" % (i + 1) for i in range(len(sh.Shape.Vertexes))]
            ourShape = sh

    for jj in range(len(allPoints)-1,-1,-1):
        for ii in range(len(picked)-1,-1,-1):
            if comparePoints(allPoints[jj],picked[ii]):
                startEndIndices.append(jj)


   
        
    start = None
    end = None

    if len(startEndIndices)!=2: #if user selects more than 2 points we select all odd points beginning at 1st (unless shift+click, we select all points between)
        if startEndIndices[0] % 2 == 0: #select all even or odd points depending on the user's initial selection if he only selected one point
            start = 0
        else:
            start = 1
        end = len(names)
    else:
        start = startEndIndices[0]
        end = startEndIndices[1]
    if selectAll and len(startEndIndices)!=2:
        start = 0
        end = len(names)
    step = 1
    if start > end:
        step = -1
    mod = start % 2
    toBeAdded=[]#will be strings naming the vertices to be additionally selected
    if idx == None:
        if not smartSelect:
            for ii in range(start, end, step):
                if ii % 2 == mod and not selectAll:
                   toBeAdded.append(names[ii]) 
                elif selectAll:
                   toBeAdded.append(names[ii])
        else: #do smart select
            comeFromDirection = None #old recently used directions
            goingToDirection = None
            toDirection = None #new soon to be used directions
            fromDirection = None
            if start > end:
                tmp = start
                start = end
                end = tmp

            comeFromDirection = fixDirection(allPoints[start-1],allPoints[start])
            goingToDirection = fixDirection(allPoints[start],allPoints[start+1]) 

            ii=start                 
            while ii < end:
                if ii==start:
                    fromDirection = comeFromDirection
                    toDirection = goingToDirection
                else:
                    fromDirection = fixDirection(allPoints[ii-1],allPoints[ii])
                    if ii+1 >= len(allPoints):
                        break
                    toDirection = fixDirection(allPoints[ii],allPoints[ii+1])

                if not comparePoints(comeFromDirection,fromDirection) or not comparePoints(goingToDirection,toDirection): #new direction
                    ii += 1 #skip this point
                    if ii>=len(allPoints):
                        break
                toBeAdded.append(names[ii])
                comeFromDirection = fixDirection(allPoints[ii-1],allPoints[ii])
                if ii+1 >= len(allPoints):
                    break
                goingToDirection = fixDirection(allPoints[ii],allPoints[ii+1])
                ii+=2
        #end smart select
    else:
        toBeAdded.append(names[idx])
        Gui.Selection.clearSelection()


    Gui.Selection.addSelection(ourShape, toBeAdded) 

def fixDirection(vec1,vec2):
    
    vector2 = vec1-vec2
    for ii in range(0,3):
        vector2[ii]=round(vector2[ii]) #otherwise cheat factor would make diagonal directions

    for jj in range(0,3):
        if vector2[jj]<0: #only interested in the direction, not how far
            vector2[jj]=-1.0
        elif vector2[jj]>0:
            vector2[jj]=1.0
    return vector2 


def moveSelected(newVector = None):
    global mouseEventCallBack
    global selPointIndex #point selected when Ctrl-clicked move button
    processEvents()
    checkOffsets() #ensure offset values are registered

    if newVector == None and ui.moveButton.text()==moveButtonWaitingText: #cancel move if user clicks move button again while 'waiting...'
        v=Gui.activeDocument().activeView()
        v.removeEventCallback("SoMouseButtonEvent",mouseEventCallBack)
        ui.moveButton.setText(moveButtonText)
        processEvents()
        return

        

    modifiers = QtGui.QApplication.keyboardModifiers()
    moveOpposite = False
    if modifiers == QtCore.Qt.ShiftModifier: #move opposite direction if shift-clicked
        moveOpposite = True

    selectionObject = Gui.Selection.getSelectionEx()
    if selectionObject:
        selObj = selectionObject[0]
    else:
        msgDialog(selectOddPointsErrorMessage,u'FCBmpImport',QtGui.QMessageBox.Critical)#no object selected
        return


    subObjs = selObj.SubObjects
    #picked = selObj.PickedPoints #the ones the user selected
    picked = selObj.SubObjects

    doc = Gui.activeDocument()
    obj = doc.getObject(selObj.ObjectName)
  
    allPoints = obj.Object.Points #all the points in the selected wire


    toBeMoved=[]

    for jj in range(len(allPoints)-1,-1,-1):
        for ii in range(len(picked)-1,-1,-1):
            if allPoints[jj].x == picked[ii].X and allPoints[jj].y == picked[ii].Y and allPoints[jj].z == picked[ii].Z:
                toBeMoved.append(jj)
    if modifiers == QtCore.Qt.ControlModifier: #if user ctrl-clicks move we setup observer and return, on click the observer calls moveSelected again with newVector set
        v=Gui.activeDocument().activeView()
        o = ViewObserver(v)
        mouseEventCallBack = v.addEventCallback("SoMouseButtonEvent",o.logPosition)
        selPointIndex = toBeMoved[0]
        ui.moveButton.setText(moveButtonWaitingText)
        return


    if len(toBeMoved) > 1 or newVector==None:
        for tbm in toBeMoved: 
            #allPoints.pop(tbm)
            allPoints[tbm]=movePoint(allPoints[tbm],moveOpposite)
    else:
        #user clicked ctrl-move, and then clicked the destination position (else newVector == None and we don't get here)
        cur = allPoints[selPointIndex]   #setup an undo operation using shift+move 
        import_x_offset = newVector[0]-cur[0]
        import_y_offset = newVector[1]-cur[1]


        ui.xOffsetEdit.setText(str(import_x_offset))
        ui.yOffsetEdit.setText(str(import_y_offset))

        ui.moveButton.setText(moveButtonText)
        Gui.Selection.clearSelection()
        processEvents()
        for ii in range(0,2): #make the actual move
            allPoints[selPointIndex][ii] = newVector[ii]
        allPoints[selPointIndex][2] = float(import_z_offset) #user must manually set z offset to something other than 0


    obj.Object.Points = allPoints
    App.ActiveDocument.recompute()

#PROGRESS BAR STUFF

def initProgressBar(label, maxValue, minValue=0, cancel_button_text=abortButtonText, title="FCBmpImport Macro",modal=False):
        
        global progress_abort
        ui.progressLabel.setText(label)
        ui.progressBar.minimum = minValue
        ui.progressBar.maximum = maxValue
        ui.progressBar.setValue(0)
        ui.abortButton.setEnabled(True)
        progress_abort = False
        

def updateProgressBar(val): #sets new progress value, processes events (to keep UI responsive), and checks
                            #for user abort
    global progress_abort
    ui.progressBar.setValue(val * 100 / ui.progressBar.maximum)
    processEvents()
    
    if val == ui.progressBar.maximum:
        ui.abortButton.setEnabled(False)
        ui.progressLabel.setText(progressCompleteText)

    if progress_abort == True:
       progress_abort = False
       ui.progressBar.setValue(0)
       ui.progressLabel.setText(abortedText)
       raise StandardError(abortedText) 
def progressAbort():
    global progress_abort
    progress_abort = True   

def processEvents():
     sleep(0.001)
     QtGui.qApp.processEvents() #so FreeCAD stays responsive to user input

def msgDialog(msg, title='FCBmpImport', icon=QtGui.QMessageBox.Information):

    diag = QtGui.QMessageBox(icon, title, msg)
    diag.setWindowModality(QtCore.Qt.ApplicationModal)
    diag.exec_()
 



#create the objects for solid and mesh imports
def makeOurPart(l,w,h,x1,y1,z1,last_part=False):
    SF = scale_factor
    length = l
    width = w
    height = h

    if(last_part == True): #wrap it up, we're done (parameters not valid for new part, just display what
                           #we have so far)
        m = Mesh.Mesh()
        meshes = []
        wedges=[]
        ii = 0
        total = len(boxes)
        initProgressBar(placingText + str(len(boxes)) + u' '+ shape_basename+u's', len(boxes))
        doc = App.ActiveDocument
        for b in boxes:


            #apply scale factor at the last minute since we're waiting on FreeCAD at this point anyway
            b.x *= SF
            b.y *= SF
            b.z *= SF
            b.length *= SF
            b.width *= SF
            #b.height *= SF #no longer apply scale_factor to part_height as of version 2018.05.16
            
            if import_as_mesh == True:
                x = float(b.x)
                y = float(b.y)
                z = float(b.z)
                length = float (b.length)
                width = float(b.width)
                height = float (b.height)
                x2 = x+length-cheat_factor #prevents diagonal adjacencies from overlapping
                y2 = y+width#-cheat_factor
                z2 = z+height#-cheat_factor
                
                m1 = Mesh.Mesh([[x,y,z],[x2,y,z],[x2,y,z2],[x,y,z],[x2,y,z2],[x,y,z2]])#bottom (as viewed from above)
                m2 = Mesh.Mesh([[x,y2,z],[x2,y2,z2],[x2,y2,z],[x,y2,z],[x,y2,z2],[x2,y2,z2]])#top
                m3 = Mesh.Mesh([[x,y,z],[x,y2,z2],[x,y2,z],[x,y,z],[x,y,z2],[x,y2,z2]])#left
                m4 = Mesh.Mesh([[x2,y,z],[x2,y2,z],[x2,y2,z2],[x2,y,z],[x2,y2,z2],[x2,y,z2]])#right
                m5 = Mesh.Mesh([[x,y,z],[x,y2,z],[x2,y2,z],[x,y,z],[x2,y2,z],[x2,y,z]])#back
                m6 = Mesh.Mesh([[x,y,z2],[x2,y2,z2],[x,y2,z2],[x,y,z2],[x2,y,z2],[x2,y2,z2]])#front
                mesh = Mesh.Mesh()
                mesh.addMesh(m1)
                mesh.addMesh(m2)
                mesh.addMesh(m3)
                mesh.addMesh(m4)
                mesh.addMesh(m5)
                mesh.addMesh(m6)
                mesh.removeDuplicatedPoints()
                mesh.removeNonManifoldPoints()
                
                meshes.append(mesh)
                processEvents()
                if ii % recompute_interval == 0 or ii==len(boxes)-1:
                    try:
                        meshTemp = OpenSCADUtils.meshoptempfile('union',(meshes))
                        m = OpenSCADUtils.meshoptempfile('union',(m,meshTemp))
                        meshes = []
            
                   
                    except:
                    
                        raise StandardError('OpenSCADUtils.meshoptempfile() failed.  Do you have OpenSCAD binary installed?')


            else:
                obj = None
                if one_solid:
                    #obj = Part.makeWedge(xmin, ymin, zmin, z2min, x2min, xmax, ymax, zmax, z2max, x2max,[pnt, dir])
                    obj = Part.makeWedge(b.x, b.y, b.z, b.z, b.x, b.x+b.length, b.y+b.width, b.z+b.height, b.z+b.height, b.x+b.length)
                    wedges.append(obj)
                else:
                    doc.addObject("Part::Wedge", b.boxName)
                    obj = doc.getObject(b.boxName)
                    obj.Xmin=str(b.x)
                    obj.Ymin =str(b.y)
                    obj.Zmin = str(b.z)
                    obj.Xmax = str(b.x+b.length)
                    obj.X2max = str(b.x+b.length)
                    obj.X2min = str(b.x)
                    obj.Ymax = str(b.y+b.width)
                    obj.Zmax = str(b.z+b.height)
                    obj.Z2min = str(b.z)
                    obj.Z2max=str(b.z+b.height)
                    box = getattr(doc,b.boxName)
                    placement = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1),0),App.Vector(0,0,0))
                    box.Placement = placement


            ii += 1
            if ii % recompute_interval == 0:

                App.ActiveDocument.recompute()
            if ii == 2:
                Gui.SendMsgToActiveView("ViewFit")

            updateProgressBar(ii)
        if import_as_mesh:
            if not one_solid:
                f = doc.addObject("Mesh::Feature", shape_basename)      
                f.Mesh = m
                f.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1),0),App.Vector(0,0,0))
            else:
                shape = Part.Shape()        
                shape.makeShapeFromMesh(m.Topology,0.05)       
                solid = Part.makeSolid(shape).removeSplitter()
                f = App.activeDocument().addObject("Part::Feature",shape_basename)
                f.Shape = solid
        if not import_as_mesh and one_solid and not make_compound_solid:
            initProgressBar(u'Fusing wedges', len(wedges)-1)
            wedge = wedges[0]
            interim = wedge #using an interim object greatly speeds up the process versus fusing each wedge individually to the current full fusion
            for idx in range(1,len(wedges)):
                if idx % recompute_interval == 0:
                    wedge = wedge.fuse(interim)
                    interim = wedges[idx]
                    continue
                interim = interim.fuse(wedges[idx])
                updateProgressBar(idx)
            wedge = wedge.fuse(interim)
        if not import_as_mesh and one_solid and make_compound_solid:
            wedge = Part.makeCompound(wedges)
        
        if one_solid:
            if import_as_mesh:
                wedge = solid              
            f = doc.addObject("Part::Feature", shape_basename)
            f.Shape = wedge.removeSplitter()

        Gui.SendMsgToActiveView("ViewFit")
        App.ActiveDocument.recompute()
        return      
    else: #not last part
        box = Box()
        box.width = width
        box.height = height
        box.length = length
        box.x = x1
        box.y = y1
        box.z = z1

        box.boxName = shape_basename + str(len(boxes))
        boxes.append(box)



#returns True if neighboring pixel is foreground color
def hasNeighbor(direction, x,y):

    if direction == 'north':
        if y >= raster_lines - 1:
            return False
        return bit_array[x][y + 1] == foreground_color
    elif direction == 'south':
        if y == 0:
            return False
        return bit_array[x][y - 1] == foreground_color
    elif direction == 'east':
        if x == pixels_per_line - 1: 
            return False
        return bit_array[x + 1][y] == foreground_color
    elif direction == 'west':
        if x == 0:
            return False
        return bit_array[x - 1][y] == foreground_color



def addHLine(x,y,x2,y2,isExtensible):

    newLine = HLine()
    newLine.left_x = x
    newLine.left_y = y
    newLine.right_x = x2
    newLine.right_y = y2
    newLine.isExtensible = isExtensible
    match = False

    for oldLine in hlines:
        if oldLine.isExtensible and oldLine.right_x == newLine.left_x and oldLine.right_y == newLine.right_y:
            hlines.remove(oldLine)
            oldLine.right_x = newLine.right_x
            oldLine.right_y = newLine.right_y
            oldLine.isExtensible = isExtensible
            hlines.append(oldLine)
            match = True
            break
    if match == False:
        hlines.append(newLine)

def addVLine(x,y,x2,y2,isExtensible):

    newLine = VLine()
    newLine.bottom_x = x
    newLine.bottom_y = y
    newLine.top_x = x2
    newLine.top_y = y2
    newLine.isExtensible = isExtensible
    match = False
    counter = 0
    for oldLine in vlines:
        if oldLine.isExtensible and oldLine.top_x == newLine.bottom_x and oldLine.top_y == newLine.bottom_y:
            match = True
            vlines.remove(oldLine)            
            oldLine.top_x = newLine.top_x
            oldLine.top_y = newLine.top_y
            oldLine.isExtensible = isExtensible
            vlines.append(oldLine)
            break
    if match == False:
        vlines.append(newLine)

def previewMaybe(): #we get here if the user presses enter or leaves after editing various line edits
    if preview_image == None:
        checkOffsets() #updates globals based on ui elements
        return
    else:
        update_preview()


def update_preview():
    global preview_image
    global pixmap

    checkOffsets()
    if preview_image == None:
        preview()
    else:
        try:
            scene.clear()
            pixmap = preview_image
            preview_image = pixmap

            scalePreview(pixmap, ui.graphicsView, zoomFactor)

        except:
            App.Console.PrintMessage(graphicsExceptionText)       

def preview():
    global preview_image
    global pixmap
    global imageName
    global name
    global zoomFactor
    checkOffsets()
    zoomFactor = 0.95 #show it bit smaller the first time so the axis cross is visible
    try:

        name= QtGui.QFileDialog.getOpenFileName(QtGui.qApp.activeWindow(),openMonoFileText,'*.bmp')[0]
        if not name:
            return
        scene.clear()
        setToolTip(ui.imagePreviewLabel, name)
        imageName = name
        pixmap = QtGui.QPixmap(name)
        preview_image = pixmap

        scalePreview(pixmap, ui.graphicsView, zoomFactor)

    except:
        App.Console.PrintMessage(graphicsExceptionText)
    


def doImport():
    global bit_array #will hold the bits used to determine pixel color (1's and 0's)
    global raster_lines
    global pixels_per_line
    global foreground_color
    global black_foreground

    bit_array = [[]]
    global boxes
    boxes = []
    global vlines
    vlines = []
    global hlines
    hlines = []
    global pixmap




    if ui.blackForegroundCheckbox.isChecked():
        black_foreground = True
    else:
        black_foreground = False
    
    checkOffsets() #validate and update globals in offsets options group
    if import_as_sketch and import_as_shape and cheat_factor == 0:
        msgDialog(cantImportText)
        return
    #display preview image
    if imageName == None:
        preview() #sets global name variable to new fileName
    try:
        scene.clear()
        #name = QtGui.QFileDialog.getOpenFileName(QtGui.qApp.activeWindow(),openMonoFileText,'*.bmp')[0]
        pixmap = QtGui.QPixmap(name)


        scalePreview(pixmap, ui.graphicsView, 1.0)




    except:
        App.Console.PrintMessage(graphicsExceptionText)
    if len(name) > 0:
        with open(name, "rb") as binary_file:
            data = binary_file.read()
        
        unpacked = struct.unpack_from("B" * len(data), data)
   
        byte0 = unpacked[0] #should be 0x42 'B'
        byte1 = unpacked[1] #should be 0x4d 'M'
        byte1c = unpacked[0x1c] #bits per pixel (must be 1)
        if byte0 != 0x42 or byte1 != 0x4d or byte1c != 0x01: #'BM' in first 2 bytes signifies this is a .BMP file
            msgDialog(invalidFileText,'FCBmpImport', QtGui.QMessageBox.Critical)
            return
        else: #parse the .BMP file
            #4 bytes (little endian) beginning at 0x0a gives the offset into
                         #the
                     #pixel array
            offset = unpacked[0x0a] + unpacked[0x0b] * 256 + unpacked[0x0c] * 256 * 256 + unpacked[0x0d] * 256 * 256 * 256
            #horizontal pixel count (pixels per row) provided in 4 bytes
            #(little
            #endian) beginning at 0x12
            pixels_per_line = unpacked[0x12] + unpacked[0x13] * 256 + unpacked[0x14] * 256 * 256 + unpacked[0x15] * 256 * 256 * 256
            #vertical pixels (rows) at 0x16, again 4 bytes little endian
            raster_lines = unpacked[0x16] + unpacked[0x17] * 256 + unpacked[0x18] * 256 * 256 + unpacked[0x19] * 256 * 256 * 256
            bit_array = [[0 for y in range(raster_lines)] for x in range(pixels_per_line) ] #initialize bit_array
            bytes_per_row = (pixels_per_line + 31) / 32 * 4 #rows get padded out to multiples of 32 bits (4 bytes)
            non_padded_bytes = math.floor(pixels_per_line / 8)
            if (pixels_per_line % 8) != 0:
                non_padded_bytes += 1
            non_padded_bytes = int(non_padded_bytes)        
            color_1_Blue = unpacked[0x36] #monochrome images don't necessarily have to be black and white
            color_1_Green = unpacked[0x37] #could be for example red and white, blue and green, whatever
            color_1_Red = unpacked[0x38] #but vast majority will be black and white
            color_2_Blue = unpacked[0x3a] #we assume ours will be black and white
            color_2_Green = unpacked[0x3b]
            color_2_Red = unpacked[0x3c]
            color_1_isBlack = False
            if color_1_Blue == 0 and color_1_Green == 0 and color_1_Red == 0:
                color_1_isBlack = True


            initProgressBar(u'Loading image file', raster_lines)
            for rr in range(0, raster_lines):
                updateProgressBar(rr)
                for npb in range(0, non_padded_bytes): #npb = non-padded-byte
                    our_byte = unpacked[offset + npb + rr * bytes_per_row]                  
                    byte_string = bin(our_byte)[2:].rjust(8, '0') #credit Daniel G at stackoverflow for this line of code
                    whichBit = 0                
                    for bit in byte_string:
                        x = npb * 8 + whichBit
                        y = rr 
                        if x > pixels_per_line - 1:#check to see if this is a padded bit
                            break                    
                        bit_array[x][y] = int(bit)
                        whichBit += 1

            if black_foreground == True:
                if color_1_isBlack:
                    foreground_color = 0 #color 1
                else:
                    foreground_color = 1 #color 2
            else: 
                if color_1_isBlack:
                    foreground_color = 1 #color 2
                else:
                    foreground_color = 0 #color 1


 
    else:
        return #no file selected

    if App.ActiveDocument == None:
        App.newDocument("Unnamed")
        App.setActiveDocument("Unnamed")
        App.ActiveDocument = App.getDocument("Unnamed")
        Gui.ActiveDocument = Gui.getDocument("Unnamed")

    if import_as_sketch and import_as_shape == False:  
        
        App.activeDocument().addObject('PartDesign::Body','Body')
        activeBody = App.activeDocument().getObject(App.activeDocument().ActiveObject.Label)
        #App.activeDocument().Body.newObject('Sketcher::SketchObject',shape_basename)
        bodies = App.ActiveDocument.findObjects('PartDesign::Body')
        activeBody = bodies[-1]
        activeBody.newObject('Sketcher::SketchObject',shape_basename)
        sketches = App.ActiveDocument.findObjects('Sketcher::SketchObject')
        sketchObject = sketches[-1]
        if sketch_support == 'XY_PLANE':
            sketchObject.Support = (App.activeDocument().XY_Plane, [''])
        elif sketch_support == 'XZ_PLANE':
            sketchObject.Support = (App.activeDocument().XZ_Plane, [''])
        elif sketch_support == 'YZ_PLANE':
            sketchObject.Support = (App.activeDocument().YZ_Plane, [''])
        sketchObject.MapMode = 'FlatFace'

        Gui.activeDocument().setEdit(shape_basename)
        sketch = App.activeDocument().getObject(App.activeDocument().ActiveObject.Label)
 
    initProgressBar(parsingBmpText, raster_lines - 1)
         


    for y in range(0,raster_lines):
        sleep(0.1)
        updateProgressBar(y)

        App.ActiveDocument.recompute()


        #we'll make rectangular parts to keep part count down for better
        #performance
        if import_as_sketch == False:
        
          
            L = []    
            for x in range(0, pixels_per_line):    
                L.append(bit_array[x][y])

            grouped_L = [(k, sum(1 for i in g)) for k,g in groupby(L)] #credit: Josh Caswell of stackoverflow for this line of code
                                                                       #takes a list like [1,1,1,0,0,1,0,1,1,1] and turns it into a
                                                                       #list of tuples[(1,3),(0,2),(1,1),(0,1),(1,3)]
                                                                                                                                           
            current_x = 0 #tracks the x-coordinate for each new contiguous pixel group on this row
            for g in grouped_L: #each g is a tuple in the form (pixel, count)
                pixel = g[0]#which pixel, black or white?
                count = g[1]#how many in a row in this group?
                if pixel == foreground_color:
                    makeOurPart(count,1, part_height, current_x + import_x_offset, y + import_y_offset, import_z_offset, False) #False = not finished
                current_x = current_x + count 

        else: #sketch import
       
                
            for x in range(0, pixels_per_line):            
        
                pixel = bit_array[x][y]
                if pixel != foreground_color:
                    continue #we're done with this pixel, nothing to see here, move along
                else:
                    #this is a pixel containing our target color
                    #strategy is to surround each pixel with line segments
                    #we check to see if there are pixels to east, north, etc. to see lines are needed above, below, etc.
                    #we want to minimize the number of line segments used where possible

                    if hasNeighbor('north',x,y) == False:
                        addHLine(x,y + 1,x + 1,y + 1,hasNeighbor('east',x,y)) #no neighbor there so add a line over the cell
 
                    if hasNeighbor('south',x,y) == False:
                        addHLine(x,y,x + 1,y,hasNeighbor('east',x,y)) #extra call to hasNeighbor determines whether this line is extensible
               
                    if hasNeighbor('west',x,y) == False:
                        addVLine(x,y,x,y + 1,hasNeighbor('north',x,y)) #x,y = top_x, top_y for new vline
               
                    if hasNeighbor('east',x,y) == False:
                        addVLine(x + 1,y,x + 1,y + 1,hasNeighbor('north',x,y)) #addVLine manages the list of vlines

    #outer y loop now complete
    if import_as_sketch == False:
        makeOurPart(0,0,0,0,0,0,True) #0's just place holders, no new part will be made this final run
    
        
    #stage 2 (adding hlines and vlines to the sketch)
    if import_as_sketch == True:

        #where 4 line segments meet is where we need to fix things up if
        #cheat_factor is enabled
        #we want the top and left to stay connected and the bottom and right to
        #stay connected
        #but we don't want both intersections to be coincidental at the same
        #point, we want them
        #cheat_factor distance apart both horizontally and vertically
        new_hlines = [] #to be added
        new_vlines = []
        old_hlines = [] #to be removed
        old_vlines = []
        hSub = []
        vSub = []
        if cheat_factor != 0:
            initProgressBar('Analyzing Cheats ', len(hlines) + len(vlines))
                #optimization reduces size of lists we have to deal with to
                #only those lines with diagonal adjacencies
            it = 0
            for l1 in hlines:
                it += 1
                updateProgressBar(it)
                for l2 in hlines:
                    if l1.left_x == l2.right_x and l1.left_y == l2.right_y:
                        hSub.append(l1)
                        hSub.append(l2)
                        continue

            hSub = list(set(hSub))

            for l1 in vlines:
                it+=1
                updateProgressBar(it)
                for l2 in vlines:

                    if l1.top_x == l2.bottom_x and l1.top_y == l2.bottom_y:
                        vSub.append(l1)
                        vSub.append(l2)
                        continue
            vSub = list(set(vSub))




            it = 0
            initProgressBar(applyingCheatsText, len(hSub)+len(vSub) )
            for left in hSub:
                it += 1
                updateProgressBar(it)
                for right in hSub:
                    if left.right_x != right.left_x or left.right_y != right.left_y:
                        continue
                    for top in vSub:
                        if top.bottom_x != left.right_x or top.bottom_x != right.left_x or top.bottom_y != left.right_y or top.bottom_y != right.left_y:
                            continue
                        for bottom in vSub:
                            if bottom.top_x == top.bottom_x and bottom.top_y == top.bottom_y and left.right_x == right.left_x and left.right_y == right.left_y and bottom.top_x == left.right_x and bottom.top_y == left.right_y:
                                direction = getCheatDirection(bottom.top_x,bottom.top_y)
                                #will be 1 if upper quadrant has a pixel,
                                #meaning pixels are at Upper Right and BL, else -1,
                                #meaning pixels are at UL and BR
                                new_top = top
                                new_bottom = bottom
                                new_left = left
                                new_right = right
                                if direction == 1:
                                    new_top.bottom_x -= cheat_factor
                                    new_top.bottom_y += cheat_factor
                                    new_left.right_x -= cheat_factor
                                    new_left.right_y += cheat_factor
                                    new_right.left_x += cheat_factor
                                    new_right.left_y -= cheat_factor
                                    new_bottom.top_x += cheat_factor
                                    new_bottom.top_y -= cheat_factor
                                else:
                                    new_top.bottom_x += cheat_factor
                                    new_top.bottom_y += cheat_factor
                                    new_left.right_x -= cheat_factor
                                    new_left.right_y -= cheat_factor
                                    new_right.left_x += cheat_factor
                                    new_right.left_y += cheat_factor
                                    new_bottom.top_x -= cheat_factor
                                    new_bottom.top_y -= cheat_factor



                                #out with the old, in with the new
                                new_vlines.append(new_top)
                                new_vlines.append(new_bottom)
                                new_hlines.append(new_left)
                                new_hlines.append(new_right)
                                old_vlines.append(top)
                                old_vlines.append(bottom)
                                old_hlines.append(left)
                                old_hlines.append(right)
                                #break
        for vl in old_vlines:
            if vl in vlines:
                vlines.remove(vl)
        for vl in new_vlines:
            if not vl in vlines:
                vlines.append(vl)
        for hl in old_hlines:
            if hl in hlines:                
                hlines.remove(hl)
        for hl in new_hlines:
            if not hl in hlines:
                hlines.append(hl)

        if import_as_shape == False:
 

            job = len(hlines) + len(vlines)
            initProgressBar(addingText + str(job) + lineSegmentsText, job)
            progress = 0
    
            for hl in hlines:
                SF = scale_factor
                sketch.addGeometry(Part.LineSegment(App.Vector(SF * (hl.left_x + import_x_offset),SF * (hl.left_y + import_y_offset),SF * (0 + import_z_offset)), App.Vector(SF * (hl.right_x + import_x_offset),SF * (hl.right_y + import_y_offset),SF * (0 + import_z_offset))),False)
                progress+=1
                if progress == 10:
                    Gui.SendMsgToActiveView("ViewFit") 
                updateProgressBar(progress)
                QtGui.qApp.processEvents()
      

            for vl in vlines:    
                SF = scale_factor
                sketch.addGeometry(Part.LineSegment(App.Vector(SF * (vl.bottom_x + import_x_offset),SF * (vl.bottom_y + import_y_offset),SF * (0 + import_z_offset)),App.Vector(SF * (vl.top_x + import_x_offset),SF * (vl.top_y+import_y_offset),SF * (0 + import_z_offset))),False)
                progress+=1
                updateProgressBar(progress)

        else: #extruded shape / face / wire rather than going into sketcher as line segments


                #at this point we have 2 lists of VLines and HLines, but they're not linked together
                #we need to sort them into shapes, then form edges out of those shapes, wires out of those edges, faces out of those wires, extrude those faces, and then Part.show() for each extruded face

                #for every hline there are exactly 2 vlines connected to it, and same for every vline, with 2 hlines connected to it (cheat factor ensures this)
                #at some point we get back to the original hline with a vline connected back to it.
                shapes = []
                attached = []
                initProgressBar(buildingShapesText, len(hlines)-1)
                for it in range(0,len(hlines)):
                    updateProgressBar(it)
                    hl = hlines[it]
                    if hl in attached:
                        continue
                    shape = []
                    shape.append(hl)
                    attached.append(hl)
                    cl = findConnectingLine(hl,hl)
                    cl2 = findConnectingLine(cl,hl)
                    cl3 = findConnectingLine(cl2,cl)
                    if cl not in attached:
                        shape.append(cl)
                    if cl2 not in attached:
                        shape.append(cl2)
                    if cl3 not in attached:
                        shape.append(cl3)
                    attached.append(cl)
                    attached.append(cl2)
                    attached.append(cl3)
                    while compareLines(cl3, hl) == False:
                        if cl3 not in attached:
                            shape.append(cl3)
                            attached.append(cl3)
                        cl = cl2
                        cl2 = cl3
                        cl3 = findConnectingLine(cl2,cl)
                    shapes.append(shape)
                    shape = []
                part_lines = []
                
                edges=[]
                SF = scale_factor
                for sh in shapes:
                    for line in sh:
                        if isinstance(line,HLine):
                            hl = Part.makeLine((SF * (line.left_x + import_x_offset),SF * (line.left_y + import_y_offset),SF * (0 + import_z_offset)),  (SF * (line.right_x + import_x_offset),SF * (line.right_y + import_y_offset),SF * (0 + import_z_offset)))
                            part_lines.append(hl)
                            
                            
                        else:
                            vl = Part.makeLine((SF * (line.bottom_x + import_x_offset),SF * (line.bottom_y + import_y_offset),SF * (0 + import_z_offset)),(SF * (line.top_x + import_x_offset),SF * (line.top_y+import_y_offset),SF * (0 + import_z_offset)))
                            part_lines.append(vl)
   
     
                    for pl in part_lines:
                        e = Part.Edge(pl)
                        edges.append(e)

                    w = Part.Wire(edges)
                                        
                    edges=[]
                    part_lines = []
                    vectors=[]

                    f = Part.Face(w)
                    if shape_form == extrudeText:
                        myShape = App.ActiveDocument.addObject("Part::Feature", "Shape")
                        myShape.Label=shape_basename
                        p = f.extrude(FreeCAD.Vector(0,0,part_height))
                        myShape.Shape = p

                    elif shape_form == faceText:
                        Draft.makeWire(w,closed=True,face=True)
                        Draft.autogroup(w)
                       
                    elif shape_form == wireText:
                        Draft.makeWire(w, closed=True, face=False)
                        Draft.autogroup(w)

 
        App.ActiveDocument.recompute()
        Gui.SendMsgToActiveView("ViewFit") 
#end of doImport()
def getCheatDirection(x,y): #do we cheat to top left/bottom right or top right/bottom left?
    direction = 1
    if bit_array[x][y] != foreground_color: #upper right quadrant is not a pixel
        direction = -1

    return direction

#helper functions for importing as shapes   
def findConnectingLine(line,alreadyConnectedLine):
    #find the other connecting line, can be only one
    if type(line) is HLine:
        for v in vlines:
            if v.bottom_x == line.right_x and v.bottom_y == line.right_y and compareLines(v,alreadyConnectedLine)==False:
                return v
            if v.top_x == line.right_x and v.top_y == line.right_y and compareLines(v,alreadyConnectedLine)==False:
                return v
            if v.bottom_x == line.left_x and v.bottom_y == line.left_y and compareLines(v,alreadyConnectedLine)==False:
                return v
            if v.top_x == line.left_x and v.top_y == line.left_y and compareLines(v,alreadyConnectedLine)==False:
                return v
        return None #should never get here unless there is some error in program logic
    else: #line is a VLine, so check for connecting hline
        for h in hlines:
            if h.left_x == line.top_x and h.left_y == line.top_y and compareLines(h,alreadyConnectedLine)==False:
                return h
            if h.right_x == line.top_x and h.right_y == line.top_y and compareLines(h,alreadyConnectedLine)==False:
                return h
            if h.left_x == line.bottom_x and h.left_y == line.bottom_y and compareLines(h,alreadyConnectedLine)==False:
                return h
            if h.right_x == line.bottom_x and h.right_y == line.bottom_y and compareLines(h,alreadyConnectedLine)==False:
                return h
        return None

def compareLines(line1, line2):
    if isinstance(line1,HLine) and isinstance(line2, HLine):
        if line1.left_x == line2.left_x and line1.left_y == line2.left_y and line1.right_x == line2.right_x and line1.right_y == line2.right_y:
            return True
        else:
            return False 
    elif isinstance(line1, VLine) and isinstance(line2,VLine): #VLines
        if line1.top_x == line2.top_x and line1.top_y == line2.top_y and line1.bottom_x == line2.bottom_x and line1.bottom_y == line2.bottom_y:
            return True
        else:
            return False
    else:
            return False #2 different line types
              



def scalePreview(pixmap, gView, scaleFactor):
    global preview_width
    global preview_height
    global actual_zoom
    global viewrectHeight
    global viewrectWidth
    global shownX
    global shownY
    global factor

    modifiers = QtGui.QApplication.keyboardModifiers()

    rect = QtCore.QRectF(pixmap.rect())
    if not rect.isNull():
        w = rect.width()
        h = rect.height()
        preview_width = w
        preview_height = h
       
        gView.setSceneRect(rect)
        unity = gView.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
        gView.scale(1 / unity.width(), 1 / unity.height())
        viewrect = gView.viewport().rect()
        scenerect = gView.transform().mapRect(rect)
        viewrectHeight = viewrect.height()
        viewrectWidth = viewrect.width()
        factor = min(viewrect.width() / scenerect.width(),
        viewrect.height() / scenerect.height())
        
        y = (h + import_y_offset)
        x = -1*import_x_offset
        
        
        penRed = QtGui.QPen(QtCore.Qt.red) #axis cross (red and green)
        penGreen = QtGui.QPen(QtCore.Qt.green)
        penBlue = QtGui.QPen(QtCore.Qt.blue) #measuring lines
        penYellow = QtGui.QPen(QtCore.Qt.yellow)
        penDarkRed = QtGui.QPen(QtCore.Qt.darkRed)
        penRed.setWidth(1.0/factor)
        penGreen.setWidth(1.0/factor)
        penBlue.setWidth(1.0/factor)
        penYellow.setWidth(1.0/factor)
        penDarkRed.setWidth(1.0/factor)
        bkcolor = MainWindow.palette().color(QtGui.QPalette.Background)
        scene.setBackgroundBrush(bkcolor)
        scene.addPixmap(pixmap)

        actual_zoom = factor*scaleFactor
        shownX = 1.0/(actual_zoom/viewrectWidth)
        shownY = 1.0/(actual_zoom/viewrectHeight)
        if modifiers == QtCore.Qt.ShiftModifier:
            for ii in range(0,int(w)):
                if ii%10==0:
                    scene.addLine(ii,0,ii,h,penDarkRed)
                elif ii%5==0:
                    scene.addLine(ii,0,ii,h,penYellow)
                else:
                    scene.addLine(ii,0,ii,h,penBlue)
        elif modifiers == QtCore.Qt.ControlModifier:
            for ii in range(0,int(h)):
                if ii%10==0:
                    scene.addLine(0,ii,w,ii,penDarkRed)
                elif ii%5==0:
                    scene.addLine(0,ii,w,ii,penYellow)
                else:
                    scene.addLine(0,ii,w,ii,penBlue)

        scene.addLine(x-10.0/factor,y,x+10.0/factor,y,penRed) #axis cross
        scene.addLine(x,y-10.0/factor, x,y+10.0/factor,penGreen)
 
        gView.scale(factor * scaleFactor, factor * scaleFactor)
        ui.imagePreviewLabel.setText(imagePreviewLabelText + u' ('+str(int(w))+u'x'+str(int(h))+u'),  px,py = '+str(round(shownX,2))+u','+str(round(shownY,2))+u'  '+zoomText+' = '+str(round(factor*scaleFactor,4))+u'x')
       



#FCBmpImport logo
xpm_file = ["78 16 17 1",
" 	c None",
".	c #020401",
"+	c #3E002C",
"@	c #0D1348",
"#	c #742423",
"$	c #BB1518",
"%	c #913A00",
"&	c #4C6290",
"*	c #EA3E26",
"=	c #8E818B",
"-	c #5C94D3",
";	c #AEAE69",
">	c #86D3FC",
",	c #FFC06C",
"'	c #A9D5DA",
")	c #FDFFCE",
"!	c #FDFFFC",
"!!!'========!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
"!!!=*******#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
"!!!=*******#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
"!!!=**$#####!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
"!!!=**#!!!!!='!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
"!!!=**#!!!!'&&!''!!!!!>@...,!!!!!!!!!!!!!!>@.#)!!!!!!!!!!!!!!!!!!!!!!!!>#)!!!!",
"!!!=*$$###&&-&&&&!!!!!>#)!>#)!!!!!!!!!!!!!!>#)!!!!!!!!!!!!!!!!!!!!!!!!!>#)!!!!",
"!!!=*$$$$#------&!!!!!>#)!-%>#@.,@.,>#@..,!>#)>#@.,@.,>#@..,!>@.#)>#&#)@..,!!!",
"!!!=*$***#-&==&-&'!!!!>@...,>+,-.,-%'+,!-#)>#)>+,-.,-%'+,!-#)@,!-%>@,!!>#)!!!!",
"!!!=*$#=@&-=!!=--&=!!!>#)!>#'#)>#)>#'#)!'@,>#)>#)>#)>#'#)!'@;#)!>+'#)!!>#)!!!!",
"!!!=*$#=&--=!!=-&&'!!!>#)!'+'#)>#)>#'#)!'@,>#)>#)>#)>#'#)!'@;#)!>+'#)!!>#)!!!!",
"!!!=$$#!'&-&==&-&!!!!!>#)!-%'#)>#)>#'#)!-%)>#)>#)>#)>#'#)!-%)@,!-%>#)!!>+)!!!!",
"!!!=$$#!!&---&-&&'!!!!>@..#)>#)>#)>#'@..#)>@.#'#)>#)>#'@..#)!>@.#)>#)!!!&.,!!!",
"!!!=$$#!!&&&&&&&&'!!!!!!!!!!!!!!!!!!>#)!!!!!!!!!!!!!!!>#)!!!!!!!!!!!!!!!!!!!!!",
"!!!=*$#!!''!&&'!!!!!!!!!!!!!!!!!!!!!>#)!!!!!!!!!!!!!!!>#)!!!!!!!!!!!!!!!!!!!!!",
"!!!'===!!!!!'=!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"]



def doSolid():
    global import_as_sketch
    global import_as_mesh
    global one_solid
    global make_compound_solid
    import_as_sketch = False
    import_as_mesh = False



    items = (multipleSolidsText, compoundSolidText, solidObjectText)
    item, ok = QtGui.QInputDialog.getItem(MainWindow, solidImportText, solidImportText, items, 0, False)
    if ok:
        if item == solidObjectText:
            one_solid = True
            make_compound_solid = False
        elif item == compoundSolidText:
            one_solid = True
            make_compound_solid = True
        else:
            one_solid = False
            make_compound_solid = False
        doImport()



def doSketch():
    global import_as_sketch
    global import_as_shape
    global sketch_support
    import_as_shape = False
    import_as_sketch = True
    items = (u'XY_PLANE', u'XZ_PLANE', u'YZ_PLANE')
    item, ok = QtGui.QInputDialog.getItem(MainWindow, sketchSupportText,sketchSupportText, items, 0, False)
    if ok:
        sketch_support = item
        doImport()


def doMesh():
    global import_as_mesh
    global import_as_sketch
    global one_solid
    import_as_sketch = False
    import_as_mesh = True

    items = (meshObjectText, solidObjectText)
    item, ok = QtGui.QInputDialog.getItem(MainWindow, meshImportText, meshImportText, items, 0, False)
    if ok:
        if item == solidObjectText:
            one_solid = True
        else:
            one_solid = False
        doImport()


def doWire():
    global import_as_sketch
    global import_as_shape
    global shape_form
    import_as_sketch = True
    import_as_shape = True
    shape_form = wireText
    doImport()

    
def doFace():
    global import_as_sketch
    global import_as_shape
    global shape_form
    import_as_sketch = True
    import_as_shape = True
    shape_form = faceText
    doImport()

def doShape():
    global import_as_sketch
    global import_as_shape
    global shape_form
    import_as_sketch = True
    import_as_shape = True
    shape_form = extrudeText
    doImport()

def setToolTip(obj,tip):
    obj.setToolTip(_fromUtf8(tip))

def zeroOffsets():
    global import_x_offset
    global import_y_offset
    global import_z_offset

    import_x_offset = 0
    ui.xOffsetEdit.setText('0')
    import_y_offset = 0
    ui.yOffsetEdit.setText('0')
    import_z_offset = 0
    ui.zOffsetEdit.setText('0')
    processEvents()

def reportMsg(elem, msg): #save history of entries into line edits in the associated label as a tool tip
    if msg not in elem.toolTip(): #but only those entries not already in there
        setToolTip(elem,elem.toolTip()+msg+'\n')

def checkOffsets():
    #check all the offset, scale, etc.  options and set globals accordingly
    global import_x_offset
    global import_y_offset
    global import_z_offset
    global scale_factor
    global recompute_interval
    global shape_basename
    global part_height
    global cheat_factor

    try:
        se = ui.scaleEdit.text()
        reportMsg(ui.scaleLabel,se)
        if(se == ''):
            scale_factor = 1 #set safe default
            ui.scaleEdit.setText('1')
            return
        scale_factor = eval_expr(ui.scaleEdit.text()) #eval_expr() allows for input such as 25.4 / 2**4
        ui.scaleEdit.setText(str(scale_factor))
    except:
        ui.scaleEdit.setText('1')
        scale_factor = 1
        raise StandardError(scaleFactorErrorText)
    
    try:
        ri = ui.recomputeIntervalEdit.text()
        reportMsg(ui.recomputeIntervalLabel,ri)
        if(ri == ''):
            recompute_interval = 10
            return
        recompute_interval = eval_expr(ri)
        ui.recomputeIntervalEdit.setText(str(recompute_interval))
    except:
        ui.recomputeIntervalEdit.setText('100')
        recompute_interval = 10
        raise StandardError(recomputeErrorText)
#x
    try:
        xo = ui.xOffsetEdit.text()
        reportMsg(ui.xOffsetLabel,xo)
       
        if (xo == ""):
            import_x_offset = 0
            ui.xOffsetEdit.setText('0')
            return

        import_x_offset = eval_expr(xo)
        ui.xOffsetEdit.setText(str(import_x_offset))


    except:
        ui.xOffsetEdit.setText('0')
        import_x_offset = 0
        raise StandardError(xOffsetErrorText)
#y
    try:
        yo = ui.yOffsetEdit.text()
        reportMsg(ui.yOffsetLabel,yo)
        if (yo == ""):
            import_y_offset = 0
            ui.yOffsetEdit.setText('0')
            return

        import_y_offset = eval_expr(yo)
        ui.yOffsetEdit.setText(str(import_y_offset))
    except:
        ui.yOffsetEdit.setText('0')
        import_y_offset = 0
        raise StandardError(yOffsetErrorText)

#z
    try:
        zo = ui.zOffsetEdit.text()
        reportMsg(ui.zOffsetLabel,zo)
        if (zo == ""):
            import_z_offset = 0
            ui.zOffsetEdit.setText('0')
            return

        import_z_offset = eval_expr(zo)
        ui.zOffsetEdit.setText(str(import_z_offset))
    except:
        ui.zOffsetEdit.setText('0')
        import_z_offset = 0
        raise StandardError(zOffsetErrorText)

    try:
        cbn = ui.baseNameEdit.text()
        reportMsg(ui.baseNameLabel,cbn)
        shape_basename = cbn
    except:
        ui.baseNameEdit.setText(baseNameText)
        shape_basename = baseNameText
        raise StandardError(baseNameErrorText)
    
#shape height
    try:
        ch = ui.shapeHeightEdit.text()
        reportMsg(ui.shapeHeightLabel,ch)
        if (ch == ""):
            part_height = 1
            ui.shapeHeightEdit.setText('1')
            return

        part_height = eval_expr(ch)
        ui.shapeHeightEdit.setText(str(part_height))
    except:
        ui.shapeHeightedit.setText('1')
        part_height = 1
        raise StandardError(wedgeHeightErrorText)

#cheat factor
    try:
        cf = ui.cheatFactorEdit.text()
        reportMsg(ui.cheatFactorLabel,cf)
        if(cf == ''):
            cheat_factor = eval_expr(CHEAT_FACTOR) #set safe default
            ui.cheatFactorEdit.setText(str(cheat_factor))
            return
        cheat_factor = eval_expr(ui.cheatFactorEdit.text()) #eval_expr() allows for input such as 25.4 / 2**4
        ui.cheatFactorEdit.setText(str(cheat_factor))
    except:
        ui.cheatFactorEdit.setText(str(eval_expr(CHEAT_FACTOR)))
        cheat_factor = 1
        raise StandardError(cheatFactorErrorText)

def stayOnTop(windowHasAlreadyBeenShown = True):
    global window_stays_on_top
    bStay = window_stays_on_top
    if windowHasAlreadyBeenShown:
        bStay = ui.staysOnTopCheckBox.isChecked()
    flags = MainWindow.windowFlags()
    if bStay:
        MainWindow.setWindowFlags(flags.__or__(QtCore.Qt.WindowStaysOnTopHint).__or__(QtCore.Qt.CustomizeWindowHint))
        window_stays_on_top = True
        MainWindow.show()
    else:
        MainWindow.setWindowFlags(flags ^ (QtCore.Qt.WindowStaysOnTopHint.__or__(QtCore.Qt.CustomizeWindowHint)))
        window_stays_on_top = False
        MainWindow.show()

def defaults():
    ui.staysOnTopCheckBox.setChecked(WINDOW_STAYS_ON_TOP)
    ui.blackForegroundCheckbox.setChecked(BLACK_FOREGROUND)
    ui.scaleEdit.setText(str(SCALE_FACTOR))
    ui.recomputeIntervalEdit.setText(str(RECOMPUTE_INTERVAL))
    ui.cheatFactorEdit.setText(str(eval_expr(str(CHEAT_FACTOR))))
    ui.shapeHeightEdit.setText(str(PART_HEIGHT))
    ui.zOffsetEdit.setText(str(IMPORT_Z_OFFSET))
    ui.yOffsetEdit.setText(str(IMPORT_Y_OFFSET))
    ui.xOffsetEdit.setText(str(IMPORT_X_OFFSET))
    ui.baseNameEdit.setText(SHAPE_BASENAME)
    processEvents()


MainWindow = QtGui.QMainWindow()

ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.setWindowTitle(VERSION_STRING)

#override default QGraphicsView with our own reimplemented GraphicsView object (defined above) so we can handle wheel movements for zooming preview image
geometry = ui.graphicsView.geometry()
ui.graphicsView = GraphicsView(ui.centralwidget)
ui.graphicsView.setGeometry(geometry)
ui.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
ui.graphicsView.setObjectName("graphicsView")
ui.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
ui.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

#connect clicked events / setup defaults / apply tooltips
ui.staysOnTopCheckBox.setChecked(window_stays_on_top)
ui.staysOnTopCheckBox.clicked.connect(stayOnTop)
ui.staysOnTopCheckBox.setText(staysOnTopText)
ui.selectFacesButton.clicked.connect(selectObjects)
setToolTip(ui.selectFacesButton, sfTip)

ui.importAsFaceButton.clicked.connect(doFace)
ui.importAsWireButton.clicked.connect(doWire)

setToolTip(ui.importAsFaceButton,importAsFaceButtonTip)
setToolTip(ui.importAsWireButton,importAsWireButtonTip)

setToolTip(ui.previewButton, previewButtonTip)
ui.previewButton.clicked.connect(preview)
ui.previewButton.setText(previewButtonText)


ui.importAsSolidButton.clicked.connect(doSolid)
setToolTip(ui.importAsSolidButton,iasbTip)

ui.importAsSketchButton.clicked.connect(doSketch)
setToolTip(ui.importAsSketchButton, importAsSketchButtonTip)
ui.importAsMeshButton.clicked.connect(doMesh)
setToolTip(ui.importAsMeshButton, iambTip)
ui.importAsShapeButton.clicked.connect(doShape)
setToolTip(ui.importAsShapeButton, importAsShapeButtonTip)
ui.exitButton.clicked.connect(on_exit)

ui.abortButton.clicked.connect(progressAbort)
ui.moveButton.setText(moveButtonText)

setToolTip(ui.moveButton, moveButtonTipText)
ui.blackForegroundCheckbox.setChecked(black_foreground)

setToolTip(ui.blackForegroundCheckbox,afcbTip)





ui.scaleEdit.setText(str(scale_factor))
setToolTip(ui.scaleEdit,seTip)
ui.scaleEdit.editingFinished.connect(previewMaybe)

ui.recomputeIntervalEdit.setText(str(recompute_interval))
setToolTip(ui.recomputeIntervalEdit, riTip)
ui.recomputeIntervalEdit.editingFinished.connect(previewMaybe)

ui.xOffsetEdit.setText(str(import_x_offset))
ui.xOffsetEdit.editingFinished.connect(previewMaybe)

setToolTip(ui.xOffsetEdit, xoeTip)

ui.yOffsetEdit.setText(str(import_y_offset))
setToolTip(ui.yOffsetEdit, yoeTip)
ui.yOffsetEdit.editingFinished.connect(previewMaybe)

ui.zOffsetEdit.setText(str(import_z_offset))
setToolTip(ui.zOffsetEdit, zoeTip)
ui.zOffsetEdit.editingFinished.connect(previewMaybe)

ui.baseNameEdit.setText(shape_basename)
setToolTip(ui.baseNameEdit,bneTip)

ui.shapeHeightEdit.setText(str(part_height))
setToolTip(ui.shapeHeightEdit,cheTip)
ui.shapeHeightEdit.editingFinished.connect(previewMaybe)
ui.cheatFactorLabel.setText(cheatFactorLabelText)
setToolTip(ui.cheatFactorEdit,cfeTip)
ui.cheatFactorEdit.setText(str(cheat_factor))
ui.cheatFactorEdit.editingFinished.connect(previewMaybe)
setToolTip(ui.offsetsGroupBoxLabel,offsetsGroupBoxTipText)

ui.cutSelectedButton.clicked.connect(cutSelected)
ui.selectOddPointsButton.clicked.connect(selectOddPoints)

ui.moveButton.clicked.connect(moveSelected)
ui.insertButton.clicked.connect(insertPoint)
ui.defaultsButton.clicked.connect(defaults)
setToolTip(ui.defaultsButton, defaultsButtonTipText)

#end of clicked connections

#apply labels or translations, if any
ui.importAsSolidButton.setText(importAsSolidButtonText)
ui.importAsSketchButton.setText(importAsSketchButtonText)
ui.importAsMeshButton.setText(importAsMeshButtonText)
ui.importAsShapeButton.setText(importAsShapeButtonText)
ui.selectFacesButton.setText(selectFacesButtonText)
ui.exitButton.setText(exitButtonText)
ui.progressLabel.setText(progressLabelText)
ui.abortButton.setText(abortButtonText)
ui.abortButton.setEnabled(False)
ui.blackForegroundCheckbox.setText(blackForegroundCheckboxText)

ui.imagePreviewLabel.setText(imagePreviewLabelText)
ui.offsetsGroupBox.setTitle(u'')
ui.scaleLabel.setText(scaleLabelText)
ui.recomputeIntervalLabel.setText(recomputeIntervalLabelText)
ui.xOffsetLabel.setText(xOffsetLabelText)

ui.zeroButton.setText(zeroText)
ui.zeroButton.clicked.connect(zeroOffsets)

setToolTip(ui.zeroButton,zeroButtonTipText)
ui.yOffsetLabel.setText(yOffsetLabelText)
ui.zOffsetLabel.setText(zOffsetLabelText)
ui.baseNameLabel.setText(baseNameLabelText)
ui.shapeHeightLabel.setText(shapeHeightLabelText)
ui.insertButton.setText(insertButtonText)
setToolTip(ui.insertButton, insertButtonTipText)
ui.wireEditGroupBox.setTitle(wirePointEditingText)

setToolTip(ui.cutSelectedButton,deleteButtonTipText)
setToolTip(ui.selectOddPointsButton,selectOddPointsButtonTipText)
ui.selectOddPointsButton.setText(selectOddPointsButtonText)
ui.cutSelectedButton.setText(deleteButtonText)
ui.offsetsGroupBoxLabel.setText(offsetsGroupBoxText)

scene = QtGui.QGraphicsScene()
ui.graphicsView.setScene(scene)
pixmap = QtGui.QPixmap(xpm_file)

#scalePreview(pixmap, ui.graphicsView, 1) #current icon looks better unscaled
scene.addPixmap(pixmap)

stayOnTop(False) #False means window hasn't yet been shown
stayOnTop() #show it first in previous call, and then call again to set the configuration

#MainWindow.show()


