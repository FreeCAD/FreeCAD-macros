# FreeCAD-macros

A repository of peer-reviewed FreeCAD macros.

To submit a macro, fork this repository, follow the instructions below, push to your repository, write a pull request, and get thanked.

Please add the following metadata in your macro. Please also add a more complete description how to use the macro near the top of your macro as normal Python comments. Please follow the `CamelCase.FCMacro` convention for the macro name (other associated files except the macro icon don't need to follow this convention). Please don't start your macro name with `Macro` or `FC` or similar, we already know it's a macro for FreeCAD. Also, if possible, start the macro name with the type of object it's working on, e.g. use `ViewRotation` instead of `RotateView`, so that all macros related to `View` will be together when sorting alphabetically.

Macro metadata:
```python
__Name__ = ''
__Comment__ = ''
__Author__ = ''
__Version__ = ''
__Date__ = ''
__License__ = ''
__Web__ = ''
__Wiki__ = ''
__Icon__ = ''
__Help__ = ''
__Status__ = ''
__Requires__ = ''
__Communication__ = ''
__Files__ = ''
```

Explanation of metadata:
```python
__Name__ = 'Name of the macro (generally, file name without extension with spaces)'
__Comment__ = 'Short one-line comment'
__Author__ = 'comma-separated list of authors'
__Version__ = 'major.minor.patch'
__Date__ = 'YYYY-MM-DD'
__License__ = 'License identifier from https://spdx.org/licenses/, e.g. LGPL-3.0-or-later, MIT, CC0-1.0'
__Web__ = 'Associated web page'
__Wiki__ = 'Associated wiki page'
__Icon__ = 'MyMacro.svg, please put an svg file along side the macro, respecting the macro filename'
__Help__ = 'A short explanation how to use the macro, e.g. what to select before launching'
__Status__ = 'Stable|Alpha|Beta'
__Requires__ = 'e.g. FreeCAD >= v0.17'
__Communication__ = 'e.g. https://github.com/FreeCAD/FreeCAD-macros/issues/ if on the github'
__Files__ = 'comma-separated list of files that should be installed together with this file, use paths relative to this file, do not include this file'
```
