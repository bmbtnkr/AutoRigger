from . import transform
import maya.cmds as cmds

"""
Module for creating a Maya joint object
"""


class Locator(transform.Transform):
    """
    Generic locator node
    """

    def create_node(self):
        cmds.select(clear=True)
        cmds.spaceLocator(name=self.name)
