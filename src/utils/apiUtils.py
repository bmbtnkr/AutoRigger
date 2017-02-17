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

