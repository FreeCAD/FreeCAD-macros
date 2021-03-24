#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
import re
from . import MultiCopyAuxFunc


# Constant Variables
# ------------------------------------------------------------------------------------------------

# It is the currently active FreeCAD document.
doc = app.activeDocument()
# It is the maximum digits for padding numbered labels of objects.
# e.g. 00001, 00111, etc.
MAX_PAD_DIGITS = 5
# It is a random string, to be used as a placeholder while changing certain variables
# and then testing against it to determine if the variable has indeed changed.
RANDOM_STRING_1 = "✍✉☏⌨"
# This variable is used solely by the '__solve_paste_code' function.
# The random string will act as the count variable prefix within the parsed python code.
RANDOM_STRING_2 = "ugmfdkGNxL"
# It is a set of partial Paste Code Commands that deals with the various
# numbering types: n, N for Ordinary Numerals; ru, RU, R for Upper-case
# Roman Numerals; r, rl, RL, for Lower-case Roman Numerals;
# au, AU, A for the Upper-case Alphabet; and a, al, AL for the
# Lower-case Alphabet. Note that the multiplicity of choices
# allows the user to use the ones that are preferable.
NUMERALS_CODE = [
    "n#",
    "N#",
    "ru#",
    "RU#",
    "R#",
    "r#",
    "rl#",
    "RL#",
    "au#",
    "AU#",
    "A#",
    "a#",
    "al#",
    "AL#",
]


# Global Variables
# ------------------------------------------------------------------------------------------------

global_objIDList = []
# It contains the integer-based ID's of the objects being dealt with.


# MultiCopy GuiObject Class
# ------------------------------------------------------------------------------------------------


class GuiObject:
    def __init__(self):
        self.padding = 1
        self.from_to = []
        self.copy_type = 1
        self.separator = ""
        self.paste_code = ""
        self.numbering_type = 1
        self.dependencies = False
        self.is_paste_code = False
        self.selected_objects = []
        self.delete_selection = True
        self.copy_document = None
        self.paste_document = None


# Private (Secondary) Functions
# ------------------------------------------------------------------------------------------------


def __stdCopy_op(obj, dependencyArg, copy_doc, paste_doc):
    """Perform the 'Standard Copy' of an object.

    Parameters
    ----------
    obj: (FreeCAD.Object)
            An object.
    dependencyArg: (bool)
            Represents whether the duplication is
            with dependencies (1) or without (0).

    Return
    ----------
    (None)
    """
    paste_doc.copyObject(obj, dependencyArg)


def __simpleCopy_op(obj, dummyVar, copy_doc, paste_doc):
    """Perform the 'Simple Copy' of an object.

    Parameters
    ----------
    obj: (FreeCAD.Object)
            An object.
    dummyVar: (*)
            A dummy variable.

    Return
    ----------
    (None)
    """
    gui.Selection.clearSelection()
    gui.Selection.addSelection(obj)
    app.setActiveDocument(paste_doc.Name)
    gui.runCommand("Part_SimpleCopy")
    app.setActiveDocument(copy_doc.Name)


def __rename(refObj, newName, rename_document):
    """Search the document for a newly added object and rename it.

    Parameters
    ----------
    refObj: (FreeCAD.Object)
            The copied (not pasted) object.
    newName: (str)
            The renaming text.
    rename_document_name: (FreeCAD.Document)
            The document in which the object is to be renamed.

    Return
    ----------
    (None)
    """
    global global_objIDList
    objList = [
        objElem
        for objElem in rename_document.Objects
        if not str(objElem.ID) in global_objIDList
    ]
    for objElem in objList:
        if objElem.TypeId == refObj.TypeId and objElem.ID != refObj.ID:
            try:
                objElemLabel = objElem.Label.replace(
                    re.findall(r"\d+", objElem.Label)[-1], ""
                )
            except Exception:
                objElemLabel = objElem.Label
            try:
                refObjElem = refObj.Label.replace(
                    re.findall(r"\d+", refObj.Label)[-1], ""
                )
            except Exception:
                refObjElem = refObj.Label
            if objElemLabel == refObjElem:
                global_objIDList.append(str(objElem.ID))
                break
    objElem.Label = newName


def __get_tabs_n(testString):
    """Get the number of prefix tabs of a string.

    It is the string of one or more tabs (\\t) at
    the start of the line of a given text string.

    This function performs an auxiliary operation that is
    part of the '__solve_paste_code' and the
    validation functions.

    Parameters
    ----------
    testString: (str)
            Text string containing a line of the input Paste Code.

    Return
    ----------
    (str): The first word in the input string.
    """
    n_sum = 0
    for testChar in testString:
        if testChar == "\t":
            n_sum += 1
        else:
            break
    return n_sum


