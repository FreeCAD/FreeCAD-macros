# see http://www.freecadweb.org/wiki/Macro_unrollRuledSurface
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2013 - DoNovae/Herve BAILLY <hbl13@donovae.com>           *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************
 
#####################################
# Macro UnrollRuledSurface
#     Unroll of a ruled surface
#####################################
import FreeCAD , FreeCADGui , Part, Draft, math, Drawing , PySide, os
from PySide import QtGui,QtCore
from FreeCAD import Base
from unrollRuledSurface.unfoldBox import unfoldBoxClass
fields_l = [] 
unroll_l = [] 
 
 
#####################################
#####################################
# Functions 
#####################################
#####################################
 
#####################################
# Function errorDialog 
#####################################
def errorDialog(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,u"Error Message",msg )
    diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()
 

#####################################
# Function proceed 
#####################################
def proceed():
   QtGui.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
 
   FreeCAD.Console.PrintMessage("===========================================\n")
   FreeCAD.Console.PrintMessage("UnrollRuledSurface: start.\n")
   try:
      file_name  = fields_l[0].text()
      pts_nbr    = float(fields_l[1].text())
      scale    = float(fields_l[2].text())
      scale_auto = scale_check.isChecked()
      edge0 = edge0_check.isChecked()
      a3 = a3_check.isChecked()
      cartridge = cartridge_check.isChecked()
      onedrawing = onedrawing_check.isChecked()
      FreeCAD.Console.PrintMessage("UnrollRuledSurface.file_name: "+file_name+"\n")
      FreeCAD.Console.PrintMessage("UnrollRuledSurface.pts_nbr: "+str(pts_nbr)+"\n")
      FreeCAD.Console.PrintMessage("UnrollRuledSurface.scale: "+str(scale)+"\n")
      FreeCAD.Console.PrintMessage("UnrollRuledSurface.scale_check: "+str(scale_auto)+"\n")
      FreeCAD.Console.PrintMessage("UnrollRuledSurface.edge0_check: "+str(edge0)+"")
      FreeCAD.Console.PrintMessage("UnrollRuledSurface.a3_check: "+str(a3)+"\n")
      FreeCAD.Console.PrintMessage("UnrollRuledSurface.cartridge: "+str(cartridge)+"\n")
      FreeCAD.Console.PrintMessage("UnrollRuledSurface.onedrawing: "+str(onedrawing)+"\n")
   except:
      msg="UnrollRuledSurface: wrong inputs...\n"
      FreeCAD.Console.PrintError(msg)
      errorDialog(msg)
 
   QtGui.qApp.restoreOverrideCursor()
   DialogBox.hide()
   unrollRS=unrollRuledSurface( file_name , pts_nbr , edge0 )
   #
   # Get selection
   #
   sel=FreeCADGui.Selection.getSelection()
   faceid=0
   objnames_l=[]
   objnames0_l=[]
   grp=FreeCAD.activeDocument().addObject("App::DocumentObjectGroup", str(file_name)+"_objs") 
   for objid in range( sel.__len__() ):
     shape=sel[objid].Shape
     faces=shape.Faces
     for id in range( faces.__len__() ):
        FreeCAD.Console.PrintMessage("UnrollRuledSurface.proceed: ObjId= "+str(objid)+" , faceId= "+str( faceid )+"\n")
	if faces.__len__() > 1:
	  name=sel[objid].Name+".faces "+str(id)
	else:
	  name=sel[objid].Name
        obj=unrollRS.unroll(faces[id],name) 
        obj.ViewObject.Visibility=False
        grp.addObject(obj)
	objnames_l.append( [ obj , name ] )
	objnames0_l.append( [ sel[objid] , name ] )
        faceid=faceid+1
   id=0
   while objnames_l.__len__() > 0:
     draw=Drawing2d( scale, scale_auto , a3 , cartridge , onedrawing,str(file_name)+"_page"+str(id) ) 
     objnames_l=draw.all( objnames_l )
     id=id+1
     FreeCAD.Console.PrintMessage("UnrollRuledSurface: obj_l= "+str(objnames_l.__len__())+"\n")
 
   FreeCAD.Console.PrintMessage("UnrollRuledSurface: end.\n")
   FreeCAD.Console.PrintMessage("===========================================\n")

