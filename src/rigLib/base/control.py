import maya.cmds as cmds

from . import transform


"""
Module for creating a Maya control object
"""


class Control(transform.Transform):
    """
    Generic joint node
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

    # get shape
    def get_shapes(self):
        cmds.listRelatives(self.name, children=True, type='shape')

    # set shapes

    # parent shapes

    # get color
    def get_color(self):
        cmds.getAttr()
    # set color

    # get rotate order
    # set rotate order

    # add attr (float, boolean, enum)
    # remove attr
    # move attr (up, down)
























