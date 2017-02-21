import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

from . import transform
from src.utils import apiUtils

"""
Module for creating a Maya light object
"""


class Light(transform.Transform):
    """
    Generic light object
    """
    def __init__(self, *args, **kwargs):
        super(Light, self).__init__(*args, **kwargs)

    def create_node(self):
        cmds.select(clear=True)
        cmds.polySphere(name=self.name)

    # get light type
    # get light attributes - intensity, etc



