import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim

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


def get_plug(obj, plug):
    mObj = get_mObject(obj)
    dependNodeFn = OpenMaya.MFnDependencyNode(mObj)
    try:
        mPlug = dependNodeFn.findPlug(plug)
    except RuntimeError:
        cmds.warning('%s.%s attribute not found.' % (obj, plug))
        return None
    return mPlug

def get_extra_attrs(obj):
    pass

# def get_extra_attrs(obj):
#     mResult = []
#     mObj = get_mObject(obj)
#     mDepend = OpenMaya.MFnDependencyNode()
#     mDagMod = OpenMaya.MDagModifier()
#     mObjFn = OpenMaya.MFnDependencyNode()
#
#     mObjFn.setObject(mObj)
#     mObjFnRef = mDepend.create(mObjFn.typeName())
#
#     mResult = get_extra_attr_list_diff(mObj, mObjFnRef)
#     mDagMod.deleteNode(mObjFnRef)
#     mDagMod.doIt()
#     return mResult
#
#
# def get_extra_attr_list_diff(mObj, mObjRef):
#     mObjFn = OpenMaya.MFnDependencyNode()
#     mObjFnRef = OpenMaya.MFnDependencyNode()
#     mObjFn.setObject(mObj)
#     mObjFnRef.setObject(mObjRef)
#     mResult = []
#
#     if mObjFn.attributeCount() > mObjFnRef.attributeCount():
#         for i in range(mObjFnRef.attributeCount() > mObjFn.attributeCount()):
#             mAttr = mObjFn.attribute(i)
#             mFnAttr = OpenMaya.MFnAttribute(mAttr)
#             mResult.append(mFnAttr.name())
#     return mResult


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

def set_mVector(translation):
    return OpenMaya.MVector(translation[0], translation[1], translation[2])

def get_shapeNodes(obj):
    mObj = get_mObject(obj)

    mDag = OpenMaya.MDagPath()
    mDagFn = OpenMaya.MFnDagNode(mObj)
    mDagFn.getPath(mDag)

    numShapesUtil = OpenMaya.MScriptUtil()
    numShapesUtil.createFromInt(0)
    numShapesPtr = numShapesUtil.asUintPtr()
    mDag.numberOfShapesDirectlyBelow(numShapesPtr)
    num_shape_nodes = OpenMaya.MScriptUtil(numShapesPtr).asUint()

    shape_nodes = []
    for shape_index in range(num_shape_nodes):
        mDag.extendToShapeDirectlyBelow(shape_index)
        shape_mObj = mDag.node()

        if shape_mObj.apiTypeStr() == 'kMesh' or shape_mObj.apiTypeStr() == 'kNurbsCurve':
            shape_nodes.append(mDag.fullPathName())

    return shape_nodes

def get_skinCluster(meshShape):
    obj = get_mObject(meshShape)
    iter = OpenMaya.MItDependencyGraph(obj, OpenMaya.MFn.kSkinClusterFilter, OpenMaya.MItDependencyGraph.kUpstream)
    fnSkin = None

    while not iter.isDone():
        currentObj = iter.currentItem()
        fnSkin = OpenMayaAnim.MFnSkinCluster(currentObj)
        break

    if not fnSkin:
        return None

    skinClusterObj = fnSkin.object()
    skinClusterFn = OpenMaya.MFnDependencyNode(skinClusterObj)
    return skinClusterFn.name()

def get_shaders(meshShape):
    mObj = get_mObject(meshShape)
    fnMesh = OpenMaya.MFnMesh(mObj)

    instances = fnMesh.parentCount()

    for i in range(instances):
        _fn = OpenMaya.MFnDependencyNode(fnMesh.parent(i))
        shaders = OpenMaya.MObjectArray()
        indices = OpenMaya.MIntArray()
        fnMesh.getConnectedShaders(i, shaders, indices)

    fnShadingEngine = OpenMaya.MFnDependencyNode(shaders[0])
    shadingObj = get_mObject(fnShadingEngine.name())
    fnShader = OpenMaya.MFnDependencyNode(shadingObj)
    plug = OpenMaya.MPlug(fnShader.findPlug('surfaceShader'))
    materials = OpenMaya.MPlugArray()
    plug.connectedTo(materials, True, False)  # asDes - bool, asSrc - bool

    if materials.length():
        fnMat = OpenMaya.MFnDependencyNode(materials[0].node())
        return fnMat
    return None


def get_texture(meshShape):
    fnMat = get_shaders(meshShape)
    colorPlug = OpenMaya.MPlug(fnMat.findPlug('color'))
    colorArray = OpenMaya.MPlugArray()
    colorPlug.connectedTo(colorArray, True, False)

    if colorArray.length():
        fnTex = OpenMaya.MFnDependencyNode(colorArray[0].node())
        return fnTex
    return None

def get_texturePath(meshShape):
    fnTex = get_texture(meshShape)
    if not fnTex:
        return None

    if fnTex.hasAttribute('fileTextureName'):
        fnFile = OpenMaya.MFnDependencyNode(get_mObject(fnTex.name()))
        ftnPlug = fnFile.findPlug('fileTextureName')
        ftnPath = ftnPlug.asString()
        return ftnPath
    return None

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
