
import lib_repair_sketch_references_partDesign
from lib_repair_sketch_references_partDesign import *

reference_state = [] #list instead of dictionary to preserve order.

for obj in FreeCAD.ActiveDocument.Objects:
    if obj.TypeId == 'Sketcher::SketchObject':
        if obj.ExternalGeometry != [] or obj.Support != None:
            debugPrint(2, 'parsing ShapeElementReferences from %s' % obj.Name )
            exGeom = [ ShapeElementReference(se_obj, se) for se_obj,se in obj.ExternalGeometry ]
            if obj.Support != None:
                assert len( obj.Support[1] ) == 1
                supportGeom = ShapeElementReference( obj.Support[0], obj.Support[1][0])
            else:
                supportGeom = None
            reference_state.append( [ obj.Name, exGeom, supportGeom ] )

lib_repair_sketch_references_partDesign.reference_state = reference_state
debugPrint( 1, 'Sketch references recorded', timePrefix=True )
