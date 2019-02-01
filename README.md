# FreeCAD-macros

A repository of peer-reviewed FreeCAD macros.

This repository hosts FreeCAD macros that volunteers have vetted and added for use to the whole community in general available through the [FreeCAD Addon Manager](https://www.freecadweb.org/wiki/AddonManager).

## How to submit a macro

- The most ideal way to submit a macro is to post it to the [FreeCAD Python Scripting and Macros subforum](https://forum.freecadweb.org/viewforum.php?f=22) for review. After a green light is given then:  

- Fork this repository
- Clone your fork locally `git clone https://github.com/your-gh-username/FreeCAD-addons`
- Setup the upstream `git remote add upstream https://github.com/FreeCAD/FreeCAD-addons`
- Create a branch to work in `git checkout -b your_branch`
- Follow our [guidelines](https://github.com/FreeCAD/FreeCAD-addons/README.md#guidelines-for-submitting-a-macro) below on how to add a macro
- When you're ready to push your changes: `git push -u origin your_branch`
- Create a PR (pull request) against upstream
- Achieve global fame once PR is merged

## Guidelines for submitting a macro
1. Please add a complete description how to use the macro near the top of your macro as normal Python comments.
2. Please follow the `CamelCase.FCMacro` convention for the macro name (other associated files except the macro icon don't need to follow this convention). Please don't start your macro name with `Macro` or `FC` or similar (we already know it's a macro for FreeCAD).
3. Also, if possible, start the macro name with the type of object it's working on, e.g. use `ViewRotation` instead of `RotateView`, so that all macros related to `View` will be together when sorting alphabetically.
4. Please add the following metadata in your macro after step 1.
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
    __License__ = 'License identifier from https://spdx.org/licenses/, e.g. LGPL-2.0-or-later as FreeCAD, MIT, CC0-1.0'
    __Web__ = 'Associated web page'
    __Wiki__ = 'Associated wiki page'
    __Icon__ = 'MyMacro.svg, please put an svg file along side the macro, respecting the macro filename'
    __Help__ = 'A short explanation how to use the macro, e.g. what to select before launching'
    __Status__ = 'Stable|Alpha|Beta'
    __Requires__ = 'e.g. FreeCAD >= v0.17'
    __Communication__ = 'e.g. https://github.com/FreeCAD/FreeCAD-macros/issues/ if on the github'
    __Files__ = 'comma-separated list of files that should be installed together with this file, use paths relative to this file, do not include this file'
    ```
