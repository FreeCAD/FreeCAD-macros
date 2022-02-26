#![alt text](LasercutterTechdrawExport.svg "Logo") FreeCAD Lasercutter SVG Export Macro

We have a lasercutter that uses .svg files as input.  
I would like to generate .svg files from my FreeCAD designs.  
The laser beam width has to be considered, but I do not want to add it in my design.  

I have created a script that is doing this task:

* Select several parts in the FreeCAD design
* Create 3D outline objects from all selected items
* Rotate them into the XY-plane
* Create views in a TechDraw page
* Arrange the views to fit in the page with minimal gaps

![alt text](LasercutterSVGExport_screenshot.png "Screenshot")

## Installation
In FreeCAD, select the Addon manager from tools menu. Go to the Macros tab and find LasercutterSVGExport in the list. Click Install.  

or  
Copy LasercutterSVGExport.FCMacro and the LasercutterSVGExport folder to your FreeCAD Macro directory (on Linux: ~/.FreeCAD/Macro)  
In menu Macro select Macros...  
Execute LasercutterSVGExport.FCMacro 

## Usage
Do not add the laserbeam width into your design. This export tool will add the beam width.

* Select several parts in the FreeCAD design
* Creates outline objects from all selected items
* Rotate them into the XY-plane
* Create views in a TechDraw page
* Arrange the views to fit in the page with minimal gaps

The tool creates a folder LaserCutterExportObjects that contains an object for each selected part.  
There are some parameters which can be changed:
* Part: Selected part
* Beam Width: The width of the laser beam in mm
* Normal: A vector perpendicular to the object
* Method: How to create the outline 
    *auto*: find the best method automatically 
    *2D*: works for 2D objects
    *3D*: create a 3D outline and then get the biggest face
    *face*: find the biggest face and create a 2D offset
    *normal*: manually define parameter Normal and use it as a perpendicular vector to the object
    
#### Troubleshooting
Find your part in the folder LaserCutterExportObjects and play with the parameters.  

*Got the wrong side of your part:*  
Set method to normal and change the parameter Normal to be perpendicular to the wanted side
  
*Missing lines or no view at all in Techdraw:*  
Change the parameter method. Try out different settings.

## Discussion
[Dedicated FreeCAD forum discussion thread](https://forum.freecadweb.org/viewtopic.php?f=35&t=31869)

## License
GNU Lesser General Public License v3.0


