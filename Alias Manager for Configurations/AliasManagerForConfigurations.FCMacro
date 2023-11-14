
# ============================================================================================================
# ============================================================================================================
# ==                                                                                                        ==
# ==                                           Alias Manager for Configurations                             ==
# ==                                                                                                        ==
# ============================================================================================================
# ============================================================================================================
# ABOUT
# ============================================================================================================
# version v0.10
# Macro developed for FreeCAD (http://www.freecadweb.org/).
# This macro helps managing aliases inside FreeCAD Spreadsheet workbench. It is a variant of alias Manager by 
# 2016 tarihatari & Pablo Gil Fernandez and EasyAlias by TheMarkster and rosta
# It is able to:
#        -set aliase of a cell in a horizontal table, e.g. Configuration Table, or vertical tabel in an older 
#         scheme know as a Part Family.  You select the cell or cells and hit Execute button.  Based on the
#         radio button selected the alias label is taken from above the cells or to the left of the cells.
#       - there is also a clear fucntion which removes the alias in selected cells if that helps too.
#       - the dialog used is modal and stays on top.  This way a user can have open while working in the
#         and it's always available to add to adjust aliases.  It can be moved off to the side or to a second
#         display.  It can also be minimized and brought up when needed.
#
# This has ONLY be tested on Mac OS.
#
# LICENSE
# ============================================================================================================
# Original work done by tarihatari (https://github.com/tarihatari/FreeCAD_Macros) &
# done by TheMarkster and rosta (https://wiki.freecadweb.org/Macro_EasyAlias)
# Improved by Pablo Gil Fernandez
# Improved by Ron Zancola
#
# Copyright (c) 2023 tarihatari & TheMarkster and rosta & Pablo Gil Fernandez & Ron Zancola
#
# This work is licensed under GNU Lesser General Public License (LGPL).
# To view a copy of this license, visit https://www.gnu.org/licenses/lgpl-3.0.html.
#
# ============================================================================================================
__title__   = "Alias Manager for Configuration Tables"
__author__  = "Ron Zancola"
__version__ = "00.10"
__date__    = "23/10/2023"
 
__Comment__ = "This macro helps managing aliases inside FreeCAD Spreadsheet workbench. It is able to set/clear the alias of a cell(s). The text in the cell above or left is used for the alias."
 
__Wiki__ = "https://github.com/pgilfernandez/FreeCAD_AliasManagerConfig"
__Help__ = "https://github.com/pgilfernandez/FreeCAD_AliasManagerConfig"
__Status__ = "dev"
__Requires__ = "FreeCAD 0.16"

from PySide import QtGui, QtCore
from PySide.QtCore import Qt
from FreeCAD import Gui
#import os
import string
import re
App = FreeCAD
Gui = FreeCADGui


# ========================================================
# ===== Info popup window ================================
# ========================================================
class infoPopup(QtGui.QDialog):
    def __init__(self, parent=None):
        self.dialog = None
        self.dialog = QtGui.QDialog()
        self.dialog.resize(360,400)
        self.dialog.setWindowTitle("About...")

        info = QtGui.QTextEdit("<h2>INFORMATION</h2><hr><br>This macro helps managing aliases inside FreeCAD Spreadsheet workbench. It is able to set the alias of a cell(s) from the text in the cell above or left.</li></ul><h2>LICENCE</h2><hr>Original work done by <b>tarihatari</b><br>(<a href='https://github.com/tarihatari/FreeCAD_Macros'>https://github.com/tarihatari/FreeCAD_Macros</a>)<br>and by<br><b>TheMarkster and rosta</b><br>(<a href='https://wiki.freecadweb.org/Macro_EasyAlias'>https://wiki.freecadweb.org/Macro_EasyAlias</a>) <br><br>Improved by <br><b>Pablo Gil Fernandez</b><br>& then <br><b>Ron Zancola</b><br><br>Copyright (c) 2023 tarihatari & TheMarkster and rosta & Pablo Gil Fernandez & Ron Zancola<br><br>This work is licensed under GNU Lesser General Public License (LGPL).<br>To view a copy of this license, visit <a href='https://www.gnu.org/licenses/lgpl-3.0.html'>https://www.gnu.org/licenses/lgpl-3.0.html</a>.<br>")
        info.setReadOnly(True)
        info.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        okbox = QtGui.QDialogButtonBox(self.dialog)
        okbox.setOrientation(QtCore.Qt.Horizontal)
        okbox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        okbox.setFocus()

        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(10)
        grid2.addWidget(info, 0, 0)
        grid2.addWidget(okbox, 1, 0)

        self.dialog.setLayout(grid2)

        QtCore.QObject.connect(okbox, QtCore.SIGNAL("rejected()"), self.close)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)
        self.dialog.show()
        self.dialog.exec_()

    def close(self):
        self.dialog.close()