def __to_numerics(argStr):
    """Convert alphabetic and roman numeral characters into ordinary numerical digits.

    This function performs an auxiliary operation that is
    part of the '__solve_paste_code' function itself.

    Parameters
    ----------
    argStr: (str)
            Text string containing solely alphabetic or
            roman numeral characters.

    Return
    ----------
    (str): The converted numerical string.
    """
    try:
        return str(MultiCopyAuxFunc.ALPHA_MAP.index(argStr.lower()))
    except Exception:
        try:
            return str(MultiCopyAuxFunc.ROMAN_NUMERAL_MAP[0].index(argStr.upper()))
        except Exception:
            return argStr


def __solve_numerals_code(codeStr, indexStr):
    """Parse the paste code commands that contain data relevant to the global variable 'NUMERALS_CODE'.

    This function performs an auxiliary operation that is part of
    the '__solve_paste_code' function itself.

    Parameters
    ----------
    codeStr: (str)
            Text string containing elements from the
            global variable 'NUMERALS_CODE'.
    indexStr: (str)
            Name of the index/count variable for use
            in a typical python 'for' loop.

    Return
    ----------
    (str): The converted string.

    Example
    ----------
    >>> __solve_numerals_code('n#3','i')
    \"\' + str(i).zfill(3) + \'\"
    >>> __solve_numerals_code('RU#','i')
    \"\' + MultiCopyAuxFunc.UpperCaseRomanNumerals(i,i)[0].zfill(0) + \'\"
    """
    codeStr1 = codeStr[0 : codeStr.index("#")]
    codeStr2 = "0"
    if len(codeStr) - len(codeStr1) > 1:
        if codeStr.count("|") == 1:
            indexStr = codeStr[codeStr.index("|") + 1 :]
            codeStr2 = codeStr[codeStr.index("#") + 1 : codeStr.index("|")]
        else:
            codeStr2 = codeStr[codeStr.index("#") + 1 :]
    codeStr2 = "0" if len(codeStr2) == 0 else codeStr2
    if codeStr1 == "n" or codeStr1 == "N":
        return "' + str(" + indexStr + ").zfill(" + codeStr2 + ") + '"
    elif codeStr1 == "ru" or codeStr1 == "RU" or codeStr1 == "R":
        return (
            "' + MultiCopyAuxFunc.UpperCaseRomanNumerals("
            + indexStr
            + ","
            + indexStr
            + ")[0].zfill("
            + codeStr2
            + ") + '"
        )
    elif codeStr1 == "r" or codeStr1 == "rl" or codeStr1 == "RL":
        return (
            "' + MultiCopyAuxFunc.LowerCaseRomanNumerals("
            + indexStr
            + ","
            + indexStr
            + ")[0].zfill("
            + codeStr2
            + ") + '"
        )
    elif codeStr1 == "au" or codeStr1 == "AU" or codeStr1 == "A":
        return (
            "' + MultiCopyAuxFunc.UpperCaseAlphabet("
            + indexStr
            + ","
            + indexStr
            + ")[0].zfill("
            + codeStr2
            + ") + '"
        )
    elif codeStr1 == "a" or codeStr1 == "al" or codeStr1 == "AL":
        return (
            "' + MultiCopyAuxFunc.LowerCaseAlphabet("
            + indexStr
            + ","
            + indexStr
            + ")[0].zfill("
            + codeStr2
            + ") + '"
        )


