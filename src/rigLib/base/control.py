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
    def __init__(self, shape='circle', color=0, *args, **kwargs):
        self.shape = shape
        self.color = color
        super(Control, self).__init__(*args, **kwargs)

    def create_node(self):
        cmds.select(clear=True)
        cmds.circle(name=self.name)
        # create anim buffer parent node (optional)
        # create constraint buffer parent node (optional)
        # create parent buffer node
        # remove input nodes - delete history

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

    # get rotate order
    # set rotate order

    # add attr (float, boolean, enum)
    # remove attr
    # move attr (up, down)
