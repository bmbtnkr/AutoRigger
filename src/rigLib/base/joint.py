from . import transform
import maya.cmds as cmds

"""
Module for creating a Maya joint object
"""


class Joint(transform.Transform):
    """
    Generic joint node
    """
    def __init__(self, jointTag='null', jointOrient=(0, 0, 0), rotateOrder='xyz', *args, **kwargs):
        self.jointTag = jointTag
        self.jointOrient = jointOrient
        self.rotateOrder = rotateOrder
        super(Joint, self).__init__(*args, **kwargs)
        self.side = self.set_side()
        self.length = 1

    def create_node(self):
        cmds.select(clear=True)
        cmds.joint(name=self.name, orientation=self.jointOrient, rotationOrder=self.rotateOrder)
        cmds.setAttr('%s.type' % self.name, 18)
        cmds.setAttr('%s.otherType' % self.name, self.jointTag, type='string')
        # cmds.addAttr(self.name, longName=self.jointTag, attributeType='string')

    def get_side(self):
        self.side = cmds.getAttr('%s.side' % self.name)
        return self.side

    def set_side(self):
        self.translate = self.get_translation()
        if self.translate[0] == 0:
            cmds.setAttr('%s.side' % self.name, 0)
            self.side = 'center'
        elif self.translate[0] > 0:
            cmds.setAttr('%s.side' % self.name, 1)
            self.side = 'left'
        else:
            cmds.setAttr('%s.side' % self.name, 2)
            self.side = 'right'
        return self.side

    def get_joint_orient(self):
        self.jointOrient = cmds.joint(self.name, orientation=True, query=True)
        return self.jointOrient

    def set_joint_orient(self):
        cmds.joint(self.name, orientation=self.jointOrient, edit=True)
        return self.jointOrient

    def get_length(self):
        # get the length of the joint chain based on number of children?
        # based on parents and children?
        # based on meta data length string attribute?
        # based on controller meta data attr???
        return self.length

    # set rotate order

    # get joint orient ?

    # get rotate order ?

    # get joint labels - side, other type,
    # set joint labels