def __validate_check_from_to(lineOfText, tags_list, tabs_n, isFixed):
    """Validate the generic 'from ... to ...' parts of the input paste code commands.

    This function performs an auxiliary operation that is part of
    the 'Validate' function itself.

    Arguments
    ----------
    lineOfText: (str)
            Text string containing a line of the inputted Paste Code.
    tags_list: (list)
            List of 'from...to' loops' user-assigned variables.
    tabs_n: (int)
            Maximum number of tabs to be present in the given line of code.
    isFixed: (book)
            True, if the 'tabs_n' argument is to considered as fixed.
            (meaning, equal to, and not maximum)

    Return
    ----------
    (bool): A boolean denoting the function's success.
    """
    if tabs_n != 0 and (__get_tabs_n(lineOfText) > tabs_n):
        return False
    if isFixed and __get_tabs_n(lineOfText) != tabs_n:
        return False
    if (
        lineOfText.count("from") != 1
        or lineOfText.count("to") != 1
        or (lineOfText.count(":") not in [1, 2])
    ):
        return False
    textElementsList = lineOfText.rstrip().split(" ")
    textElementsList = [
        elem for elem in textElementsList if elem != " " and elem != "\t"
    ]
    if len(textElementsList) not in [5, 7]:
        return False
    if textElementsList[4] != ":":
        return False
    if len(textElementsList) == 7:
        # digits_exist = False
        # for charElem in textElementsList[5]:
        # 	if charElem.isnumeric():
        # 		digits_exist = True
        # 		break
        if len(textElementsList[5]) == 0:
            return False
        if (
            textElementsList[6] != ":"
            or not textElementsList[5][0].isalpha()
            or not textElementsList[5].isalnum()
        ):  # or not digits_exist:
            return False
        tags_list.append(textElementsList[5])
    if textElementsList[1].isnumeric() and textElementsList[3].isnumeric():
        if int(textElementsList[1]) == int(textElementsList[3]) == 0:
            return True
        if int(textElementsList[3]) == 0:
            return False
        if (
            abs(int(textElementsList[1])) / float(textElementsList[1]) == 1
            and abs(int(textElementsList[3])) / float(textElementsList[3]) == 1
            and int(textElementsList[1]) <= 500
            and int(textElementsList[3]) <= 500
            and int(textElementsList[1]) <= int(textElementsList[3])
        ):
            return True
    elif not textElementsList[1].isnumeric() and not textElementsList[3].isnumeric():
        elem_2_and_4_str = textElementsList[1] + textElementsList[3]
        elemType1Exists, elemType2Exists = True, True
        for elem_2_and_4_char in elem_2_and_4_str:
            # The purpose of the 'tempVar' variable is to check whether or not
            # alphabetic characters or roman numerals are present in the
            # '...' positions of the 'from...to...' statement.
            try:
                tempVar = MultiCopyAuxFunc.ALPHA_MAP.index(elem_2_and_4_char.lower())
            except Exception:
                del tempVar
                elemType1Exists = False
                break
        for elem_2_and_4_char in elem_2_and_4_str:
            try:
                tempVar = MultiCopyAuxFunc.ROMAN_NUMERAL_MAP[0].index(
                    elem_2_and_4_char.upper()
                )
            except Exception:
                del tempVar
                if elemType1Exists:
                    elemType2Exists = False
                    break
                else:
                    return False
        if not elemType1Exists or (elemType1Exists and elemType2Exists):
            if MultiCopyAuxFunc.RomanToInt(
                textElementsList[3].upper()
            ) >= MultiCopyAuxFunc.RomanToInt(textElementsList[1].upper()):
                return True
        else:
            if MultiCopyAuxFunc.AlphaToInt(
                textElementsList[3].lower()
            ) >= MultiCopyAuxFunc.AlphaToInt(textElementsList[1].lower()):
                return True
    return False


