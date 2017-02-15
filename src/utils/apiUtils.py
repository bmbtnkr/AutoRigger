import maya.OpenMaya as om

def get_mObject(obj):
    sel = om.MSelectionList()
    om.MGlobal.getSelectionListByName(obj, sel)
    mObj = om.MObject()
    sel.getDependNode(0, mObj)
    return mObj

def get_mDagPath(obj):
    sel = om.MSelectionList()
    om.MGlobal.getSelectionListByName(obj, sel)
    mDag = om.MDagPath()
    sel.getDagPath(0, mDag)
    return mDag

