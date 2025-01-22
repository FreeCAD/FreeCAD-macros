# Objects To Python
Exports existing objects from a FreeCAD project to a python script

This macro should create clean, human readable python code from already existing FreeCAD objects.
When the generated code is executed, it should create all objects from scratch.

ATTENTION: It does not work for all objects in FreeCAD. Especially objects created by built in python scripts like everything in the Draft workbench will not work correctly.

## How it works
The macro is quite simple. It loops through the properties of all selected objects, compares then to a default object, and generates script lines for object creation and changed properties. For some objects (Sketcher or Spreadsheet objects), special handling in the macro is needed. It may not be complete.

## Usage
This macro generates python code from all selected objects in a FreeCAD project.
If no object is selected, all objects in the project will be selected.

A dialog will open and the output will be written into it. Press CTRL-a and CTRL-c to copy the code.

