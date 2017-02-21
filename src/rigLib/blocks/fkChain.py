"""
Module for creating an AutoRigger fk/ik chain component

FK/IK chain component - Animateable component
Requires a joint chain length of 3
Contains two sets of controls for animating in FK and IK
Control Flags: FK[...], IK, Pole Vector, FK/IK Switch
"""

# create an fk/ik chain metadata node first

# needs fk joints x3
# ik joints x3

# pole vector transform?
#

# fk/ik switch attribute - in metadata node???


# tagging arm joints:
# chain root = "arm"
# chain end = "arm"
# chain terminator = "arm"

# ToDo: make this work with any number of middle joints

import maya.cmds as cmds
from src.rigLib.base import transform
from src.rigLib.base import control
from src.rigLib.base import joint


class FkChain(object):
    def __init__(self, joints=()):
        self.joints = joints
        self.control_joints = None

    def create_joints(self, joints):
        cmds.select(clear=True)
        orig_joints = [joint.Joint(name=jnt, create=False) for jnt in joints]
        self.control_joints = []

        for index, jnt in enumerate(orig_joints):
            parent = None if index == 0 else self.control_joints[index - 1]
            # print index, jnt, parent, self.control_joints, index + 1, len(orig_joints), index + 1 < len(orig_joints)

            if index < len(orig_joints):
                control_joint = joint.Joint(name='%s_fk' % jnt, translateTo=jnt, rotateTo=jnt,
                                             jointOrient=jnt.get_joint_orient(), jointTag='fkChain', parent=parent)

                self.control_joints.append(control_joint)

        cmds.makeIdentity(self.control_joints[1:-1], apply=True)

        return self.control_joints

    def get_joints(self):
        return self.control_joints

    def create_controls(self):
        pass

    def get_controls(self):
        pass

    def get_constraints(self):
        pass

    def create_block(self):
        if len(self.joints) < 3:
            cmds.warning('Could not build FkIkChain block, not enough joints', self.joints)
            return False

        self.create_joints(self.joints)

        self.fkRootCtrl = control.Control(name=self.rootJnt.name.replace('jt', 'ctrl').replace('template', 'fk'),
                                          translateTo=self.rootJnt, rotateTo=self.rootJnt, normal=(1, 0, 0))

        self.fkMidCtrl = control.Control(name=self.midJnt.name.replace('jt', 'ctrl').replace('template', 'fk'),
                                         translateTo=self.midJnt, rotateTo=self.midJnt, normal=(1, 0, 0))

        self.fkEndCtrl = control.Control(name=self.endJnt.name.replace('jt', 'ctrl').replace('template', 'fk'),
                                         translateTo=self.endJnt, rotateTo=self.endJnt)

        self.fkRootCtrl.create_null_grps()
        self.fkMidCtrl.create_null_grps()
        self.fkEndCtrl.create_null_grps()

        self.fkMidCtrl.nullGrp.set_parent(self.fkRootCtrl.name)
        self.fkEndCtrl.nullGrp.set_parent(self.fkMidCtrl.name)

        self.fkRootCtrl.lockChannels(('t', 's', 'v'))
        self.fkMidCtrl.lockChannels(('t', 's', 'v'))
        self.fkEndCtrl.lockChannels(('t', 's', 'v'))

        fkRootOrientConstraint = cmds.orientConstraint(self.fkRootCtrl.name, self.rootJnt)[0]
        fkMidOrientConstraint = cmds.orientConstraint(self.fkMidCtrl.name, self.midJnt)[0]
        fkEndOrientConstraint = cmds.orientConstraint(self.fkEndCtrl.name, self.endJnt)[0]

    def set_pole_vector(self):
        pass

    def get_pole_vector(self):
        return self.poleVector

    def get_joints(self):
        return self.joints()
