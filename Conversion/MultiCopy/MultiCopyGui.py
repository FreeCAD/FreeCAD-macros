#!/usr/bin/env python


##########################################################################################
#####				L I C E N S E					     #####
##########################################################################################
#
#  GNU LESSER GENERAL PUBLIC LICENSE
#  Version 2.1, February 1999
#
#  Copyright (C) 1991, 1999 Free Software Foundation, Inc.
#  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.
#
#  [This is the first released version of the Lesser GPL. It also counts
#  as the successor of the GNU Library Public License, version 2, hence
#  the version number 2.1.]
#
#  'MultiCopy' is a FreeCAD macro package. MultiCopy allows the duplication
#  (copy and paste) of multiple FreeCAD objects that can be labelled
#  sequentially and in a custom manner.
#
#  Copyright (C) 2021  Melwyn Francis Carlo
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this library; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#  Contact Information :-
#  Email :  carlo.melwyn@outlook.com
#  FreeCAD UserTalk :  http://www.freecadweb.org/wiki/index.php?title=User:Melwyncarlo
#
##########################################################################################
#####				L I C E N S E					     #####
##########################################################################################


# Library Imports
# ------------------------------------------------------------------------------------------------

import FreeCAD as app
import FreeCADGui as gui
from PySide import QtCore
from PySide.QtGui import (
    QPushButton,
    QPushButton,
    QTextEdit,
    QPlainTextEdit,
    QRadioButton,
    QComboBox,
    QLabel,
    QCheckBox,
    QLineEdit,
    QSpinBox,
    QTextCursor,
    QTabWidget,
    QIcon,
    QMessageBox,
    QCursor,
)
from . import MultiCopyCore
from . import MultiCopyAuxFunc


# Constant Variables
# ------------------------------------------------------------------------------------------------

# It is the currently active FreeCAD document.
doc = app.activeDocument()


# Primary (Main) Classes
# ------------------------------------------------------------------------------------------------