# =========================================================
# ===== Global variables and CONSTANTS=====================
# =========================================================
alphabet_list = list(string.ascii_uppercase)
SET_HORIZ = "from Above"
SET_VERT = "from Left"
CLEAR = "Clear"

CELL_ADDR_RE = re.compile(r"([A-Za-z]+)([1-9]\d*)")
CUSTOM_ALIAS_RE = re.compile(r".*\((.*)\)")
MAGIC_NUMBER = 64
REPLACEMENTS = {
    " ": "_",
    ".": "_",
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "Ä": "Ae",
    "Ö": "Oe",
    "Ü": "Ue",
    "ß": "ss",
    "'": ""
}

# =========================================================
# ===== Helper code =======================================
# =========================================================
def getSpreadsheets():
    """
    Returns a set of selected spreadsheets in the active document or None if none is selected.
    :returns: a set of selected spreadsheets in the active document or None if none is selected
    :rtype: set
    """

    spreadsheets = set()
    for selectedObject in Gui.Selection.getSelection():
        if selectedObject.TypeId == 'Spreadsheet::Sheet':
            spreadsheets.add(selectedObject)
        elif selectedObject.TypeId == "App::Link":
            linkedObject = selectedObject.LinkedObject
            if linkedObject.TypeId == 'Spreadsheet::Sheet':
                spreadsheets.add(linkedObject)
    return spreadsheets

# The original implementatin of a1_to_rowcol and rowcol_to_a1 can be found here:
# https://github.com/burnash/gspread/blob/master/gspread/utils.py

def a1_to_rowcol(label:str):
    """Translates a cell's address in A1 notation to a tuple of integers.
    :param str label: A cell label in A1 notation, e.g. 'B1'. Letter case is ignored.
    :returns: a tuple containing `row` and `column` numbers. Both indexed from 1 (one).
    :rtype: tuple
    Example:
    >>> a1_to_rowcol('A1')
    (1, 1)
    """

    match = CELL_ADDR_RE.match(label)

    row = int(match.group(2))

    column_label = match.group(1).upper()
    column = 0
    for i, c in enumerate(reversed(column_label)):
        column += (ord(c) - MAGIC_NUMBER) * (26**i)

    return (row, column)

def rowcol_to_a1(row:int, column:int):
    """Translates a row and column cell address to A1 notation.
    :param row: The row of the cell to be converted. Rows start at index 1.
    :type row: int, str
    :param col: The column of the cell to be converted. Columns start at index 1.
    :type row: int, str
    :returns: a string containing the cell's coordinates in A1 notation.
    Example:
    >>> rowcol_to_a1(1, 1)
    A1
    """
    row = int(row)
    column = int(column)
    dividend = column
    column_label = ""
    while dividend:
        (dividend, mod) = divmod(dividend, 26)
        if mod == 0:
            mod = 26
            dividend -= 1
        column_label = chr(mod + MAGIC_NUMBER) + column_label

    label = "{}{}".format(column_label, row)

    return label

def textToAlias(text:str):
    # support for custom aliases between parentheses
    match = CUSTOM_ALIAS_RE.match(text)
    if match:
        return match.group(1)

    for character in REPLACEMENTS:
        text = text.replace(character,REPLACEMENTS.get(character))
    return text

def setAlias(setMode : str):
    spreadsheets = getSpreadsheets()
    if not spreadsheets:
        QtGui.QMessageBox.critical(None, "Error",
            "No spreadsheet selected.\nPlease select a spreadsheet in the tree view.")
        return

    for spreadsheet in spreadsheets:   # Need to evaluate if this is really needed, it might set alias' unintentionally
        for selectedCell in spreadsheet.ViewObject.getView().selectedCells():
            # Mode - Set Horiz ==========================================
            if setMode == SET_HORIZ:
                row, column = a1_to_rowcol(selectedCell)
                sourceCell = rowcol_to_a1(row - 1, column)
                try:
                    contents = spreadsheet.getContents(sourceCell)
                except:
                    QtGui.QMessageBox.critical(None, "Error", "Must have a cell to the Above " + selectedCell)
                    return
            # Mode - Set Vert ==========================================
            elif setMode == SET_VERT:
                row, column = a1_to_rowcol(selectedCell)
                sourceCell = rowcol_to_a1(row, column - 1)
                try:
                    contents = spreadsheet.getContents(sourceCell)
                except:
                    QtGui.QMessageBox.critical(None, "Error", "Must have a cell to the Left of " + selectedCell)
                    return
                
            if contents:
                alias = textToAlias(contents)
                try:
                    spreadsheet.setAlias(selectedCell, alias)
                except:
                    QtGui.QMessageBox.critical(None, "Error",
                        "Unable to set alias <i>" + alias + "</i> at cell " + nextCell +
                        "<br>in spreadsheet <i>" + spreadsheet.FullName + "</i>." +
                        "<br><br><b>Remember, aliases cannot begin with a numeral or an " +
                        "underscore or contain any invalid characters.</b>")

