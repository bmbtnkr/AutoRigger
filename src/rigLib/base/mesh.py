import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

from . import transform
from src.utils import apiUtils

"""
Module for creating a Maya mesh object
"""


class Mesh(transform.Transform):
    """
    Generic mesh object
    """
    def __init__(self, *args, **kwargs):
        super(Mesh, self).__init__(*args, **kwargs)

    def create_node(self):
        cmds.select(clear=True)
        cmds.polySphere(name=self.name)

    # get shape?
    # add custom rig attributes?

    # get shader
    # get texture

    # get uvs

    # get uv maps

    # get connected skin cluster if skin cluster