class __Launch_Main_Dialog:

    """The 'MultiCopy' class is the MultiCopy object itself.

    It is both a GUI as well as a console-based class that is responsible for
    physical creation of the custom 2D airfoil curves/shapes.
    The gathered user input data is used for the process.
    """

    def __init__(self):
        """This function initializes of the 'MultiCopy' class."""
        global doc
        doc = app.activeDocument()
        self.radio_prev = ''
        self.list_of_documents = []
        self.selected_objs = gui.Selection.getSelection()
        self.list_of_documents = MultiCopyCore.GetDocumentsList(doc)
        self.__launch()

    def __dialog_is_busy(self, isBusy):
        """This function disables/enables certain GUI elements in the main dialog box."""
        if isBusy:
            self.main_dialog.setCursor(QCursor(QtCore.Qt.WaitCursor))
            self.main_dialog.findChild(QTabWidget, 'tabset').setEnabled(False)
            self.main_dialog.findChild(QPushButton, 'paste_button').setEnabled(False)
            self.main_dialog.findChild(QRadioButton, 'simple_copy_radio').setEnabled(
                False
            )
            self.main_dialog.findChild(QPushButton, 'command_list_button').setEnabled(
                False
            )
            self.main_dialog.findChild(QRadioButton, 'standard_copy_radio').setEnabled(
                False
            )
            self.main_dialog.findChild(QCheckBox, 'delete_selections_check').setEnabled(
                False
            )
            self.main_dialog.findChild(QComboBox, 'documents_list_combobox').setEnabled(
                False
            )
        else:
            self.main_dialog.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            self.main_dialog.findChild(QTabWidget, 'tabset').setEnabled(True)
            self.main_dialog.findChild(QPushButton, 'paste_button').setEnabled(True)
            self.main_dialog.findChild(QRadioButton, 'simple_copy_radio').setEnabled(
                True
            )
            self.main_dialog.findChild(QPushButton, 'command_list_button').setEnabled(
                True
            )
            self.main_dialog.findChild(QRadioButton, 'standard_copy_radio').setEnabled(
                True
            )
            self.main_dialog.findChild(QCheckBox, 'delete_selections_check').setEnabled(
                True
            )
            self.main_dialog.findChild(QComboBox, 'documents_list_combobox').setEnabled(
                True
            )

    def __paste_button_clicked(self):
        self.__dialog_is_busy(True)
        runObj = MultiCopyCore.GuiObject()
        runObj.copy_document = doc
        runObj.selected_objects = self.selected_objs
        runObj.from_to = [
            self.main_dialog.findChild(QComboBox, 'from_combobox').currentIndex(),
            self.main_dialog.findChild(QComboBox, 'to_combobox').currentIndex(),
        ]
        runObj.separator = self.main_dialog.findChild(
            QLineEdit, 'add_separator_textbox'
        ).text()
        runObj.padding = self.main_dialog.findChild(
            QSpinBox, 'add_padding_spinbox'
        ).value()
        if self.main_dialog.findChild(
            QRadioButton, 'numbering_type_n_radio'
        ).isChecked():
            runObj.numbering_type = 1
        elif self.main_dialog.findChild(
            QRadioButton, 'numbering_type_ru_radio'
        ).isChecked():
            runObj.numbering_type = 2
        elif self.main_dialog.findChild(
            QRadioButton, 'numbering_type_rl_radio'
        ).isChecked():
            runObj.numbering_type = 3
        elif self.main_dialog.findChild(
            QRadioButton, 'numbering_type_au_radio'
        ).isChecked():
            runObj.numbering_type = 4
        elif self.main_dialog.findChild(
            QRadioButton, 'numbering_type_al_radio'
        ).isChecked():
            runObj.numbering_type = 5
        runObj.copy_type = (
            1
            if self.main_dialog.findChild(
                QRadioButton, 'standard_copy_radio'
            ).isChecked()
            else 2
        )
        runObj.dependencies = (
            True
            if self.main_dialog.findChild(QCheckBox, 'dependencies_check').isChecked()
            else False
        )
        runObj.delete_selection = (
            True
            if self.main_dialog.findChild(
                QCheckBox, 'delete_selections_check'
            ).isChecked()
            else False
        )
        runObj.paste_document = app.getDocument(
            self.list_of_documents[
                self.main_dialog.findChild(
                    QComboBox, 'documents_list_combobox'
                ).currentIndex()
            ]
        )
        if self.main_dialog.findChild(QTabWidget, 'tabset').currentIndex() == 0:
            runObj.is_paste_code = False
        else:
            runObj.is_paste_code = True
            runObj.paste_code = self.main_dialog.findChild(
                QPlainTextEdit, 'commands_input_textbox'
            ).toPlainText()
            if not MultiCopyCore.Validate(runObj.paste_code):
                MultiCopyAuxFunc.setAlertBox(
                    'The inputted Paste Code Commands are invalid.', True
                )
                return
        result = MultiCopyCore.RunFromGui(runObj)
        if result[0]:
            self.main_dialog.done(1)
            MultiCopyAuxFunc.setAlertBox(
                'The selected objects have been copy-pasted successfully!', None, True
            )
            app.Console.PrintMessage(
                '\nThe selected objects have been copy-pasted successfully!\n'
            )
        else:
            MultiCopyAuxFunc.setAlertBox(result[1], True)
            app.Console.PrintError('\n' + result[1] + '\n')
        self.__dialog_is_busy(False)

    def __launch(self):
        """This function generates and displays the MultiCopy GUI interface.

        It creates all the dialog boxes for user interaction and input.
        """
        self.main_dialog = gui.PySideUic.loadUi(
            app.getUserMacroDir(True) + '/MultiCopy/resources/MultiCopy_Main_Dialog.ui'
        )
        objects_list_textbox = self.main_dialog.findChild(
            QTextEdit, 'objects_list_textbox'
        )
        commands_input_textbox = self.main_dialog.findChild(
            QPlainTextEdit, 'commands_input_textbox'
        )
        # Adds a filter to detect Paste Code Commands changes in the 'commands_input_textbox' and
        # validate the same.
        _filter = Filter()
        _filter.sendObject(self)
        commands_input_textbox.installEventFilter(_filter)
        # Inserts the list of selected FreeCAD objects into the 'objects_list_textbox'.
        objects_list_textbox_text = '<table>'
        for i_, selected_obj in enumerate(self.selected_objs, 1):
            objects_list_textbox_text += (
                '<tr><td>['
                + str(i_)
                + ']</td><td>&nbsp;&nbsp;'
                + selected_obj.Label
                + '</td><td>&nbsp;&nbsp;&nbsp;&nbsp;&#60;'
                + str(selected_obj.TypeId).replace('\'', '')
                + '&#62;</td></tr>'
            )
        objects_list_textbox_text += '</table>'
        objects_list_textbox.setHtml(objects_list_textbox_text)
        commands_input_textbox.setPlainText('from ')
        commands_input_textbox.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)
        self.__numbering_type_radios_clicked()
        for docElem in self.list_of_documents:
            self.main_dialog.findChild(QComboBox, 'documents_list_combobox').addItem(
                app.getDocument(docElem).Label
            )
        self.main_dialog.findChild(
            QRadioButton, 'numbering_type_n_radio'
        ).clicked.connect(lambda: self.__numbering_type_radios_clicked())
        self.main_dialog.findChild(
            QRadioButton, 'numbering_type_ru_radio'
        ).clicked.connect(lambda: self.__numbering_type_radios_clicked())
        self.main_dialog.findChild(
            QRadioButton, 'numbering_type_rl_radio'
        ).clicked.connect(lambda: self.__numbering_type_radios_clicked())
        self.main_dialog.findChild(
            QRadioButton, 'numbering_type_au_radio'
        ).clicked.connect(lambda: self.__numbering_type_radios_clicked())
        self.main_dialog.findChild(
            QRadioButton, 'numbering_type_al_radio'
        ).clicked.connect(lambda: self.__numbering_type_radios_clicked())
        self.main_dialog.findChild(
            QCheckBox, 'delete_selections_check'
        ).toggled.connect(lambda: self.__delete_selections_check_toggled())
        self.main_dialog.findChild(QCheckBox, 'add_separator_check').toggled.connect(
            lambda: self.__add_separator_check_toggled()
        )
        self.main_dialog.findChild(QCheckBox, 'add_padding_check').toggled.connect(
            lambda: self.__add_padding_check_toggled()
        )
        self.main_dialog.findChild(QPushButton, 'paste_button').clicked.connect(
            lambda: self.__paste_button_clicked()
        )
        self.main_dialog.findChild(QTabWidget, 'tabset').currentChanged.connect(
            lambda: self.__tabset_tab_toggled()
        )
        self.main_dialog.findChild(QPushButton, 'command_list_button').clicked.connect(
            launch_commands_list_dialog
        )
        self.main_dialog.findChild(QPushButton, 'close_button').clicked.connect(
            lambda: self.main_dialog.done(1)
        )
        self.main_dialog.setWindowIcon(
            QIcon(app.getUserMacroDir(True) + '/MultiCopy/resources/MultiCopy.svg')
        )
        self.main_dialog.exec_()

    def __radio_operation(self, radioObjName, radioFunc):
        """This function decided the 'From' and 'To' combo-box options.

        This function is called when a radio buttons pertaining to one of
        the various 'Numbering Types' functions are toggled.

        Arguments
        ----------
        radioObjName: The object name of the clicked/toggled radio button.
        radioFunc: The 'Numbering Types' function associated with the radio button.
        """
        self.main_dialog.findChild(QComboBox, 'from_combobox').clear()
        self.main_dialog.findChild(QComboBox, 'from_combobox').addItems(radioFunc)
        self.main_dialog.findChild(QComboBox, 'from_combobox').setCurrentIndex(0)
        self.main_dialog.findChild(QComboBox, 'to_combobox').clear()
        self.main_dialog.findChild(QComboBox, 'to_combobox').addItems(radioFunc)
        self.main_dialog.findChild(QComboBox, 'to_combobox').setCurrentIndex(0)
        self.radio_prev = radioObjName

    def __numbering_type_radios_clicked(self):
        if (
            self.main_dialog.findChild(
                QRadioButton, 'numbering_type_n_radio'
            ).isChecked()
            and self.radio_prev != 'numbering_type_n_radio'
        ):
            self.__radio_operation(
                'numbering_type_n_radio', MultiCopyAuxFunc.OrdinaryNumerals(0, 500)
            )
        elif (
            self.main_dialog.findChild(
                QRadioButton, 'numbering_type_ru_radio'
            ).isChecked()
            and self.radio_prev != 'numbering_type_ru_radio'
        ):
            self.__radio_operation(
                'numbering_type_ru_radio',
                MultiCopyAuxFunc.UpperCaseRomanNumerals(1, 200),
            )
        elif (
            self.main_dialog.findChild(
                QRadioButton, 'numbering_type_rl_radio'
            ).isChecked()
            and self.radio_prev != 'numbering_type_rl_radio'
        ):
            self.__radio_operation(
                'numbering_type_rl_radio',
                MultiCopyAuxFunc.LowerCaseRomanNumerals(1, 200),
            )
        elif (
            self.main_dialog.findChild(
                QRadioButton, 'numbering_type_au_radio'
            ).isChecked()
            and self.radio_prev != 'numbering_type_au_radio'
        ):
            self.__radio_operation(
                'numbering_type_au_radio', MultiCopyAuxFunc.UpperCaseAlphabet(1, 702)
            )
        elif (
            self.main_dialog.findChild(
                QRadioButton, 'numbering_type_al_radio'
            ).isChecked()
            and self.radio_prev != 'numbering_type_al_radio'
        ):
            self.__radio_operation(
                'numbering_type_al_radio', MultiCopyAuxFunc.LowerCaseAlphabet(1, 702)
            )

    def __delete_selections_check_toggled(self):
        if self.main_dialog.findChild(QCheckBox, 'delete_selections_check').isChecked():
            quest_reply = QMessageBox.question(
                None,
                'MultiCopy - Warning Question',
                'Are you sure you want to delete the selected object(s)?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if quest_reply == QMessageBox.No:
                self.main_dialog.findChild(
                    QCheckBox, 'delete_selections_check'
                ).setChecked(False)

    def __add_separator_check_toggled(self):
        self.main_dialog.findChild(QLineEdit, 'add_separator_textbox').setText('')
        if self.main_dialog.findChild(QCheckBox, 'add_separator_check').isChecked():
            self.main_dialog.findChild(QLineEdit, 'add_separator_textbox').setEnabled(
                True
            )
        else:
            self.main_dialog.findChild(QLineEdit, 'add_separator_textbox').setEnabled(
                False
            )

    def __add_padding_check_toggled(self):
        self.main_dialog.findChild(QSpinBox, 'add_padding_spinbox').setValue(1)
        if self.main_dialog.findChild(QCheckBox, 'add_padding_check').isChecked():
            self.main_dialog.findChild(QSpinBox, 'add_padding_spinbox').setEnabled(True)
        else:
            self.main_dialog.findChild(QSpinBox, 'add_padding_spinbox').setEnabled(
                False
            )

    def __tabset_tab_toggled(self):
        if self.main_dialog.findChild(QTabWidget, 'tabset').currentIndex() == 1:
            self.main_dialog.findChild(
                QPlainTextEdit, 'commands_input_textbox'
            ).setFocus()
        self.main_dialog.findChild(QPushButton, 'paste_button').setEnabled(True)


class __PasteCodeCommands_Dialog:

    """This function launches the 'Paste Code Commands List' dialog box over the main open dialog box."""

    def __init__(self):
        commands_dialog = gui.PySideUic.loadUi(
            app.getUserMacroDir(True)
            + '/MultiCopy/resources/MultiCopy_Commands_Dialog.ui'
        )
        commands_dialog.findChild(QPushButton, 'okay_button').clicked.connect(
            lambda: commands_dialog.done(1)
        )
        commands_dialog.setWindowIcon(
            QIcon(app.getUserMacroDir(True) + 'MultiCopy.svg')
        )
        commands_dialog.exec_()


# Sub-main (Secondary) Classes
# ------------------------------------------------------------------------------------------------


class Filter(QtCore.QObject):
    """This class performs semi-real-time validation of
    the input paste code commands.

    It performs the validation when the user focusses out of
    the input text box. Appropriately, the GUI interface may
    change by blocking access to certain GUI elements if
    the validation returns a false value.
    """

    def sendObject(self, argObj):
        self.dialogObj = argObj

    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.FocusIn:
            widget.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)
            self.dialogObj.main_dialog.findChild(
                QLabel, 'validation_signal_label'
            ).setStyleSheet('background-color:#1c1c1c')
            self.dialogObj.main_dialog.findChild(
                QPushButton, 'paste_button'
            ).setEnabled(True)
            return False
        elif event.type() == QtCore.QEvent.FocusOut:
            self.dialogObj._Launch_Main_Dialog__dialog_is_busy(True)
            if MultiCopyCore.Validate(
                self.dialogObj.main_dialog.findChild(
                    QPlainTextEdit, 'commands_input_textbox'
                ).toPlainText()
            ):
                self.dialogObj.main_dialog.findChild(
                    QLabel, 'validation_signal_label'
                ).setStyleSheet('background-color:darkgreen')
            else:
                self.dialogObj.main_dialog.findChild(
                    QLabel, 'validation_signal_label'
                ).setStyleSheet('background-color:crimson')
            self.dialogObj._Launch_Main_Dialog__dialog_is_busy(False)
            return False
        else:
            return False


# Public (User) Functions
# ------------------------------------------------------------------------------------------------


def launch_commands_list_dialog():
    __PasteCodeCommands_Dialog()


def Launch():
    """This function checks whether or not the user has selected one or more objects.

    It then calls the '_Launch_Main_Dialog' class.
    """
    if len(gui.Selection.getSelection()) > 0:
        __Launch_Main_Dialog()
    else:
        message = 'No FreeCAD objects have been selected for MultiCopy!'
        message_box = QMessageBox(
            QMessageBox.Critical, 'MultiCopy - Error Message', message
        )
        message_box.setWindowModality(QtCore.Qt.ApplicationModal)
        message_box.exec_()


def Run():
    """This function is an alias of the 'Launch()' function."""
    Launch()
