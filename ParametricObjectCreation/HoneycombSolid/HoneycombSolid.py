"""
HoneycombSolid --> Honeycomb solid creator.
(c) 2021 Christian González Di Antonio <christiangda@gmail.com>
"""

__Version__ = "v1.0.2"

import FreeCAD
import Part
import math 
from FreeCAD import Base


class HoneycombSolid:

	def __init__(self, obj):
		''' Custom properties of Honeycomb feature '''
		obj.addProperty("App::PropertyLength","Length","Honeycomb","Length of the Honeycomb").Length=100.0
		obj.addProperty("App::PropertyLength","Width","Honeycomb","Width of the Honeycomb").Width=100.0
		obj.addProperty("App::PropertyLength","Height","Honeycomb", "Height of the Honeycomb").Height=2.0
		obj.addProperty("App::PropertyLength","Circumradius","Polygon","Radius of the inner circle").Circumradius=5.0
        	#obj.addProperty("App::PropertyLength","Edges","Polygon","Poligon number of edges").Edges=6.0
		obj.addProperty("App::PropertyLength","Tickness","Walls","Tickness of the honeycomb walls").Tickness=1.0
		obj.Proxy = self
	
		self.Type = 'HoneycombSolid'
		self.Version = __version__
        

	def onChanged(self, fp, prop):
		''' Print the name of the property that has changed '''
		FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

	def execute(self, fp):
		''' Print a short message when doing a recomputation, this method is mandatory '''
		FreeCAD.Console.PrintMessage("Recompute Python HoneycombSolid feature\n")

		length = fp.Length
		width = fp.Width
		height = fp.Height
		radius = fp.Circumradius
		tickness = fp.Tickness
        
		#edges = fp.Edges
		edges = 6

		#######################################################################
		# Container box, used to cut the polygon array
		container = Part.makeBox(length,width,height)

		#######################################################################
		# create the first polygon
		figure = []
		m=Base.Matrix()
		edges_angle = math.radians(360.0/edges)
		m.rotateZ(edges_angle)
		v=Base.Vector(radius,0,0)

		for i in range(edges):
			figure.append(v)
			v = m.multiply(v)

		figure.append(v)
		polygon = Part.makePolygon(figure)

		# move it to the center of the container box	
		polygon.translate(Base.Vector(length/2, width/2, 0))

		# create a face for the first polygon
		f1=Part.Face([polygon])

		#######################################################################
		# create copies of poligon using radial pattern

		# calculate how many circunferencias needs to cover the maximun length of the container box
		n_cols = math.ceil( (length / (radius + tickness) / 2) )
		n_rows = math.ceil( (width / (radius + tickness) / 2) + 3)
		# FreeCAD.Console.PrintMessage("n_cols: " + str(n_cols) + " n_rows: " + str(n_rows) + "\n")
	
		# To store all the poligons face
		e_faces = []
		e_faces.append(f1) # add the first one created before

		# Iterate over each imaginary circle which circunference contains the center of the polygon circle 
		for column in range(-n_cols, n_cols):
			for row in range(-n_rows, n_rows):
				# omit the first
				if (column != 0) or (row != 0):
					if column % 2 != 0:
					# odd
						if row % 2 != 0:
						# odd
							centers_distance = tickness + 2 * radius * math.sin(edges_angle)
							x_delta = centers_distance *  math.sin(edges_angle)
							y_delta = centers_distance * math.cos(edges_angle)

							x_origin = column * x_delta 
							y_origin = row * y_delta
		
							delta_x_y = Base.Vector(x_origin, y_origin,0)
		
							polygon_copy = polygon.copy()
							polygon_copy.translate(delta_x_y)		
							fn=Part.Face([polygon_copy])
							e_faces.append(fn)

					else:
					# even
						if row <= (n_rows/2) and row >= (-n_rows/2):
							centers_distance = tickness + 2 * radius * math.sin(edges_angle)
							x_delta = centers_distance  * math.sin(edges_angle)
							y_delta = centers_distance
							
							x_origin = column * x_delta 
							y_origin = row * y_delta
		
							delta_x_y = Base.Vector(x_origin, y_origin,0)
		
							polygon_copy = polygon.copy()
							polygon_copy.translate(delta_x_y)		
							fn=Part.Face([polygon_copy])
							e_faces.append(fn)

		# join all the faces
		mshell = Part.makeShell(e_faces)
		extruded_polygon = mshell.extrude(Base.Vector(0,0,height))

		# cut the array of solids using the container box
		shape = container.cut(extruded_polygon) # comment it to see the array of solids

		fp.Shape = shape # comment it to see the array of solids
		#fp.Shape = extruded_polygon # uncomment it to see the array of solids

	def __getstate__(self):
		''' When saving the document this object gets stored using Python's cPickle module.
		Since we have some un-pickable here -- the Coin stuff -- we must define this method
		to return a tuple of all pickable objects or None.
		'''
		return self.Type, self.Version

	def __setstate__(self,state):
		''' When restoring the pickled object from document we have the chance to set some
		internals here. Since no data were pickled nothing needs to be done here.
		'''
		self.Type = state[0]
		self.Version = state[1]

