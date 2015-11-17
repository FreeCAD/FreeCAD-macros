# FreeCAD-macros
A repository for the FreeCAD macros from http://www.freecadweb.org/wiki/index.php?title=Macros_recipes


Part Design - repair sketch references macros
----------------------------------------------

Macros for repairing Part Design Features after a part update.
Contains many bugs! 
Only supports the repair of the following features

* sketches:  geometry and support references
* linearPattern: direction reference


Requires the pyside and numpy python libraries.
On a Linux Debian based system such as Ubuntu, installation can be done through BASH as follows


```bash
$ sudo apt-get install git python-numpy python-pyside
$ cd ~/.FreeCAD/
$ git clone https://github.com/hamish2014/FreeCAD-macros.git
$ ln -s FreeCAD-macros/PartDesign/*.py ./
```

Once installed, use git to upgrade to the latest version through BASH as follows
```bash
$ cd ~/.FreeCAD/FreeCAD-macros
$ git pull
$ cd ~/.FreeCAD
$ rm *.pyc
```