def __validate_check_assignment(lineOfText, tags_list, tabs_n):
    """Validate the generic '[...] =  ...' parts of the input paste code commands.

    This function performs an auxiliary operation that is part of
    the 'Validate' function itself.

    Arguments
    ----------
    lineOfText: (str)
            Text string containing a line of the inputted Paste Code.
    tags_list: (list)
            List of 'from...to' loops' user-assigned variables.
    tabs_n: (int)
            Maximum number of tabs to be present in the given line of code.
    isFixed: (book)
            True, if the 'tabs_n' argument is to considered as fixed.
            (meaning, equal to, and not maximum)

    Return
    ----------
    (bool): A boolean denoting the function's success.
    """
    if tabs_n != 0 and (__get_tabs_n(lineOfText) > tabs_n):
        return False
    lineOfText_copy = lineOfText
    if tabs_n > 0:
        lineOfText_copy = lineOfText.replace("\t", "")
    textElementsList = lineOfText_copy.split(" ")
    textElementsList = [elem for elem in textElementsList if elem != " " or elem != ""]
    if len(textElementsList[0]) < 3:
        return False
    if (
        textElementsList[0][0] != "["
        or textElementsList[0][-1] != "]"
        or textElementsList[1] != "="
    ):
        return False
    # The 'tempStr1' variable contains the text element within the '[' and ']' (square) brackets.
    tempStr1 = textElementsList[0][1:-1]
    if "|" in tempStr1:
        # The 'tempVar1' and 'tempVar2' variables check whether or not the 'tempStr1' variable's
        # text contents beside the '|' (pipe) character contain appropriate numerical values.
        tempVar1 = tempStr1[0 : tempStr1.index("|")]
        tempVar2 = tempStr1[tempStr1.index("|") + 1 :]
        if tempVar1.isnumeric() and tempVar2.isnumeric():
            tempBool = int(tempVar2) in [0, 1]
        else:
            tempBool = False
    else:
        tempBool = tempStr1.isnumeric() or tempBool
    if not tempBool:
        return False
    input_label_text = (
        "".join(textElementsList[2:])
        .replace("\t", "")
        .replace("\n", "")
        .replace("\r", "")
        .strip()
    )
    if input_label_text.count("\{") != input_label_text.count("\}"):
        return False
    input_label_text = input_label_text.replace("\{", "").replace("\}", "")
    if input_label_text.count("{") != input_label_text.count("}"):
        return False
    while input_label_text.count("{") > 0:
        # The 'tempStr2' variable is used to test the validity of the 'input_label_text' text value
        # within the '{' and '}' (curly) brackets.
        tempStr2 = RANDOM_STRING_1
        codeFound = False
        try:
            tempStr2 = input_label_text[
                input_label_text.index("{") : input_label_text.index("}")
            ]
        except Exception:
            return False
        for ncElem in NUMERALS_CODE:
            if ncElem in tempStr2:
                codeFound = True
                break
        if codeFound:
            if tempStr2.count("|") > 1:
                return False
            # The 'tempVar' variable checks whether or not the 'tempStr2' variable's
            # text contents between the '#' (hash) and '|' (pipe) characters, in any,
            # contain appropriate numerical values.
            if tempStr2.count("|") == 1:
                tempVar = tempStr2[tempStr2.index("#") + 1 : tempStr2.index("|")]
                # The 'tempStr3' variable tests for the presence of the 'tags_list' elements
                # within the 'tempStr2' variable's text value, to the right of the
                # '|' (pipe) character.
                tempStr3 = tempStr2[tempStr2.index("|") + 1 :]
                if len(tempStr3) == 0:
                    return False
                if not tempStr3 in tags_list:
                    return False
            else:
                tempVar = tempStr2[tempStr2.index("#") + 1 :]
            if len(tempVar) != 0 and not tempVar.isnumeric():
                return False
            if len(tempVar) != 0 and int(tempVar) != float(tempVar):
                return False
            if len(tempVar) != 0 and int(tempVar) > MAX_PAD_DIGITS:
                return False
            input_label_text = input_label_text.replace(tempStr2 + "}", "", 1)
        else:
            if tempStr2[1:].isnumeric():
                input_label_text = input_label_text.replace(tempStr2 + "}", "", 1)
            else:
                return False
    return True