#####################################
# Function close 
#####################################
def close():
   DialogBox.hide()

#####################################
# Class unrollRuledSurface 
#     - file_name : output file 
#     - pts_nbr : nbr point of 
#       discretization
#####################################
class unrollRuledSurface:
  def __init__( self, file_name, pts_nbr , edge0 ):
    self.doc = FreeCAD.activeDocument()
    self.file_name = file_name
    self.pts_nbr = int(pts_nbr)
    self.edge0 = edge0
    FreeCAD.Console.PrintMessage("UnrollRuledSurface.unroll - file_name: "+self.file_name+" , pts_nbr: "+str(self.pts_nbr)+"\n")
 

  #####################################
  # Function discretize 
  #####################################
  def discretize(self,curve):
         if type(curve).__name__=='GeomLineSegment':
            sd=curve.discretize( self.pts_nbr )
         elif type(curve).__name__=='GeomBSplineCurve':
            nodes=curve.getPoles()
            spline=Part.BSplineCurve()
            spline.buildFromPoles( nodes )
            sd=spline.discretize( self.pts_nbr )
         elif type(curve).__name__=='GeomCircle':
            sd=curve.discretize( self.pts_nbr )
	 else:
            sd=curve.discretize( self.pts_nbr )
         return sd 

  #####################################
  # Function nbpoles 
  #####################################
  def nbpoles(self,curve):
       if type(curve).__name__=='GeomLineSegment':
         nbpol=1
       elif type(curve).__name__=='GeomBSplineCurve':
         nbpol=curve.NbPoles
       elif type(curve).__name__=='GeomCircle':
         nbpol=2
       elif type(curve).__name__=='GeomBezierCurve':
         nbpol=4
       else:
         nbpol=0
       FreeCAD.Console.PrintMessage("UnrollRulrdSurface.nbpole {:s} = {:d}\n".format(type(curve).__name__,nbpol))
       return nbpol
 
  #####################################
  # Function unroll 
  #####################################
  # Unroll of a face 
  # composed of 2 or 4 edges
  #####################################
  def unroll(self,face,name):
    FreeCAD.Console.PrintMessage("UnrollRuledSurface.unroll: Ege Nbr= "+str( face.Edges.__len__())+"\n")
    if face.Edges.__len__() == 2: 
       e1=face.Edges[0]
       e2=face.Edges[1]
       sd1=e1.Curve.discretize( self.pts_nbr )
       sd2=e2.Curve.discretize( self.pts_nbr )
    elif face.Edges.__len__() == 3:
       e1=face.Edges[0]
       e2=face.Edges[2]
       sd1=e1.Curve.discretize( self.pts_nbr )
       sd2=e2.Curve.discretize( self.pts_nbr )
    else:
       E0=face.Edges[0]
       E1=face.Edges[1]
       E2=face.Edges[2]
       E3=face.Edges[3]
       #
       # Choose more complexe curve as edge
       #
       nbpol0=self.nbpoles(E0.Curve)
       nbpol1=self.nbpoles(E1.Curve)
       nbpol2=self.nbpoles(E2.Curve)
       nbpol3=self.nbpoles(E3.Curve)
       FreeCAD.Console.PrintMessage("UnrollRuledSurface.unroll: nbpol0= {:d}, nbpol1= {:d}, nbpol2= {:d}, nbpol3= {:d}\n".format(nbpol0,nbpol1,nbpol2,nbpol3))
 
       if self.edge0:
         e1=E0
         e2=E2
         v=self.discretize( E1 )
	 v0=v[0]
	 v1=v[self.pts_nbr-1]
       else:
         e1=E1
         e2=E3
         v=self.discretize( E2 )
	 v0=v[0]
	 v1=v[self.pts_nbr-1]
 
       sd1=self.discretize( e1 )
       sd2=self.discretize( e2 )
       #
       # Reverse if curves cross over
       #
       if not ( sd2[0].__eq__( v0 ) or not sd2[0].__eq__( v1 ) ):
          sd2.reverse()
 
    #
    # Create a polygon object and set its nodes 
    #
    devlxy_l=self.devlxyz( sd1 , sd2 )
    FreeCAD.Console.PrintMessage("UnrollRuledSurface.unroll: size devlxy_l: "+str( devlxy_l.__len__())+"\n")
    p=self.doc.addObject("Part::Polygon",name) 
    p.Nodes=devlxy_l
    self.doc.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    return p
 
  #####################################
  # Function vect_copy 
  #   - vect:  
  #   - return copy of vector
  #####################################
  def vect_copy( self, vect):
     v= vect.add( FreeCAD.Base.Vector(0,0,0) )
     return v 
 
  #####################################
  # Function vect_cos 
  #   - vect1,2:  
  #   - return cos angle between 
  #     2 vectors 
  #####################################
  def vect_cos( self , vect1, vect2 ):
     cosalp=vect1.dot(vect2)/vect1.Length/vect2.Length
     return cosalp
 
  #####################################
  # Function vect_sin 
  #   - vect1,2:  
  #   - return abs(sin) angle between 
  #     2 vectors 
  #####################################
  def vect_sin( self , vect1, vect2 ):
     v= FreeCAD.Base.Vector(0,0,0)
     v.x=vect1.y*vect2.z-vect1.z*vect2.y
     v.y=vect1.z*vect2.x-vect1.x*vect2.z
     v.z=vect1.x*vect2.y-vect1.y*vect2.x
     sinalp=v.Length/vect1.Length/vect2.Length
     return sinalp
 
 
  #####################################
  # Function devlxyz 
  #    - vect1,2: 2 edges of the shape
  #    - return dvlxy_l
  #####################################
  # unroll of a face 
  # composed of 4 edges
  #####################################
  def devlxyz( self , vect1 , vect2 ):
    #
    # Init
    #
    if ( vect1.__len__() != vect2.__len__()) or  ( vect1.__len__() != self.pts_nbr ) or ( vect2.__len__() != self.pts_nbr ):
        msg="UnrollRuledSurface.devlxyz: incompatility of sizes vect1 , vect2, pts_nbr- "+str( vect1.__len__())+" , "+str( vect2.__len__())+" , "+str( self.pts_nbr )+"\n"
        FreeCAD.Console.PrintError(msg)
        errorDialog(msg)
 
    devlxy_l=[]
    devl1xy_l=[]
    devl2xy_l=[]
    errormax=0.0
    #
    # Init unroll
    # AB
    #
    a1b1=vect2[0].sub(vect1[0])
    oa1=FreeCAD.Vector(0,0,0)
    devl1xy_l.append( oa1 ) #A1
    ob1=FreeCAD.Vector(a1b1.Length,0,0)
    devl2xy_l.append( ob1 ) #B1
    #self.draw_line( devl1xy_l[0] , devl2xy_l[0] )
    #self.draw_line( vect1[0] , vect2[0] )
    for j in range( 1 , self.pts_nbr ) : 
      #
      # AB
      #
      ab=vect2[j-1].sub(vect1[j-1])
      #self.draw_line( vect1[j-1] , vect2[j-1] )
      #
      # AC
      #
      ac=vect1[j].sub(vect1[j-1])
      #
      # BD
      #
      bd=vect2[j].sub(vect2[j-1])
      #
      # CD 
      #
      cd=vect2[j].sub(vect1[j])
      #
      # A1B1 in unroll plan
      #
      a1b1=devl2xy_l[j-1].sub(devl1xy_l[j-1])
      a1b1n=self.vect_copy(a1b1)
      a1b1n.normalize()
      a1b1on=FreeCAD.Vector(-a1b1n.y,a1b1n.x,0)
      #
      # A1C1
      #
      cosalp=self.vect_cos( ab , ac )
      sinalp=self.vect_sin( ab , ac )
      a1c1=self.vect_copy(a1b1n)
      a1c1.multiply(cosalp*ac.Length)
      v=self.vect_copy(a1b1on)
      v.multiply(sinalp*ac.Length)
      a1c1=a1c1.add(v)
      #FreeCAD.Console.PrintMessage("UnrollRuledSurface.alp a1b1: "+str(a1b1n.getAngle(a1b1on))+"\n")
      #FreeCAD.Console.PrintMessage("UnrollRuledSurface.alp oc1: "+str(a1b1n.getAngle(a1c1)-alp)+"\n")
      #FreeCAD.Console.PrintMessage("UnrollRuledSurface.length oc1: "+str(a1c1.Length-ac.Length)+"\n")
      oa1=self.vect_copy(devl1xy_l[j-1])
      oc1=oa1.add(a1c1)
      devl1xy_l.append(oc1)
      #
      # B1D1
      #
      cosalp=self.vect_cos( ab , bd )
      sinalp=self.vect_sin( ab , bd )
      b1d1=self.vect_copy(a1b1n)
      b1d1.multiply(cosalp*bd.Length)
      v=self.vect_copy(a1b1on)
      v.multiply(sinalp*bd.Length)
      b1d1=b1d1.add(v)
      #FreeCAD.Console.PrintMessage("UnrollRuledSurface.alp od1: "+str(b1a1n.getAngle(b1d1)-alp)+"\n")
      #FreeCAD.Console.PrintMessage("UnrollRuledSurface.length od1: "+str(b1d1.Length-bd.Length)+"\n")
      ob1=self.vect_copy(devl2xy_l[j-1])
      od1=ob1.add(b1d1)
      devl2xy_l.append(od1)
      #
      # Draw generatrice
      #
      #self.draw_line( devl1xy_l[j] , devl2xy_l[j] )
      c1d1=devl2xy_l[j].sub( devl1xy_l[j] )
      if ab.Length <> 0 :
         errormax=max(errormax,math.fabs(ab.Length-c1d1.Length)/ab.Length)
    #
    # The end
    #
    FreeCAD.Console.PrintMessage("UnrollRuledSurface Error cd,c1d1: {:.1f} %\n".format(errormax*100))
 
    #
    # Close polygone
    #
    devlxy_l = devl1xy_l
    devl2xy_l.reverse()
    devlxy_l.extend( devl2xy_l )
    v=FreeCAD.Vector(0,0,0)
    devlxy_l.append( v )
 
    return devlxy_l
 
 
 
  #####################################
  # Function draw_line 
  #   - vect0,1: two points 
  #####################################
  def draw_line( self , vect0 , vect1 ):
     l=Part.Line()
     l.StartPoint=vect0
     l.EndPoint=vect1
     self.doc.addObject("Part::Feature","Line").Shape=l.toShape()
 

