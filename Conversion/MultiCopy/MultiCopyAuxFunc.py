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

from PySide import QtCore, QtGui
import math, string


# Constant Variables
# ------------------------------------------------------------------------------------------------

# It is a random string, to be used as a placeholder while changing certain variables
# and then testing against it to determine if the variable has indeed changed.
RANDOM_STRING = '✍✉☏⌨'
# Reference :  https://pypi.org/project/roman/
ROMAN_NUMERAL_MAP = (
    ('M', 1000),
    ('CM', 900),
    ('D', 500),
    ('CD', 400),
    ('C', 100),
    ('XC', 90),
    ('L', 50),
    ('XL', 40),
    ('X', 10),
    ('IX', 9),
    ('V', 5),
    ('IV', 4),
    ('I', 1),
)
# Alphabetic characters string list
# The first element is a dummy string
ALPHA_MAP = [RANDOM_STRING] + list(string.ascii_lowercase)


# Public (User) Functions
# ------------------------------------------------------------------------------------------------

# Reference :  https://pypi.org/project/roman/
def IntToRoman(n):
    """Convert an integer to its upper-case roman numeral variant.

    Parameters
    ----------
    n: (int)
            An arbitrary integer value.

    Return
    ----------
    (str): The converted roman numerical string.

    Example
    ----------
    >>> IntToRoman(1)
    'I'
    >>> IntToRoman(8)
    'VIII'
    >>> IntToRoman(100)
    'C'
    """
    result = ''
    try:
        for numeral, integer in ROMAN_NUMERAL_MAP:
            while n >= integer:
                result += numeral
                n -= integer
    except Exception:
        result = ''
    return result


# Reference :  https://pypi.org/project/roman/
def RomanToInt(inputStr):
    """Convert an upper-case roman numeral string to its integer variant.

    Parameters
    ----------
    inputStr: (str)
            An arbitrary roman numeral.

    Return
    ----------
    (int): The converted integer number.

    Example
    ----------
    >>> RomanToInt('III')
    3
    >>> RomanToInt('IX')
    9
    """
    result = 0
    index = 0
    try:
        for numeral, integer in ROMAN_NUMERAL_MAP:
            while inputStr[index : index + len(numeral)] == numeral:
                result += integer
                index += len(numeral)
    except Exception:
        result = 0
    return result


def IntToAlpha(n):
    """Convert an integer to its lower-case alphabetic string variant.

    Parameters
    ----------
    n: (int)
            An arbitrary integer value.

    Return
    ----------
    (str): The converted alphabetic string.

    Example
    ----------
    >>> IntToAlpha(5)
    'e'
    >>> IntToAlpha(26)
    'z'
    >>> IntToAlpha(52)
    'az'
    """
    result = ''
    try:
        if 1 <= n <= 26:
            result = ALPHA_MAP[n]
        elif 27 <= n <= 702:
            result = (
                ALPHA_MAP[math.ceil((n - 26) / 26)]
                + ALPHA_MAP[n - (26 * math.ceil((n - 26) / 26))]
            )
        elif 703 <= n <= 18278:
            tempVar1 = math.ceil((n - 702) / 26) % 26
            tempVar2 = math.ceil(n - 702) % 26
            tempVar1 = 26 if tempVar1 == 0 else tempVar1
            tempVar2 = 26 if tempVar2 == 0 else tempVar2
            result = (
                ALPHA_MAP[math.ceil((n - 702) / 676)]
                + ALPHA_MAP[tempVar1]
                + ALPHA_MAP[tempVar2]
            )
        else:
            raise Exception('Input value too large')
    except Exception:
        result = ''
    return result


def AlphaToInt(inputStr):
    """Convert a lower-case alphabetic string to its integer variant.

    Parameters
    ----------
    inputStr: (str)
            An arbitrary alphabetic string.

    Return
    ----------
    (int): The converted integer number.

    Example
    ----------
    >>> AlphaToInt('a')
    1
    >>> AlphaToInt('aa')
    27
    >>> AlphaToInt('zz')
    702
    """
    result = 0
    try:
        if len(inputStr) == 1:
            result = ALPHA_MAP.index(inputStr)
        elif len(inputStr) == 2:
            result = (26 * ALPHA_MAP.index(inputStr[0])) + ALPHA_MAP.index(inputStr[1])
        elif len(inputStr) == 3:
            result = (
                (676 * ALPHA_MAP.index(inputStr[1]))
                + (26 * ALPHA_MAP.index(inputStr[1]))
                + ALPHA_MAP.index(inputStr[2])
            )
        else:
            raise Exception('Input value too large')
    except Exception:
        result = 0
    return result


