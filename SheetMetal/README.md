# SheetMetal StitchCut Macro

The SheetMetalStitchCut macro creates evenly spaced stitch cuts along a selected line in a sketch,
primarily for sheet metal flat patterns to allow easier hand folding.

## Features
- Start & end offset from edges
- Automatic cut length calculation
- User-defined number of cuts
- Optional cut width (0 = single line, >0 = slot)
- Inserts cuts directly into the active sketch
- Persistent settings between runs
- Undo support (transaction based)
- PySide2 / PySide6 compatibility

## Usage
1. Enter **edit mode** on a sketch.
2. Select the line to apply stitch cuts to.
3. Run the macro.
4. Enter:
   - Start & End Offset
   - Gap between cuts
   - Number of cuts
   - **Cut Width**
     - `0` → single cut line
     - `>0` → rectangular slot of specified width
5. The original line is replaced with stitch cuts.

## Author
John Hyslop

## FreeCAD Version
Tested on FreeCAD 1.0.2 and later.

## License
Free for personal, educational, and commercial use.
Please credit the author by including this README in your project or linking to the repository.

## Changelog

### Version 1.2 (March 2026)
- Added PySide6 compatibility (works with modern FreeCAD builds)
- Improved geometry validation and error handling
- Added zero-length line protection
- Improved transaction handling with abort on failure
- Added sensible input ranges and decimal precision controls
- General stability improvements

### Version 1.1 (February 2026)
- Now uses FreeCAD’s Persistent Configuration System
- Cut Widths can now be applied
- Updated description and clarity improvements
- Renamed macro to SheetMetalStitchCut.FCMacro for FreeCAD macro list organization
- Fixed UI improvements: Replaced `QLineEdit` with `QSpinBox` and `QDoubleSpinBox`
- Added Open Transaction for Undo functionality

### Version 1.0 (March 2025)
- Initial release

## Last Updated
March 2026