def __solve_paste_code(objectsList, paste_document, paste_code):
    """Parse the input paste code commands into the python code format and tests for its validity.

    Parameters
    ----------
    objectsList: (list)
            List of selected FreeCAD objects.
    paste_document: (FreeCAD.Document)
            The name of the document in which
            the objects are to be pasted.
    paste_code: (str)
            The paste code commands string.

    Return
    ----------
    ([bool, str]):  If 'True', then the parsed code itself;
                    else, the error message.
    """
    # The 'i_count' variable denotes the number of 'from...to...' loops: i1, i2, i3, etc.
    i_count = 0
    testCode = ""
    from_index = 0
    alertMessage = ""
    parsableCode = "copy_op = __stdCopy_op if copy_type == 1 else __simpleCopy_op\n"
    assignedLabelsList = []
    paste_code_list = paste_code.split("\n")
    paste_code_list = [elem for elem in paste_code_list if elem != "\n" and elem != ""]
    for i in range(len(paste_code_list)):
        first_word = paste_code_list[i].split(maxsplit=1)[0]
        textElementsList = paste_code_list[i].split(" ")
        textElementsList = [i.replace("\t", "") for i in textElementsList]
        if first_word == "from":
            i_count += 1
            from_index = int(__to_numerics(textElementsList[1]))
            to_index = int(__to_numerics(textElementsList[3])) + 1
            if from_index > to_index:
                return [
                    False,
                    "The 'From' value cannot be greater than the 'To' value!",
                ]
            parsableCode += (
                ("\t" * __get_tabs_n(paste_code_list[i]))
                + "for "
                + RANDOM_STRING_2
                + str(i_count)
                + " in range("
                + __to_numerics(textElementsList[1])
                + ","
                + str(int(__to_numerics(textElementsList[3])) + 1)
                + "):\n"
            )
            if len(textElementsList) == 7:
                parsableCode += "\t" * (__get_tabs_n(paste_code_list[i]) + 1)
                parsableCode += (
                    textElementsList[5] + "=" + RANDOM_STRING_2 + str(i_count) + "\n"
                )
        else:
            if "|" in textElementsList[0]:
                assignedIndex = (
                    int(
                        "".join(textElementsList[0][1 : textElementsList[0].index("|")])
                    )
                    - 1
                )
                dependency = (
                    1
                    if int(
                        "".join(
                            textElementsList[0][textElementsList[0].index("|") + 1 : -1]
                        )
                    )
                    == 1
                    else 0
                )
            else:
                assignedIndex = int("".join(textElementsList[0][1:-1])) - 1
                dependency = 0
            if assignedIndex < 0 or assignedIndex >= len(objectsList):
                alertMessage = "Only numbers between 1 and " + str(len(objectsList))
                alertMessage += " are allowed within the brackets. "
                alertMessage += "The following snippet produced the error :\n\n"
                alertMessage += "[" + str(assignedIndex) + "]"
                return [False, alertMessage]
            assignedString = "".join(textElementsList[2:])
            assignedString = (
                assignedString.replace("\t", "").replace("\n", "").replace("\r", "")
            )
            assignedString = assignedString.strip()
            j = 0
            assignedLabel = ""
            while j < len(assignedString):
                if assignedString[j] == "{":
                    if assignedString[j + 1].isnumeric():
                        # The 'tempVar' variable contains the numerical value of the
                        # 'assignedString' variable, if it is numeric.
                        tempVar = int(
                            assignedString[j + 1 : assignedString.index("}", j + 1)]
                        )
                        if tempVar > 0 and tempVar <= len(objectsList):
                            assignedLabel += objectsList[tempVar - 1].Label
                            j = assignedString.index("}", j + 1) + 1
                        else:
                            alertMessage = "Only numbers between 1 and " + str(
                                len(objectsList)
                            )
                            alertMessage += " are allowed within the brackets. "
                            alertMessage += (
                                "The following snippet produced the error :\n\n"
                            )
                            alertMessage += "{" + str(tempVar) + "}"
                            return [False, alertMessage]
                    else:
                        # Here, the 'tempVar' variable is a test variable to check whether or not
                        # the test was successful.
                        tempVar = j
                        for ncElem in NUMERALS_CODE:
                            if (
                                ncElem
                                in assignedString[
                                    j : assignedString.index("#", j + 1) + 1
                                ]
                            ):
                                input_ncElem = assignedString[
                                    j + 1 : assignedString.index("}", j + 1)
                                ]
                                if "n#" in ncElem.lower():
                                    i_str = str(i_count)
                                else:
                                    i_str = (
                                        str(i_count) + "+1"
                                        if from_index == 0
                                        else str(i_count)
                                    )
                                input_ncElem = __solve_numerals_code(
                                    input_ncElem, RANDOM_STRING_2 + i_str
                                )
                                assignedLabel += input_ncElem
                                j = assignedString.index("}", j + 1) + 1
                                break
                        if j == tempVar:
                            return [
                                False,
                                "The paste code commands contain some undetectable, invalid elements.",
                            ]
                else:
                    if assignedString[j] == "\\":
                        assignedLabel += "\\"
                    elif assignedString[j] == "'":
                        assignedLabel += "'"
                    elif assignedString[j] == "'":
                        assignedLabel += "'"
                    else:
                        assignedLabel += assignedString[j]
                    j += 1
            if not assignedLabel in assignedLabelsList:
                assignedLabelsList.append(assignedLabel)
            else:
                alertMessage = (
                    "The following label creates duplicates within the input code :\n\n"
                )
                alertMessage += assignedLabel
                return [False, alertMessage]
            parsableCode += (
                ("\t" * __get_tabs_n(paste_code_list[i]))
                + "copy_op(selected_objs["
                + str(assignedIndex)
            )
            parsableCode += (
                "], " + str(dependency) + ", copy_document, paste_document)\n"
            )
            parsableCode += (
                "\t" * __get_tabs_n(paste_code_list[i])
            ) + "__rename(selected_objs["
            parsableCode += (
                str(assignedIndex) + "], '" + assignedLabel + "', paste_document)\n"
            )
    testFailed = False
    testCode = "for labelElem in assignedLabelsList:\n\t"
    testCode += "if len(paste_document.getObjectsByLabel(labelElem)) > 0:\n\t\t"
    testCode += "testVar = labelElem\n\t\t"
    testCode += "testFailed = True\n\t\t"
    testCode += "break\n\n"
    testCode += "if testFailed:\n\talertMessage = "
    testCode += "'An object containing the following label already exists in the document :\\n\\n'\n\t"
    testCode += "alertMessage += testVar\n"
    exec(testCode)
    if testFailed:
        if not alertMessage:
            alertMessage = "Unexpected error occurred during the MultiCopy operation! Please report."
        return [False, alertMessage]
    else:
        return [True, parsableCode]