#####################################
# Class Drawing2d 
#   -obj_l: listes of object
#   -topxh1
#   -topyh1
#   -topxv1
#   -topyv1
#   -topxvmax1
#   -topyvmax1
#   -topxvmax1
#   -topyvmax1
#####################################
class Drawing2d:
  #####################################
  # Function __init__ 
  #     - Scale
  #     - scale_auto
  #     - a3
  #     - cartridge
  #     - onedrawing
  #####################################
  def __init__( self,  scale , scale_auto , a3 , cartridge , onedrawing , page_str ):
    self.TopX_H=0
    self.TopY_H=0
    self.TopX_V=0
    self.TopY_V=0
    self.TopX_Hmax=0
    self.TopY_Hmax=0
    self.TopX_Vmax=0
    self.TopY_Vmax=0
    self.a3=a3
    self.scale=scale
    self.scale_auto=scale_auto
    self.cartridge=cartridge
    self.onedrawing=onedrawing
    if self.a3:
      self.L=420
      self.H=297
      self.marge=6
    else:
      self.L=297
      self.H=210
      self.marge=6
    self.name=page_str
 
  #####################################
  # Function newPage 
  #####################################
  def newPage( self ):
    freecad_dir=os.getenv('HOME')+"/.FreeCAD/Mod/unrollRuledSurface"
    page = FreeCAD.activeDocument().addObject('Drawing::FeaturePage', self.name )
    if self.a3:
        if self.cartridge:
           page.Template = freecad_dir+'/A3_Landscape.svg'   
        else:
           page.Template = freecad_dir+'/A3_Landscape_Empty.svg'   
    else:
        if self.cartridge:
           page.Template = freecad_dir+'/A4_Landscape.svg'   
        else:
           page.Template = freecad_dir+'/A4_Landscape_Empty.svg'   
    return page
 
 
  #####################################
  # Function all 
  #####################################
  def all( self, objname_l ):
      obj1_l=[]
      for objid in range( objname_l.__len__() ):
        if objid == 0 or not self.onedrawing:
          page = self.newPage()
        obj1_l.extend( self.done( objid , objname_l[objid] ))
      return obj1_l 
 
  #####################################
  # Function all 
  #####################################
  def done( self, id , objname ):
    #
    # Init
    #
    obj_l=[]
    obj=objname[0]
    objname=objname[1]
    xmax=obj.Shape.BoundBox.XMax-obj.Shape.BoundBox.XMin
    ymax=obj.Shape.BoundBox.YMax-obj.Shape.BoundBox.YMin
    if ymax > xmax :
      Draft.rotate( obj , 90 )
    Draft.move( obj , FreeCAD.Base.Vector( -obj.Shape.BoundBox.XMin , -obj.Shape.BoundBox.YMin , 0))
    xmax=obj.Shape.BoundBox.XMax-obj.Shape.BoundBox.XMin
    ymax=obj.Shape.BoundBox.YMax-obj.Shape.BoundBox.YMin
 
    scale=min((self.L-4*self.marge)/xmax,(self.H-4*self.marge)/ymax)
 
    if ( not self.scale_auto ) or ( self.onedrawing ) :
       scale=self.scale
 
    FreeCAD.Console.PrintMessage("UnrollRuledSurface.drawing: scale= {:.2f}\n".format(scale))
 
 
    if id == 0 or not self.onedrawing:
      #
      # Init
      #
      FreeCAD.Console.PrintMessage("Dawing2d: init\n")
      self.TopX_H=self.marge*2
      self.TopY_H=self.marge*2
      TopX=self.TopX_H
      TopY=self.TopY_H
      self.TopX_H=self.TopX_H + xmax * scale + self.marge
      self.TopY_H=self.TopY_H 
      self.TopX_Hmax=max( self.TopX_Hmax , self.TopX_H )
      self.TopY_Hmax=max( self.TopY_Hmax , self.TopY_H + ymax*scale+self.marge )
      self.TopX_Vmax=max( self.TopX_Vmax , self.TopX_Hmax )
      self.TopX_V=max(self.TopX_Vmax,self.TopX_V)
      self.TopY_V=self.marge*2
    elif self.onedrawing:
      if self.TopX_H + xmax * scale < self.L :
        if self.TopY_H + ymax * scale + self.marge*2 < self.H :
	   #
	   # H Add at right on same horizontal line
	   #
           FreeCAD.Console.PrintMessage("Dawing2d: horizontal\n")
           TopX=self.TopX_H
           TopY=self.TopY_H
           self.TopX_H=self.TopX_H + xmax * scale + self.marge
	   self.TopX_Hmax=max( self.TopX_Hmax , self.TopX_H )
	   self.TopY_Hmax=max( self.TopY_Hmax , self.TopY_H + ymax*scale+self.marge )
	   self.TopX_Vmax=max( self.TopX_Hmax , self.TopX_Vmax )
           self.TopX_Vmax=max( self.TopX_Vmax , self.TopX_Hmax  )
           self.TopX_V=max(self.TopX_Vmax,self.TopX_V)
	else:
	   #
	   # V Add at right on same horizontal line
	   #
           FreeCAD.Console.PrintMessage("Dawing2d: vertival\n")
           if self.TopX_V + ymax * scale +2* self.marge < self.L and self.TopY_V + xmax * scale + 2*self.marge < self.H :
             Draft.rotate( obj , 90 )
	     Draft.move( obj , FreeCAD.Base.Vector( -obj.Shape.BoundBox.XMin , -obj.Shape.BoundBox.YMin , 0))
	     x0=xmax;xmax=ymax,ymax=x0
             self.TopX_V=max(self.TopX_Vmax, self.TopX_V)
             TopX=self.TopX_V
             TopY=self.TopY_V
	     self.TopX_V = self.TopX_V + xmax * scale + self.marge
	     self.TopY_Vmax=max( self.TopY_Vmax , self.TopY_V + ymax * scale + self.marge )
	   else:
	     obj_l.append( [ obj , name ] )
	     return obj_l
 
      else:
	#
	# H Carriage return 
	#
        if ( self.TopY_Hmax + ymax * scale + self.marge*2 < self.H ):   
           FreeCAD.Console.PrintMessage("Dawing2d: carriage return: "+str(self.TopY_H + ymax * scale )+" > "+str(self.H)+"\n")
           TopX=self.marge*2
           TopY=self.TopY_Hmax
           self.TopX_H=TopX + xmax * scale + self.marge
           self.TopY_H=TopY 
	   self.TopX_Hmax=max( self.TopX_Hmax , self.TopX_H )
	   self.TopY_Hmax=self.TopY_Hmax + ymax*scale+self.marge
           self.TopX_Vmax=max( self.TopX_Vmax , self.TopX_Hmax )
           self.TopX_V=max(self.TopX_Vmax,self.TopX_V)
	else:
	   #
	   # V Add at right on same horizontal line
	   #
           FreeCAD.Console.PrintMessage("Dawing2d: vertival: "+str(self.TopX_V)+" , "+str(self.TopX_Vmax)+"\n")
           if self.TopX_V + ymax * scale + 2*self.marge < self.L and self.TopY_V + xmax * scale + 2*self.marge < self.H :
             Draft.rotate( obj , 90 )
	     Draft.move( obj , FreeCAD.Base.Vector( -obj.Shape.BoundBox.XMin , -obj.Shape.BoundBox.YMin , 0))
	     x0=xmax;xmax=ymax,ymax=x0
             TopX=self.TopX_V
             TopY=self.TopY_V
	     self.TopX_V = self.TopX_V + xmax * scale + self.marge
	     self.TopY_Vmax=max( self.TopY_Vmax , self.TopY_V + ymax * scale + self.marge )
	   else:
	     obj_l.append( [ obj , objname ] )
	     return obj_l
 
    page=FreeCAD.activeDocument().getObject(self.name )
 
    Text=FreeCAD.activeDocument().addObject('Drawing::FeatureViewAnnotation', objname+"_txt")
    Text.Text=objname
    Text.X=TopX+xmax*scale/2
    Text.Y=TopY+ymax*scale/2
    Text.Scale=2
 
    TopView = FreeCAD.activeDocument().addObject('Drawing::FeatureViewPart',objname)
    TopView.Source = obj
    TopView.Direction = (0.0,0.0,1)
    TopView.Rotation = 0 
    TopView.X = TopX 
    TopView.Y = TopY 
    TopView.ShowHiddenLines = False
    TopView.Scale = scale 
    page.addObject(TopView)
    page.addObject(Text)
    FreeCAD.activeDocument().recompute()
    return obj_l
 
 
 