class ViewProviderHoneycombSolid:
	def __init__(self, obj):
		''' Set this object to the proxy object of the actual view provider '''
		obj.Proxy = self

	def attach(self, obj):
		''' Setup the scene sub-graph of the view provider, this method is mandatory '''
		return

	def updateData(self, fp, prop):
		''' If a property of the handled feature has changed we have the chance to handle this here '''
		return

	def getDisplayModes(self,obj):
		''' Return a list of display modes. '''
		modes=[]
		return modes

	def getDefaultDisplayMode(self):
		''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
		return "Shaded"

	def setDisplayMode(self,mode):
		''' Map the display mode defined in attach with those defined in getDisplayModes.
		Since they have the same names nothing needs to be done. This method is optional.
		'''
		return mode

	def onChanged(self, vp, prop):
		''' Print the name of the property that has changed '''
		FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

	def getIcon(self):
		''' Return the icon in XMP format which will appear in the tree view. This method is optional
		and if not defined a default icon is shown.
		'''
		return """
			/* XPM */
			static const char * ViewProviderHoneycombSolid_xpm[] = {
			"16 16 6 1",
			" 	c None",
			".	c #141010",
			"+	c #615BD2",
			"@	c #C39D55",
			"#	c #000000",
			"$	c #57C355",
			"        ........",
			"   ......++..+..",
			"   .@@@@.++..++.",
			"   .@@@@.++..++.",
			"   .@@  .++++++.",
			"  ..@@  .++..++.",
			"###@@@@ .++..++.",
			"##$.@@$#.++++++.",
			"#$#$.$$$........",
			"#$$#######      ",
			"#$$#$$$$$#      ",
			"#$$#$$$$$#      ",
			"#$$#$$$$$#      ",
			" #$#$$$$$#      ",
			"  ##$$$$$#      ",
			"   #######      "};
			"""

	def __getstate__(self):
		''' When saving the document this object gets stored using Python's cPickle module.
		Since we have some un-pickable here -- the Coin stuff -- we must define this method
		to return a tuple of all pickable objects or None.
		'''
		return None

	def __setstate__(self,state):
		''' When restoring the pickled object from document we have the chance to set some
		internals here. Since no data were pickled nothing needs to be done here.
		'''
		return None


def makeHoneycombSolid():
	doc = FreeCAD.activeDocument()

	if doc is None:
		doc = FreeCAD.newDocument()

	obj = doc.addObject("Part::FeaturePython", "HoneycombSolid")
	HoneycombSolid(obj)
	ViewProviderHoneycombSolid(obj.ViewObject)
	doc.recompute()
