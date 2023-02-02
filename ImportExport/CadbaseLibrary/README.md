# Macro Cadbase Library
{{Macro
|Name=CadbaseLibrary
|Icon=CadbaseLibrary.svg
|Description=This CadbaseLibrary macro to use components (parts) from CADBase in FreeCAD.
|Author=mnnxp
|Version=0.2.0
|Date=2023-02-02
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

Create an account on the platform [CADBase](https://cadbase.rs) for yourself (skip if you already have a CADBase account).

In the **CADBase library** window, in the **Options** tab, click the **Settings** button, in the **CADBase library configuration** window that opens, you need to set the **username** and **password** to gain access to CADBase. Wait for the token to be received after pressing the **OK** button.

#### Instalation Blake3

To use this macro to update files already in the CADBase storage, Blake3 must be installed.

```sh
  # Install on Unix/macOS
  python3 -m pip install "blake3"
  # Install on Windows
  py -m pip install "blake3"
```

## Info

In FreeCAD, you can find which is your user **modules folder** by entering or pasting `App.getUserAppDataDir()+"Mod"` and your usr **macros folder** by entering `App.getUserMacroDir()` in the Python console (found under menu View->Panels)

If you need to save logs to a file (for example, for debugging, studying, or other purposes), you need to create a `cadbase_file_2018.log` file in the local library folder.

Please don't use `cadbase_file_2018` and `cadbase_file_2018.log` as file or folder names in the CADBase library folder. These files store server responses and logs, if you use these filenames for your data, you may lose them.

To avoid losing local data when downloading from CADBase storage, files already in local storage are skipped when downloading from the cloud.

Before uploading files to the cloud (CADBase storage), the macro checks for existing files on the cloud and excludes files from an upload list if their local and cloud hashes are the same. A hash is calculated using the Blake3 library.

This check is skipped and previously downloaded files (whe already in the cloud) are not updated if the Blake3 library is not installed.

## Link

[Forum thread](https://forum.freecadweb.org/viewtopic.php?f=22&t=69389)

## Version

v0.1.0 2022-06-13    * first release

v0.1.1 2022-10-15    * bugs fixed and code optimization

v0.1.2 2022-11-11    * Changed URLs for `Wiki` and `Web`, code split into files, updated interface: added descriptions for settings

v0.1.3 2022-11-13    * Bugs fixed. Added check to skip a file if it already exists in local storage.

v0.2.0 2023-02-02    * Added the ability to upload files to the CADBase storage. Added comparing local and cloud-stored files using Blake3 hash.