# Private (Main / Primary) Functions
# ------------------------------------------------------------------------------------------------


def __RunPasteCommands(guiObj):
    """Perform the 'Paste' operation based on the user's various input parameters.

    This function is the '__RunPasteCode' function's GUI equivalent.
    This function is called when the 'Paste' button is clicked.

    Parameters
    ----------
    guiObj: (GuiObject)
            A MultiCopy GuiObject.

    Return
    ----------
    ([bool, str]):  A boolean denoting the function's success,
                    and an error message if false or an
                    empty string.
    """
    global global_objIDList
    for obj in guiObj.copy_document.Objects:
        global_objIDList.append(str(obj.ID))
    if guiObj.numbering_type == 1:
        naming_func = MultiCopyAuxFunc.OrdinaryNumerals
    else:
        guiObj.from_to[0] += 1
        guiObj.from_to[1] += 1
    if guiObj.numbering_type == 2:
        naming_func = MultiCopyAuxFunc.UpperCaseRomanNumerals
    elif guiObj.numbering_type == 3:
        naming_func = MultiCopyAuxFunc.LowerCaseRomanNumerals
    elif guiObj.numbering_type == 4:
        naming_func = MultiCopyAuxFunc.UpperCaseAlphabet
    elif guiObj.numbering_type == 5:
        naming_func = MultiCopyAuxFunc.LowerCaseAlphabet
    obj_exists = False
    for obj in guiObj.selected_objects:
        if not obj_exists:
            for i in range(guiObj.from_to[0], guiObj.from_to[1] + 1):
                renamed_obj_label = (
                    obj.Label
                    + guiObj.separator
                    + naming_func(i, i)[0].zfill(guiObj.padding)
                )
                if len(guiObj.paste_document.getObjectsByLabel(renamed_obj_label)) > 0:
                    obj_exists = True
                    break
        else:
            break
    if obj_exists:
        return [
            False,
            "The object '" + renamed_obj_label + "' already exists in the document!",
        ]
    copy_op = __stdCopy_op if guiObj.copy_type == 1 else __simpleCopy_op
    for obj in guiObj.selected_objects:
        for j in range(guiObj.from_to[0], guiObj.from_to[1] + 1):
            copy_op(
                obj, guiObj.dependencies, guiObj.copy_document, guiObj.paste_document
            )
            __rename(
                obj,
                obj.Label
                + guiObj.separator
                + naming_func(j, j)[0].zfill(guiObj.padding),
                guiObj.paste_document,
            )
    if guiObj.delete_selection:
        for obj in guiObj.selected_objects:
            obj.removeObjectsFromDocument()
            guiObj.copy_document.removeObject(obj.Name)
    guiObj.copy_document.recompute()
    guiObj.paste_document.recompute()
    return [True, ""]


def __RunPasteCode(
    selected_objs,
    code_string,
    paste_document,
    copy_document,
    copy_type,
    delete_selection,
):
    """Perform the 'Paste' operation based on the user's various input parameters.

    This function is the '__RunPasteCommands' function's CUI equivalent.

    Parameters
    ----------
    selected_objs: (list)
            List of selected FreeCAD objects.
    code_string: (str)
            The paste code commands string.
    paste_document: (FreeCAD.Document)
            The document to paste to.
    copy_document: (FreeCAD.Document)
            The document to copy from.
    copy_type: (bool)
            The copy operation mode.
    delete_selection: (bool)
            If true, the selected objects are deleted
            after the MultiCopy operation.

    Return
    ----------
    ([bool, str]):  A boolean denoting the function's success,
                    and an error message if false or an
                    empty string.
    """
    result = __solve_paste_code(selected_objs, paste_document, code_string)
    if result[0]:
        exec(result[1])
        if delete_selection:
            for obj in selected_objs:
                obj.removeObjectsFromDocument()
                copy_document.removeObject(obj.Name)
        copy_document.recompute()
        paste_document.recompute()
        return [True, ""]
    else:
        return [False, result[1]]


# Public (User) Functions
# ------------------------------------------------------------------------------------------------