# ========================================================
# ===== Main code ========================================
# ========================================================
class p():
    def aliasManagerConfig(self):
        try:
            # Mode - Set Horiz
            if (self.setHoriz.isChecked()):
                setAlias(SET_HORIZ)
                App.ActiveDocument.recompute()
            # Mode - Set Vert
            elif (self.setVert.isChecked()):
                setAlias(SET_VERT)
                App.ActiveDocument.recompute()

            #If unexpected mode
            else:
                FreeCAD.Console.PrintError("\nError or 'TODO'\n")
        except:
            FreeCAD.Console.PrintError("\nUnable to complete task\n")
            self.close()

    def onClearButton(self):
        for selectedCell in App.ActiveDocument.Spreadsheet.ViewObject.getView().selectedCells():
            App.ActiveDocument.Spreadsheet.setAlias(selectedCell, '')
            App.ActiveDocument.recompute()

    def popup(self):
        self.dialog2 = infoPopup()
        self.dialog2.exec_()

    def close(self):
        App.ActiveDocument.recompute()
        self.dialog.hide()

    def __init__(self):
        # Updated bitmap so each line has 16 chars which removes warnings like below
        #    "QImage: XPM pixels missing on image line 15 (possibly a C++ trigraph)."
        infoIcon = ['16 16 3 1',
                '   c None',
                '+  c #444444',
                '.  c #e6e6e6',
                '     ......     ',
                '   ..........   ',
                '  ......++....  ',
                ' .......++..... ',
                ' .............. ',
                '.....+++++......',
                '....+++++.......',
                '.......++.......',
                '.......++.......',
                '.......+........',
                '......++........',
                ' .....++.+..... ',
                ' .....++++..... ',
                '  .....++.....  ',
                '   ..........   ',
                '     ......     ']

        self.dialog = None        
        self.dialog = QtGui.QDialog()
        self.dialog.resize(350,140)
        
        self.dialog.setWindowTitle("Alias Manager for Configurations")
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # From Above
        self.setHoriz = QtGui.QRadioButton(SET_HORIZ)
        self.setHoriz.setChecked(True)
        
        # From Left
        self.setVert = QtGui.QRadioButton(SET_VERT)
        

        # d1 thru d5 removed

        # Info button
        self.d6 = QtGui.QPushButton("")
        self.d6.setFixedWidth(40)
        self.d6.setIcon(QtGui.QIcon(QtGui.QPixmap(infoIcon)))
        self.d6.clicked.connect(self.popup)

        # Execute and Done Buttons      
        okbox = QtGui.QDialogButtonBox(self.dialog)
        okbox.setOrientation(QtCore.Qt.Vertical) 
        okbox.addButton("Execute", QtGui.QDialogButtonBox.AcceptRole)
        okbox.addButton("Done", QtGui.QDialogButtonBox.RejectRole) 
        QtCore.QObject.connect(okbox, QtCore.SIGNAL("rejected()"), self.close)
        QtCore.QObject.connect(okbox, QtCore.SIGNAL("accepted()"), self.aliasManagerConfig)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)
   

        # Clear Button        
        self.clearButton = QtGui.QDialogButtonBox(self.dialog)
        self.clearButton.setOrientation(QtCore.Qt.Horizontal)
        self.clearButton.addButton(CLEAR, QtGui.QDialogButtonBox.AcceptRole)
        self.clearButton.clicked.connect(self.onClearButton)

        # Layout
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        #add radio button1
        grid.addWidget(self.setHoriz, 2, 0, 1, 1)
        #add radio button2
        grid.addWidget(self.setVert, 2, 1, 1, 1)
        #add Clear Buutton
        grid.addWidget(self.clearButton, 2, 3, 1, 2)
        # cancel, OK
        grid.addWidget(okbox,   4, 0, 1, 1)
        # + info
        grid.addWidget(self.d6, 6, 0, 1, 1)
        self.dialog.setLayout(grid)


        self.dialog.show()
        self.dialog.exec_()

p()