#####################################
#####################################
# Dialog Box 
#####################################
#####################################
fields = [[ "File Name" , "UnrollSurface" ]]
fields.append(["Dicretization Points Nbr","100" ])
fields.append(["Scale","1" ])
 
DialogBox = QtGui.QDialog()
DialogBox.resize(250,250)
DialogBox.setWindowTitle("UnrollRuledSurface")
la = QtGui.QVBoxLayout(DialogBox)
buttonGrp1 = QtGui.QButtonGroup(DialogBox)
buttonGrp2 = QtGui.QButtonGroup(DialogBox)
 
#
# Input fields
#
for id in range(len( fields )):
  la.addWidget(QtGui.QLabel( fields[ id ][ 0 ] ))
  fields_l.append( QtGui.QLineEdit( fields[ id ][ 1 ] ))
  la.addWidget( fields_l[ id ] )

scale_check = QtGui.QCheckBox( DialogBox )
scale_check.setObjectName("checkBox")
scale_check.setChecked(True)
la.addWidget(QtGui.QLabel("Scale auto"))
la.addWidget(scale_check)
 
line3 = QtGui.QFrame(DialogBox)
line3.setFrameShape(QtGui.QFrame.HLine)
line3.setFrameShadow(QtGui.QFrame.Sunken)
la.addWidget(line3)
 
