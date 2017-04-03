import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

from . import transform
from src.utils import apiUtils

"""
Module for creating a Maya control object
"""


class Control(transform.Transform):
    """
    Generic control object
    """
    def __init__(self, shape='circle', color=0, normal=(0,1,0), *args, **kwargs):
        self.shape = shape
        self.color = color
        self.normal = normal
        super(Control, self).__init__(*args, **kwargs)
        self.nullGrp = None
        self.offsetGrp = None
        self.animGrp = None

    def create_node(self):
        cmds.select(clear=True)

        control = cmds.circle(name=self.name, normal=self.normal) # move this to set shapes
        cmds.delete(self.name, constructionHistory=True)
        cmds.setAttr('%s.rotateOrder' % self.name, channelBox=True, keyable=False)
        self.name = transform.Transform(control[0], create=False)

    def get_null_grps(self):
        return self.nullGrp, self.offsetGrp, self.animGrp

    def create_null_grps(self):
        self.nullGrp = transform.Transform(name='null_%s_grp' % self.name)
        self.offsetGrp = transform.Transform(name='offset_%s_grp' % self.name, parent=self.nullGrp)
        self.animGrp = transform.Transform(name='anim_%s_grp' % self.name, parent=self.offsetGrp)

        self.nullGrp.set_translation(self.name.get_translation())
        self.nullGrp.set_rotation(self.name.get_rotation())
        self.nullGrp.set_scale(self.name.get_scale())

        self.name.set_parent(self.animGrp)
        self.name.set_translation(worldSpace=False)
        self.name.set_rotation(worldSpace=False)
        self.name.set_scale()
        return self.nullGrp, self.offsetGrp, self.animGrp

    # get shapes
    def get_shapes(self):
        cmds.listRelatives(self.name, children=True, type='shape')

        mDag = apiUtils.get_mDagPath(self.name)
        shapesUtil = OpenMaya.MScriptUtil()
        shapesUtil.createFromInt(0)
        shapesPtr = shapesUtil.asUintPtr()
        mDag.numberOfShapesDirectlyBelow(shapesPtr)

        numShapes = OpenMaya.MScriptUtil(shapesPtr).asUint()
        shapes = []
        for i in range(numShapes):
            mDag.extendToShapeDirectlyBelow(i)
            shapes.append(mDag.fullPathName())
            mDag = apiUtils.get_mDagPath(self.name)

        return shapes

    # set shapes
    def set_shapes(self):
        pass

    # parent shapes

    # get color
    def get_color(self):
        if not len(self.get_shapes()):
            return False
        elif len(self.get_shapes()) == 1:
            return [cmds.getAttr('%s.overrideColor' % i) for i in self.get_shapes()][0]
        elif len(self.get_shapes()) > 1:
            return [cmds.getAttr('%s.overrideColor' % i) for i in self.get_shapes()]

    # set color
    def set_color(self, color=0):
        if not self.get_shapes():
            return False
        if color > 31:
            cmds.warning('Cannot set the attribute %s.overrideColor past its maximum value of 31. # ' % self.get_shapes())
            return False
        [cmds.setAttr('%s.overrideColor' % shape, color) for shape in self.get_shapes()]
        return True

    # get rotate order
    # set rotate order

    # add attr (float, boolean, enum)
    # remove attr
    # move attr (up, down)