def GetDocumentsList(docObj=None):
    """This function gets a list of currently open FreeCAD documents.

    This function is to be called from another function or module for
    obtaining an updated list of currently open FreeCAD documents.
    This function is not meant to be called directly from the
    FreeCAD application.

    Parameters
    ----------
    docObj: (FreeCAD.Document)
            [Optional]
            The document to be placed at the start of the list.
            Default: None

    Return
    ----------
    (list): List of FreeCAD documents.
    """
    listArg = []
    if docObj:
        listArg.append(docObj.Name)
    for itemsSet in app.listDocuments().items():
        for itemElem in itemsSet:
            if (docObj and itemElem != listArg[0]) or not docObj:
                listArg.append(itemElem)
            break
    return listArg


def Validate(code_string):
    """Performs syntactic validation of the input paste code commands.

    This function performs the validation when the user focusses out of
    the associated input text box.

    Parameters
    ----------
    code_string: (str)
            The paste code commands string.

    Return
    ----------
    (bool): 'True' is the code is valid; else, 'False'
    """
    tab_n = 0
    tags_list = []
    isCodeValid = False
    fromCodeCompleted = False
    paste_code_list = code_string.split("\n")
    paste_code_list = [elem for elem in paste_code_list if elem != "\n" and elem != ""]
    try:
        first_word = paste_code_list[0]
    except Exception:
        first_word = ""
    if len(code_string) == 0 or len(first_word) == 0:
        return False
    if first_word.split(maxsplit=1)[0] != "from":
        return False
    for i in range(len(paste_code_list)):
        first_word = paste_code_list[i].split(maxsplit=1)[0]
        if first_word == "from":
            if fromCodeCompleted:
                fromCodeCheck = __validate_check_from_to(
                    paste_code_list[i], tags_list, tab_n, False
                )
                tab_n = __get_tabs_n(paste_code_list[i])
            else:
                fromCodeCheck = __validate_check_from_to(
                    paste_code_list[i], tags_list, tab_n, True
                )
            fromCodeCompleted = False
            if fromCodeCheck and i < len(paste_code_list) - 1:
                if paste_code_list[i + 1][0 : tab_n + 1] == "\t" * (tab_n + 1):
                    tab_n += 1
                    isCodeValid = True
                else:
                    isCodeValid = False
                    break
            else:
                isCodeValid = False
                break
        elif len(first_word) >= 3:
            if __validate_check_assignment(paste_code_list[i], tags_list, tab_n):
                isCodeValid = True
                fromCodeCompleted = True
            else:
                isCodeValid = False
                break
        else:
            isCodeValid = False
            break
    return isCodeValid


def RunFromGui(guiObj):
    """Perform the MultiCopy operation by inputting a MultiCopy GuiObject.

    This function is to be called from another function after the required data
    has been collected from the GUI elements of the MultiCopy programme.
    This function is not meant to be called directly from the FreeCAD application.

    Parameters
    ----------
    guiObj: (GuiObject)
            A MultiCopy GuiObject.

    Return
    ----------
    ([bool, str]):  A boolean denoting the function's success,
                    and an error message if false or an
                    empty string.
    """
    if not isinstance(guiObj, GuiObject):
        return False
    if (
        not isinstance(guiObj.padding, int)
        or not isinstance(guiObj.from_to, list)
        or not isinstance(guiObj.copy_type, int)
        or not isinstance(guiObj.numbering_type, int)
        or not isinstance(guiObj.dependencies, bool)
        or not isinstance(guiObj.is_paste_code, bool)
        or not isinstance(guiObj.delete_selection, bool)
        or not isinstance(guiObj.selected_objects, list)
        or not isinstance(guiObj.separator, str)
        or not isinstance(guiObj.paste_code, str)
    ):
        raise TypeError("Some arguments contain values of incorrect type.")
        return [False, ""]  # lgtm [py/unreachable-statement]
    if not guiObj.selected_objects:
        raise ValueError("The selected_objects list is empty.")
        return [False, ""]  # lgtm [py/unreachable-statement]
    try:
        dummyVar = guiObj.copy_document.Label
    except Exception as err:
        raise Exception(str(err))
        return [False, ""]  # lgtm [py/unreachable-statement]
    del dummyVar
    if not all(isinstance(elem, int) for elem in guiObj.from_to):
        raise TypeError("The 'From' and 'To' indices must be of integer values.")
        return [False, ""]  # lgtm [py/unreachable-statement]
    for obj in guiObj.selected_objects:
        if not obj:
            raise ValueError("One of the selected objects does not exist.")
            return [False, ""]  # lgtm [py/unreachable-statement]
    if guiObj.from_to[0] > guiObj.from_to[1]:
        return [False, "The 'From' value cannot be greater than the 'To' value!"]
    if guiObj.is_paste_code:
        if not Validate(guiObj.paste_code):
            return [False, "The inputted Paste Code Commands are invalid."]
        return __RunPasteCode(
            guiObj.selected_objects,
            guiObj.paste_code,
            guiObj.paste_document,
            guiObj.copy_document,
            guiObj.copy_type,
            guiObj.delete_selection,
        )
    else:
        if (
            guiObj.padding not in range(1, MAX_PAD_DIGITS + 1, 1)
            or guiObj.copy_type not in [1, 2]
            or guiObj.numbering_type not in range(1, 5 + 1, 1)
        ):
            raise ValueError(
                "Some integer-based arguments contain values of incorrect range."
            )
            return [False, ""]  # lgtm [py/unreachable-statement]
        return __RunPasteCommands(guiObj)


