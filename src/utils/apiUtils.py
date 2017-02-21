import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

def get_mObject(obj):
    sel = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getSelectionListByName(obj, sel)
    mObj = OpenMaya.MObject()
    sel.getDependNode(0, mObj)
    return mObj

def get_mDagPath(obj):
    sel = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getSelectionListByName(obj, sel)
    mDag = OpenMaya.MDagPath()
    sel.getDagPath(0, mDag)
    return mDag

def get_matrix(mObj):
    pass

def decomp_matrix(mObj, matrix):
    pass

def getAllExtraAttributes(obj):
    m_result = []
    m_obj         = get_mObject(obj)
    m_workMFnDep  = OpenMaya.MFnDependencyNode()
    m_workMDagMod = OpenMaya.MDagModifier()
    m_objFn    = OpenMaya.MFnDependencyNode()
    m_objFn.setObject( m_obj ) # get function set from MObject
    m_objRef = m_workMFnDep.create( m_objFn.typeName() ) # Create reference MObject of the given type
    # -- get the list --
    m_result = getAttrListDifference( m_obj,m_objRef )
    # --
    m_workMDagMod.deleteNode( m_objRef ) # set node to delete
    m_workMDagMod.doIt() # execute delete operation
    return m_result

def getAttrListDifference( m_obj, m_objRef ):
    m_objFn    = OpenMaya.MFnDependencyNode()
    m_objRefFn = OpenMaya.MFnDependencyNode()
    m_objFn.setObject( m_obj )
    m_objRefFn.setObject( m_objRef )
    m_result = []
    if ( m_objFn.attributeCount() > m_objRefFn.attributeCount() ):
        for i in range( m_objRefFn.attributeCount(), m_objFn.attributeCount()  ):
            m_atrr = m_objFn.attribute(i)
            m_fnAttr = OpenMaya.MFnAttribute( m_atrr )
            m_result.append( m_fnAttr.name() )
    return m_result





# import maya.cmds as cmds
# import maya.api.OpenMaya as OpenMaya
# import math
# import sys
#
# def getMatrix(node):
#  '''
#  Gets the world matrix of an object based on name.
#  '''
#  #Selection list object and MObject for our matrix
#  selection = OpenMaya.MSelectionList()
#  matrixObject = OpenMaya.MObject()
#
#  #Adding object
#  selection.add(node)
#
#  #New api is nice since it will just return an MObject instead of taking two arguments.
#  MObjectA = selection.getDependNode(0)
#
#  #Dependency node so we can get the worldMatrix attribute
#  fnThisNode = OpenMaya.MFnDependencyNode(MObjectA)
#
#  #Get it's world matrix plug
#  worldMatrixAttr = fnThisNode.attribute( "worldMatrix" )
#
#  #Getting mPlug by plugging in our MObject and attribute
#  matrixPlug = OpenMaya.MPlug( MObjectA, worldMatrixAttr )
#  matrixPlug = matrixPlug.elementByLogicalIndex( 0 )
#
#  #Get matrix plug as MObject so we can get it's data.
#  matrixObject = matrixPlug.asMObject(  )
#
#  #Finally get the data
#  worldMatrixData = OpenMaya.MFnMatrixData( matrixObject )
#  worldMatrix = worldMatrixData.matrix( )
#
#  return worldMatrix
#
# def decompMatrix(node,matrix):
#  '''
#  Decomposes a MMatrix in new api. Returns an list of translation,rotation,scale in world space.
#  '''
#  #Rotate order of object
#  rotOrder = cmds.getAttr('%s.rotateOrder'%node)
#
#  #Puts matrix into transformation matrix
#  mTransformMtx = OpenMaya.MTransformationMatrix(matrix)
#
#  #Translation Values
#  trans = mTransformMtx.translation(OpenMaya.MSpace.kWorld)
#
#  #Euler rotation value in radians
#  eulerRot = mTransformMtx.rotation()
#
#  #Reorder rotation order based on ctrl.
#  eulerRot.reorderIt(rotOrder)
#
#  #Find degrees
#  angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]
#
#  #Find world scale of our object.
#  scale = mTransformMtx.scale(OpenMaya.MSpace.kWorld)
#
#  #Return Values
#  return [trans.x,trans.y,trans.z],angles,scale
#
# #If we're in the main namespace run our stuffs!
# if __name__ == '__main__':
#  #Defining object name.
#  nodeName = 'yourName'
#
#  #Get Matrix
#  mat = getMatrix(nodeName)
#
#  #Decompose matrix
#  matDecomp = decompMatrix(nodeName,mat)
#
#  #Print our values
#  sys.stdout.write('\n---------------------------%s---------------------------\n'%nodeName)
#  sys.stdout.write('\nTranslation : %s' %matDecomp[0])
#  sys.stdout.write('\nRotation    : %s' %matDecomp[1])
#  sys.stdout.write('\nScale       : %s\n' %matDecomp[2])






























# def set_poleVector(rootJnt, midJnt, endJnt):
#     rootIkPos = cmds.xform(rootJnt, translation=True, worldSpace=True, query=True)
#     midIkPos = cmds.xform(midJnt, translation=True, worldSpace=True, query=True)
#     endIkPos = cmds.xform(endJnt, translation=True, worldSpace=True, query=True)
#
#
#
#
#     # I'm using hard-coded joint names for this example
#     # Create Joint Vectors
#     try:
#         shoulderIkPos = cmds.xform('shldr_jnt', q=True, ws=True, t=True)
#         shoulderIkVec = OpenMaya.MVector(shoulderIkPos[0], shoulderIkPos[1], shoulderIkPos[2])
#         elbowIkPos = cmds.xform('elbw_jnt', q=True, ws=True, t=True)
#         elbowIkVec = OpenMaya.MVector(elbowIkPos[0], elbowIkPos[1], elbowIkPos[2])
#         wristIkPos = cmds.xform('wrst_jnt', q=True, ws=True, t=True)
#         wristIkVec = OpenMaya.MVector(wristIkPos[0], wristIkPos[1], wristIkPos[2])
#     except:
#             cmds.error('All arm joints not found or named incorrectly')
#
#     # Transpose vectors to correct pole vector translation point
#     bisectorVec = (shoulderIkVec * 0.5) + (wristIkVec * 0.5)
#     transposedVec = (elbowIkVec * distanceScale) - (bisectorVec * distanceScale)
#     ikChainPoleVec = bisectorVec + transposedVec
#
#     # Create a pole vector
#     poleVecCon = cmds.spaceLocator(name='%selbowPV' % prefix)
#     poleVecPos = [ikChainPoleVec.x, ikChainPoleVec.y, ikChainPoleVec.z]
#     cmds.xform(poleVecCon, t=poleVecPos)
#     cmds.delete(cmds.orientConstraint('elbw_jnt', poleVecCon))
#
#     # Visualize Vectors and End Points
#     if verbose:
#         for vector, letter in zip([bisectorVec, transposedVec, ikChainPoleVec,
#                                    shoulderIkVec, elbowIkVec, wristIkVec],
#                                   ['bisectorVec', 'transposedVec', 'ikChainPoleVec',
#                                   'shoulderIk', 'elbowIk', 'wristIk']):
#             cmds.spaceLocator(n='%sVecLoc' % letter, p=[vector.x, vector.y, vector.z])
#             cmds.curve(n='%sVecCurve' % letter, degree=1, p=[(0, 0, 0), (vector.x, vector.y, vector.z)])
#
#     return poleVecCon