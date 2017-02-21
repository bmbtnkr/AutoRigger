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

import maya.cmds as cmds
from src.rigLib.base import control
from src.rigLib.base import joint


class block(object):
    def __init__(self, metadata=None, joints=(),):
        self.metadata = metadata
        self.joints = joints


    def get_metadata(self):
        return self.metadata

    def set_metadata(self, data):
        data = self.metadata
        return self.metadata