edge0_check = QtGui.QRadioButton( DialogBox )
la.addWidget(QtGui.QLabel("Generatrices from edge 1 to 4" ))
edge0_check.setChecked(False)
la.addWidget(edge0_check)
edge1_check = QtGui.QRadioButton( DialogBox )
la.addWidget(QtGui.QLabel("Generatrices from edge 0 to 3" ))
edge1_check.setChecked(True)
buttonGrp1.addButton(edge0_check)
buttonGrp1.addButton(edge1_check)
la.addWidget(edge1_check)
 
line4 = QtGui.QFrame(DialogBox)
line4.setFrameShape(QtGui.QFrame.HLine)
line4.setFrameShadow(QtGui.QFrame.Sunken)
la.addWidget(line4)
 
a3_check = QtGui.QRadioButton( DialogBox )
la.addWidget(QtGui.QLabel("A3" ))
a3_check.setChecked(False)
la.addWidget(a3_check)
a4_check = QtGui.QRadioButton( DialogBox )
la.addWidget(QtGui.QLabel("A4"))
a4_check.setChecked(True)
buttonGrp2.addButton(a3_check)
buttonGrp2.addButton(a4_check)
la.addWidget(a4_check)
 
cartridge_check = QtGui.QCheckBox( DialogBox )
cartridge_check.setObjectName("checkBox")
la.addWidget(QtGui.QLabel("Cartridge"))
cartridge_check.setChecked(False)
la.addWidget(cartridge_check)
 
line6 = QtGui.QFrame(DialogBox)
line6.setFrameShape(QtGui.QFrame.HLine)
line6.setFrameShadow(QtGui.QFrame.Sunken)
la.addWidget(line6)
 
onedrawing_check = QtGui.QCheckBox( DialogBox )
onedrawing_check.setObjectName("checkBox")
la.addWidget(QtGui.QLabel("Group drawings in page"))
onedrawing_check.setChecked(True)
la.addWidget(onedrawing_check)
 
line7 = QtGui.QFrame(DialogBox)
line7.setFrameShape(QtGui.QFrame.HLine)
line7.setFrameShadow(QtGui.QFrame.Sunken)
la.addWidget(line7)
 
box = QtGui.QDialogButtonBox(DialogBox)
box.setOrientation(QtCore.Qt.Horizontal)
box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
la.addWidget(box)
 
QtCore.QObject.connect(box, QtCore.SIGNAL("accepted()"), proceed )
QtCore.QObject.connect(box, QtCore.SIGNAL("rejected()"), close )
QtCore.QMetaObject.connectSlotsByName(DialogBox)
DialogBox.show()
