from . import transform
import maya.cmds as cmds

"""
Module for creating a Maya joint object
"""


class Joint(transform.Transform):
    """
    Generic joint node
    """
    def __init__(self, jointOrient=(0, 0, 0), rotateOrder='xyz', *args, **kwargs):
        self.jointOrient = jointOrient
        self.rotateOrder = rotateOrder
        super(Joint, self).__init__(*args, **kwargs)

    def create_node(self):
        cmds.select(clear=True)
        cmds.joint(name=self.name, orientation=self.jointOrient, rotationOrder=self.rotateOrder)