def Run(paste_code, copy_type=True, delete_selection=False, paste_document_label=None):
    """Perform the MultiCopy operation by inputting the required arguments.

    This is a public function, and can be used by the user to perform the
    MultiCopy operation directly from a terminal or the FreeCAD application's
    Python console.

    Parameters
    ----------
    paste_code: (str)
            The paste code commands string.
            For indentations, use \'\\t\'.
            For line breaks, use \'\\n\'.
    copy_type: (str) | (int) | (bool)
            [Optional]
            The copy operation mode.
            Values: 'Standard', 'Simple' |
                    1, 2 | True False
            Default: 'Standard' | 1 | True
    delete_selection: (bool)
            [Optional]
            If true, the selected objects are deleted
            after the MultiCopy operation.
            Default: False
    paste_document_label: (str) | (FreeCAD.Document)
            [Optional]
            The name of the document to paste to, or
            the document object itself.
            Default: FreeCAD.ActiveDocument

    Return
    ----------
    (None)
    """
    global doc
    doc = app.activeDocument()
    paste_document_label = paste_document_label or doc
    # Run a few parameters validation tests
    if len(gui.Selection.getSelection()) == 0:
        app.Console.PrintError(
            "\n" + "No FreeCAD objects have been selected for MultiCopy!" + "\n"
        )
        return
    if (
        not isinstance(copy_type, bool)
        and not copy_type in [1, 2]
        and not isinstance(copy_type, str)
    ):
        app.Console.PrintError(
            "\n" + "The copy_type value of '" + str(copy_type) + "' is invalid." + "\n"
        )
        return
    if isinstance(copy_type, str) and (
        copy_type.lower() != "standard" or copy_type.lower() != "simple"
    ):
        app.Console.PrintError(
            "\n" + "The copy_type value of '" + str(copy_type) + "' is invalid." + "\n"
        )
        return
    if not isinstance(delete_selection, bool) and not isinstance(delete_selection, int):
        app.Console.PrintError(
            "\n" + "The delete_selection value must be a boolean value." + "\n"
        )
        return
    if not isinstance(paste_code, str):
        app.Console.PrintError("\n" + "The paste_code value must be a string." + "\n")
        return
    if isinstance(paste_document_label, str):
        dummyVar = False
        docList = GetDocumentsList()
        for elem in docList:
            if app.getDocument(elem).Label == paste_document_label:
                paste_document = app.getDocument(elem)
                dummyVar = True
                break
        if not dummyVar:
            app.Console.PrintError(
                "\n"
                + "The paste_document_label value is not a FreeCAD.Document."
                + "\n"
            )
            return
    else:
        try:
            dummyVar = paste_document_label.Label
            paste_document = paste_document_label
        except Exception:
            app.Console.PrintError(
                "\n" + "The input paste_document does not exist." + "\n"
            )
            return
    del dummyVar
    # Run the Paste Code validation test
    if not Validate(paste_code):
        app.Console.PrintError(
            "\n" + "The input Paste Code Commands are invalid!" + "\n"
        )
        return
    # Modify the 'copy_type' variable
    if isinstance(copy_type, str):
        copy_type = 1 if copy_type.lower() == "standard" else 2
    elif isinstance(copy_type, bool):
        copy_type = 1 if copy_type else 2
    # Begin the MultiCopy operation
    result = __RunPasteCode(
        gui.Selection.getSelection(),
        paste_code,
        paste_document,
        doc,
        copy_type,
        delete_selection,
    )
    if result[0]:
        app.Console.PrintMessage(
            "\n" + "MultiCopy operation has been completed successfully!" + "\n"
        )
    else:
        app.Console.PrintError("\n" + result[1] + "\n")
