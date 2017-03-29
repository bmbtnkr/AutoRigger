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
        self.controls = []

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

        cmds.makeIdentity(self.control_joints[0], apply=True)

        return self.control_joints

    def get_joints(self):
        return self.control_joints

    def create_block(self):
        if not len(self.joints):
            cmds.warning('Could not build FkIkChain block, not enough joint(s)', self.joints)
            return False

        self.create_joints(self.joints)

        for index, jnt in enumerate(self.control_joints):
            fkCtrl = control.Control(name='ctrl_%s' % jnt.name,
                                     translateTo=jnt, rotateTo=jnt, normal=(1, 0, 0))

            self.controls.append(fkCtrl.name)
            fkCtrl.create_null_grps()
            fkCtrl.lockChannels(('t', 's', 'v'))
            cmds.orientConstraint(fkCtrl.name, jnt)

            try:
                if index:
                    cmds.parent(fkCtrl.nullGrp, self.controls[index-1])
            except IndexError:
                pass

        # self.fkMidCtrl.nullGrp.set_parent(self.fkRootCtrl.name)
        # self.fkEndCtrl.nullGrp.set_parent(self.fkMidCtrl.name)
