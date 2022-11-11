# Macro Cadbase Library
{{Macro
|Name=CadbaseLibrary
|Icon=CadbaseLibrary.svg
|Description=This CadbaseLibrary macro to use components (parts) from CADBase in FreeCAD.
|Author=mnnxp
|Version=0.1.2
|Date=2022-11-11
|FCVersion=0.19
}}

## Description

The macro is designed to load and use components (parts) from CADBase* in the FreeCAD.

For a component modification, sets of files for various CAD systems are loaded. Thus, only FreeCAD set files are downloaded, without downloading documentation and other information on the component.

*CADBase is a platform for publishing and sharing information about 3D components, drawings and manufacturers.

## Usage

If access token expired, then need in the **CADBase library** window, in the **Options** tab, click the **Settings** button, in the **CADBase Library Configuration** window that opens, you need to set the **username**/**password** to gain access to CADBase and wait for a new token to be received after pressing the **OK** button.

Add target components to bookmarks (favorites) on the CADBase site. In FreeCAD will only display components that the user has bookmarked on CADBase, as well as those that have been previously downloaded.

Clicking **Update from CADBase** only updates the list of components from bookmarks active user, without downloading component modifications and files.
Double-clicking on a components folder to get a list of modifications for component.

Getting files of a fileset for FreeCAD occurs after double-clicking on a modification folder.

## Install

In menu Tools select Addon Manager Select the Macros tab find CADBaseLibrary in the list and click Install.

In menu Tools select **Addon Manager**, select the **Macros** tab find **CADBaseLibrary** in the list and click Install.

After it is installed on the above location, it will be available in the macros menu.

Open **Macro** in the ToolBar, select **Macros...**, choose the `CadbaseLibrary.FCMacro` macro and execute.

On first run, the macro will ask you for the location of your library. This location can be changed in the macro settings in the field **Library path**.

Create an account on the platform [CADBase](https://cadbase.rs/#/register) for yourself (skip if you already have a CADBase account).

In the **CADBase library** window, in the **Options** tab, click the **Settings** button, in the **CADBase library configuration** window that opens, you need to set the **username** and **password** to gain access to CADBase. Wait for the token to be received after pressing the **OK** button.

## Info

In FreeCAD, you can find which is your user **modules folder** by entering or pasting `App.getUserAppDataDir()+"Mod"` and your usr **macros folder** by entering `App.getUserMacroDir()` in the Python console (found under menu View->Panels)

Please don't use `cadbase_response_file_2018` as the name of files or folders in the CADBase library folder.

## Link

[Forum thread](https://forum.freecadweb.org/viewtopic.php?f=22&t=69389)

## Version

v0.1.0 2022-06-13    * first release
v0.1.1 2022-10-15    * bugs fixed and code optimization
v0.1.2 2022-11-11    * Changed URLs for `Wiki` and `Web`, code split into files, updated interface: added descriptions for settings
