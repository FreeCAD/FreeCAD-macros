#todo add these to these files locally
import FreeCAD
import numpy, datetime
from assembly2lib import getSubElementAxis, getSubElementPos, sphericalSurfaceSelected, vertexSelected, LinearEdgeSelected, CircularEdgeSelected, cylindricalPlaneSelected, planeSelected, getObjectFaceFromName, getObjectEdgeFromName, getObjectVertexFromName
from variableManager import ReversePlacementTransformWithBoundsNormalization #also assembly2 code
from numpy import dot
norm = numpy.linalg.norm


def debugPrint( level, msg, timePrefix=False ):
    if level <= debugPrint.printLevel:
        tPrefix = '' if not timePrefix else datetime.datetime.now().strftime('%H:%M:%S ')
        FreeCAD.Console.PrintMessage( '%s%s\n' % (tPrefix,msg))
debugPrint.printLevel = 2


class ShapeElementReference:
    def __init__(self, object, subelement):
        self.object = object
        self.description = SubElementInfo( subelement, object )

    def getSubElementName( self ):
        se_org = self.description
        se_org_name = se_org.subElementName
        T = ReversePlacementTransformWithBoundsNormalization( self.object )
        se_current = SubElementInfo( se_org_name, self.object, T )
        if se_org == se_current:
            return se_org_name
        else:
            debugPrint(3, 'ShapeElementReference %s.%s has changed. Searching for closest match' % ( self.object.Name, se_org_name) )

        prefixDict = {'Vertexes':'Vertex','Edges':'Edge','Faces':'Face'}
        if se_org_name.startswith('Vertex'):
            listName = 'Vertexes'
        elif se_org_name.startswith( 'Edge' ):
            listName = 'Edges'
        elif se_org_name.startswith( 'Face' ):
            listName = 'Faces'
        se_errors = []
        for j, subelement in enumerate( getattr( self.object.Shape, listName) ):
            se_name =  '%s%i' % (prefixDict[listName], j+1 )
            if classifySubElement( self.object, se_name ) == se_org.category:
                se_errors.append( SubElementInfo( se_name, self.object, T) - se_org )
        min_error = min( se_errors )
        return min_error.se1.subElementName


class _SelectionWrapper:
    'as to interface with assembly2lib classification functions'
    def __init__(self, obj, subElementName):
        self.Object = obj
        self.SubElementNames = [subElementName]
def classifySubElement( obj, subElementName ):
    selection = _SelectionWrapper( obj, subElementName )
    if planeSelected( selection ):
        return 'plane'
    elif cylindricalPlaneSelected( selection ):
        return 'cylindricalSurface'
    elif CircularEdgeSelected( selection ):
        return 'circularEdge'
    elif LinearEdgeSelected( selection ):
        return 'linearEdge'
    elif vertexSelected( selection ):
        return 'vertex' #all vertex belong to Vertex classification
    elif sphericalSurfaceSelected( selection ):
        return 'sphericalSurface'
    else:
        raise RuntimeError, "unable to classify subelement %s" % (locals())


class SubElementInfo:
    def __init__(self, subElementName, obj, T=None):
        self.subElementName = subElementName
        if T == None:
            T =  ReversePlacementTransformWithBoundsNormalization( obj )
        self.category = classifySubElement( obj, subElementName )
        if self.category in ['cylindricalSurface','circularEdge','plane','linearEdge']:
            self.axis_T = T.unRotate( getSubElementAxis( obj, subElementName ) )
        self.pos_T = T( getSubElementPos( obj, subElementName ) )
    def cmpErrors( self, b):
        if self.category in ['cylindricalSurface','circularEdge','plane','linearEdge']:
            error1 = 1 - dot( self.axis_T, b.axis_T )
        else:
            error1 = 0
        error2 = norm( self.pos_T - b.pos_T )
        return error1, error2
    def __eq__( self, b ):
        if self.category == b.category:
            error1, error2 = self.cmpErrors( b ) 
            return error1 == 0 and error2 == 0
        else:
            return False
    def __sub__(self, b):
        return SubElementInfo_Absolute_Difference( self, b )


class SubElementInfo_Absolute_Difference:
    def __init__(self, se1, se2):
        self.se1 = se1
        self.se2 = se2 
        self.error1, self.error2 = se1.cmpErrors( se2 )
    def __lt__( self, b):
        if self.error1 <> b.error1:
            return self.error1 < b.error1
        else:
            return self.error2 < b.error2
