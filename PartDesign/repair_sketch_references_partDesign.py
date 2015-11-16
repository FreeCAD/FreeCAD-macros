
import lib_repair_sketch_references_partDesign
from lib_repair_sketch_references_partDesign import *


debugPrint(2,'repair_sketch_references started',timePrefix=True)

reference_state = lib_repair_sketch_references_partDesign.reference_state
if len( reference_state ) == 0:
    raise ValueError, "record_sketch_references needs to be run first"
for sketch_name, exGeom, supportGeom in reference_state:
    debugPrint(3,'  checking %s' % sketch_name)
    sketch = FreeCAD.ActiveDocument.getObject( sketch_name )
    assert sketch != None
    changed = False

    newExtGeom = []
    for g in exGeom:
        se_name = g.getSubElementName()
        old_name = g.description.subElementName
        if se_name != old_name:
            changed = True
            debugPrint( 2,'  ExternalGeometry: %s -> %s' % (se_name, old_name) )
        newExtGeom.append( ( g.object, se_name) )

    if supportGeom != None:
        se_name = supportGeom.getSubElementName()
        old_name = supportGeom.description.subElementName
        if se_name != old_name:
            changed = True
            debugPrint( 2,'  supportGeom: %s->%s' % (se_name, old_name) )
            sketch.Support = ( supportGeom.object, [se_name] )

    if changed:
        sketch.ExternalGeometry = newExtGeom
        FreeCAD.ActiveDocument.recompute()
        debugPrint(3,'  FreeCAD.ActiveDocument.recompute()')

debugPrint(1,'repair_sketch_references completed',timePrefix=True)