# Numbering Types Function - Ordinary Numerals
def OrdinaryNumerals(start, end):
    """Create a string list of ordinary numerals (numbers).

    Parameters
    ----------
    start: (int)
            Start count variable.
    end: (int)
            End count variable.

    Return
    ----------
    ([str, ...]): The converted ordinary numerals list.

    Example
    ----------
    >>> OrdinaryNumerals(5,10)
    ['5', '6', '7', '8', '9', '10']
    """
    tempList = []
    for i in range(start, end + 1):
        tempList.append(str(i))
    return tempList


# Numbering Types Function - Upper-case Roman Numerals
def UpperCaseRomanNumerals(start, end):
    """Create a string list of upper case roman numerals.

    Parameters
    ----------
    start: (int)
            Start count variable.
    end: (int)
            End count variable.

    Return
    ----------
    ([str, ...]): The converted upper case roman numerals list.

    Example
    ----------
    >>> UpperCaseRomanNumerals(1,3)
    ['I', 'II', 'III']
    """
    tempList = []
    for i in range(start, end + 1):
        tempList.append(IntToRoman(i))
    return tempList


# Numbering Types Function - Lower-case Roman Numerals
def LowerCaseRomanNumerals(start, end):
    """Create a string list of lower case roman numerals.

    Parameters
    ----------
    start: (int)
            Start count variable.
    end: (int)
            End count variable.

    Return
    ----------
    ([str, ...]): The converted lower case roman numerals list.

    Example
    ----------
    >>> LowerCaseRomanNumerals(1,3)
    ['i', 'ii', 'iii']
    """
    tempList = []
    for i in range(start, end + 1):
        tempList.append(IntToRoman(i).lower())
    return tempList


# Numbering Types Function - Upper-case Alphabet
def UpperCaseAlphabet(start, end):
    """Create a string list of upper case alphabetic characters.

    Parameters
    ----------
    start: (int)
            Start count variable.
    end: (int)
            End count variable.

    Return
    ----------
    ([str, ...]): The converted upper case alphabetic characters list.

    Example
    ----------
    >>> UpperCaseAlphabet(1,5)
    ['A', 'B', 'C', 'D', 'E']
    """
    tempList = []
    for i in range(start, end + 1):
        tempList.append(IntToAlpha(i).upper())
    return tempList


# Numbering Types Function - Lower-case Alphabet
def LowerCaseAlphabet(start, end):
    """Create a string list of lower case alphabetic characters.

    Parameters
    ----------
    start: (int)
            Start count variable.
    end: (int)
            End count variable.

    Return
    ----------
    ([str, ...]): The converted lower case alphabetic characters list.

    Example
    ----------
    >>> LowerCaseAlphabet(22,26)
    ['v', 'w', 'x', 'y', 'z']
    """
    tempList = []
    for i in range(start, end + 1):
        tempList.append(IntToAlpha(i))
    return tempList


def setAlertBox(message, error=False, neither=False):
    """Set error and warning pop-up messages.

    Parameters
    ----------
    message: (str)
            The string-based message to be displayed.
    error: (bool)
            'True' opens up the 'Critical' message box, and
            'False' opens up the 'Warning' message box.
    neither: (bool)
            'True' opens up the 'Information' message box, and
            'False' relies on the 'error' variable.
    Return
    ----------
    (None)
    """
    if neither:
        messagebox = QtGui.QMessageBox(
            QtGui.QMessageBox.Information, 'MultiCopy - Info. Message', message
        )
    else:
        if error:
            messagebox = QtGui.QMessageBox(
                QtGui.QMessageBox.Critical, 'MultiCopy - Error Message', message
            )
        else:
            messagebox = QtGui.QMessageBox(
                QtGui.QMessageBox.Warning, 'MultiCopy - Warning Message', message
            )
    messagebox.setWindowModality(QtCore.Qt.ApplicationModal)
    messagebox.exec_()
