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


"""This is the MultiCopy package documentation.

NAME
--------------------
MultiCopy

VERSION
--------------------
v2.0.0

DESCRIPTION
--------------------
'MultiCopy' is a user-created macro to be used within the FreeCAD application. 
MultiCopy allows the duplication (copy and paste) of multiple FreeCAD objects 
that can be labelled sequentially and in a custom manner.

Key features include:
 > Two input methods: by mouse, or by keyboard (Paste Code Commands)
 > Standard Copy and Simple Copy methods supported
 > Duplication across two different documents
 > Delete selected objects after duplication
 > Duplicate with or without dependencies
 > Add custom label separators
 > Add padded numbering to labels
 > Numbering types: Ordinary numerals, upper/lower-case roman numerals and 
   upper/lower-case alphabetic characters
 > Unique 'Paste Code Commands' that allow multiple duplication procedurally 
   as well as in nested loops
 > Both CUI and GUI methods available

For more details, visit:
https://github.com/melwyncarlo/MultiCopy
https://wiki.freecadweb.org/Macro_MultiCopy

PACKAGE CONTENTS
--------------------
MultiCopyCore.py
MultiCopyGui.py
"""


__Title__='MultiCopy'
__Author__='Melwyncarlo'
__Version__='2.0.0'
__Date__='2021-03-23'
__Comment__='MultiCopy allows the duplication (copy and paste) of multiple FreeCAD objects that can be labelled sequentially and in a custom manner.'
__Web__='https://github.com/melwyncarlo/MultiCopy'
__Wiki__='http://www.freecadweb.org/wiki/index.php?title=Macro_MultiCopy'
__Help__='Select one or more FreeCAD objects, then click on the MultiCopy button/macro, and follow the instructions in the dialog box.'
__Status__='stable'
__Requires__='Freecad >= v0.17'
__Communication__='https://github.com/melwyncarlo/MultiCopy/issues'
__Files__='MultiCopyGui.py, MultiCopyCore.py, MultiCopyAuxFunc.py, resources/MultiCopy_Main_Dialog.ui, resources/MultiCopy_Commands_Dialog.ui, resources/MultiCopy.svg'


# Library Imports
# ------------------------------------------------------------------------------------------------

from . import MultiCopyGui as Gui
from . import MultiCopyCore as Core


# Alias Functions
# ------------------------------------------------------------------------------------------------

Run = Core.Run
Launch = Gui.Launch
