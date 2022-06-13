# Macro Cadbase Library
{{Macro
|Name=CadbaseLibrary
|Icon=CadbaseLibrary.svg
|Description=This CadbaseLibrary macro to use components (parts) from CADBase in FreeCAD.
|Author=mnnxp
|Version=0.1
|Date=2022-06-13
|FCVersion=0.19
}}

## Description

The macro is designed to load and use components (parts) from CADBase* in the FreeCAD.

For a component modification, sets of files for various CAD systems are loaded. Thus, only FreeCAD set files are downloaded, without downloading documentation and other information on the component.

*CADBase is a platform for publishing and sharing information about 3D components, drawings and manufacturers.

## Usage

If access token expired, then need in the **CADBase library** window, in the **Options** tab, click the **Config** button, in the **CADBase library configuration** window that opens, you need to set the **username**/**password** to gain access to CADBase and wait for a new token to be received after pressing the **OK** button.

Add target components to bookmarks (favorites) on the CADBase site. In FreeCAD will only display components that the user has bookmarked on CADBase, as well as those that have been previously downloaded.

Clicking **Update from CADBase** only updates the list of components from bookmarks active user, without downloading component modifications and files.
Double-clicking on a component's folder pull component's modifications.

Getting files of a fileset for FreeCAD occurs after double-clicking on the modification folder.
Double-clicking

## Install

Install through Addon manager.

This script is made to be used as a FreeCAD macro, and to be placed inside your macros folder (default is $HOME/.FreeCAD on mac/linux, C:/Users/youruser/Application Data/FreeCAD on windows).

After it is installed through Addon manager on the above location, it will be available in the macros menu. On first run, it will ask you for the location of your library.

Next steps (skip first step if you already have a CADBase account):
1. Create an account on the platform [CADBase](https://cadbase.rs/#/register) for yourself
2. In FreeCAD, select the **Macro** tab, click **Macros...** and select the `CadbaseLibrary.FCMacro` macro, then you will be prompted to select the module folder (where the files from the CADBase store will be loaded)
* In FreeCAD, find which is your user **modules folder** by entering or pasting `App.getUserAppDataDir()+"Mod"` and your usr **macros folder** by entering `App.getUserMacroDir()` in the Python console (found under menu View->Panels)
3. In the **CADBase library** window, in the **Options** tab, click the **Config** button, in the **CADBase library configuration** window that opens, you need to set the **username** and **password** to gain access to CADBase. Wait for the token to be received after pressing the **OK** button.

**Note**: Please DO NOT use accented characters in your file names, thanks!!!


## Link

[Forum thread](https://forum.freecadweb.org/viewtopic.php?f=22&t=69389)

## Version

v0.1 2022-06-13    * first release
