#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2022 - Wanderer Fan <wandererfan@gmail.com>             *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************
"""Migrates drawings made in FreeCAD v0.18 to v0.19."""

__title__ = "fixRotation"
__author__ = "WandeererFan"
__url__ = "http://www.freecadweb.org/index.html"
__version__ = "00.01"
__date__ = "2022/02/26"

# convert v0.18 Rotation values to v0.19 

import TechDraw

def fixRotation():
    increment = App.Units.Degree
    increment.Value = 270
    for obj in FreeCAD.ActiveDocument.Objects:
        if obj.isDerivedFrom("TechDraw::DrawViewSection"):
            if obj.Rotation != 0.0:
                obj.Rotation = obj.Rotation + increment
                obj.touch()
            for inObj in obj.InList:
                if obj.isDerivedFrom("TechDraw::DrawViewDimension"):
                    inObj.touch()
        elif obj.isDerivedFrom("TechDraw::DrawViewPart"):
            if obj.Rotation != 0.0:
                obj.Rotation = -obj.Rotation
                obj.touch()


if __name__ == '__main__':
    fixRotation()
    FreeCAD.ActiveDocument.recompute()

