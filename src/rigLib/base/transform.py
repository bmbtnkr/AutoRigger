import itertools
import maya.cmds as cmds

"""
Module for creating a Maya transform object
"""


class Transform(object):
    """
    Generic transform node
    """

    def __init__(self, name='_null', create=True, worldMatrix=None, parent=None,
                 translateTo=None, rotateTo=None,
                 lockAttrs=None, hideAttrs=None, nonKeyableAttrs=None,
                 translate=None, rotate=None, scale=None):

        self.name = name
        self.create = create
        self.translate = translate
        self.rotate = rotate
        self.scale = scale
        self.worldMatrix = worldMatrix
        self.parent = parent
        self.translateTo = translateTo
        self.rotateTo = rotateTo
        self.lockAttrs = lockAttrs
        self.hideAttrs = hideAttrs
        self.nonKeyableAttrs = nonKeyableAttrs
        self.nullGrp = None

        if create:
            self.create_node()

        if self.translate:
            self.set_translation(translation=self.translate, worldSpace=True)

        if self.rotate:
            self.set_rotation(rotation=self.rotate, worldSpace=True)

        if self.scale:
            self.set_scale(scale=self.scale)

        if self.worldMatrix:
            self.set_matrix(self.worldMatrix)

        if self.parent:
            self.set_parent(self.parent)

        if self.translateTo:
            self.pointSnapTo(self.translateTo)

        if self.rotateTo:
            self.orientSnapTo(self.rotateTo)

        if self.lockAttrs:
            self.lockChannels(self.lockAttrs)

        if self.hideAttrs:
            self.hideChannels(self.hideAttrs)

        if self.nonKeyableAttrs:
            self.nonKeyableChannels(self.nonKeyableAttrs)

    def __repr__(self):
        return self.name

    def create_node(self):
        cmds.select(clear=True)
        cmds.group(name=self.name, empty=True)

    def create_null_grp(self):
        self.nullGrp = cmds.group(name='null_%s_grp' % self.name, empty=True)
        pos = cmds.xform(self.name, translation=True, worldSpace=True, query=True)
        rot = cmds.xform(self.name, rotation=True, worldSpace=True, query=True)
        scl = cmds.xform(self.name, scale=True, worldSpace=True, query=True)
        cmds.xform(self.nullGrp, translation=pos, rotation=rot, scale=scl, worldSpace=True)
        cmds.parent(self.nullGrp, self.get_parent())
        cmds.parent(self.name, self.nullGrp)

    def delete(self):
        cmds.delete(self.name)

    def rename(self, new_name):
        cmds.rename(self.name, new_name)
        self.name = new_name
        return self.name

    def get_path(self, obj=None):
        if obj:
            return cmds.ls(obj, long=True)[0]
        return cmds.ls(self.name, long=True)[0]

    def get_parent(self):
        parent = cmds.listRelatives(self.name, parent=True)
        if parent:
            return parent[0]
        return None

    def set_parent(self, parent):
        parent = self.get_path(parent)
        cmds.parent(self.name, parent)
        return parent

    def get_translation(self, worldSpace=True):
        if worldSpace:
            self.translate = cmds.xform(self.name, translation=True, worldSpace=True, query=True)
            return self.translate
        else:
            self.translate = cmds.xform(self.name, translation=True, objectSpace=True, query=True)
            return self.translate

    def set_translation(self, translation=(0, 0, 0), worldSpace=True):
        if worldSpace:
            cmds.xform(self.name, translation=translation, worldSpace=True)
            self.translate = self.get_translation(worldSpace=True)
            return self.translate
        else:
            cmds.xform(self.name, translation=translation, objectSpace=True)
            self.translate = self.get_translation(worldSpace=False)
            return self.translate

    def get_rotation(self, worldSpace=True):
        if worldSpace:
            self.rotate = cmds.xform(self.name, rotation=True, worldSpace=True, query=True)
            return self.rotate
        else:
            self.rotate = cmds.xform(self.name, rotation=True, objectSpace=True, query=True)
            return self.rotate

    def set_rotation(self, rotation=(0, 0, 0), worldSpace=True):
        if worldSpace:
            cmds.xform(self.name, rotation=rotation, worldSpace=True)
            self.rotate = self.get_rotation(worldSpace=True)
            return self.rotate
        else:
            cmds.xform(self.name, rotation=rotation, objectSpace=True)
            self.rotate = self.get_rotation(worldSpace=False)
            return self.rotate

    def get_scale(self):
        self.scale = cmds.xform(self.name, scale=True, relative=True, query=True)
        return self.scale

    def set_scale(self, scale=(1, 1, 1)):
        cmds.xform(self.name, scale=scale)
        self.scale = self.get_scale()
        return self.scale

    def get_matrix(self, worldSpace=True):
        if worldSpace:
            self.worldMatrix = cmds.xform(self.name, matrix=True, worldSpace=True, query=True)
            return self.worldMatrix
        else:
            self.worldMatrix = cmds.xform(self.name, matrix=True, objectSpace=True, query=True)
            return self.worldMatrix

    def set_matrix(self, matrix=(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1), worldSpace=True):
        if worldSpace:
            cmds.xform(self.name, matrix=matrix, worldSpace=True)
            self.worldMatrix = self.get_matrix(worldSpace=True)
            return self.worldMatrix
        else:
            cmds.xform(self.name, matrix=matrix, objectSpace=True)
            self.worldMatrix = self.get_matrix(worldSpace=False)
            return self.worldMatrix

    def pointSnapTo(self, translateTo):
        if cmds.objExists(translateTo):
            temp_translate = cmds.xform(translateTo, translation=True, worldSpace=True, query=True)
            cmds.xform(self.name, translation=temp_translate, worldSpace=True)

    def orientSnapTo(self, rotateTo):
        if cmds.objExists(rotateTo):
            temp_rotate = cmds.xform(self.rotateTo, rotation=True, worldSpace=True, query=True)
            cmds.xform(self.name, rotation=temp_rotate, worldSpace=True)

    def parentSnapTo(self, parentTo):
        if cmds.objExists(parentTo):
            self.pointSnapTo(parentTo)
            self.orientSnapTo(parentTo)

    def lockChannels(self, lockChannels=None):
        if not lockChannels and not self.lockAttrs:
            return False
        channels = lockChannels if lockChannels else self.lockAttrs
        if type(channels) == list or type(channels) == tuple:
            [cmds.setAttr('%s.%s' % (self.name, attr), lock=True) for attr in channels]
        elif type(channels) == str:
            cmds.setAttr('%s.%s' % (self.name, channels), lock=True)
        else:
            return False
        return True

    def hideChannels(self, hideChannels=None):
        if not hideChannels and not self.hideAttrs:
            return False
        channels = hideChannels if hideChannels else self.hideAttrs

        # necessary to explicitly call which attributes to hide in cmds.setAttr()
        channels = list(channels)
        for attr in channels:
            if attr == 't' or attr == 'r' or attr == 's':
                channels[channels.index(attr)] = \
                    ['%s%s' % (attr, axis) for axis in ['x', 'y', 'z']]
            else:
                channels[channels.index(attr)] = [attr]
        channels = tuple(list(itertools.chain.from_iterable(channels)))

        if type(channels) == list or type(channels) == tuple:
            [cmds.setAttr('%s.%s' % (self.name, attr), keyable=False, channelBox=False) for attr in channels]
        elif type(channels) == str:
            cmds.setAttr('%s.%s' % (self.name, channels), keyable=False, channelBox=False)
        else:
            return False
        return True

    def nonKeyableChannels(self, nonKeyableChannels=None):
        if not nonKeyableChannels and not self.nonKeyableAttrs:
            return False
        channels = nonKeyableChannels if nonKeyableChannels else self.hideAttrs
        if type(channels) == list or type(channels) == tuple:
            [cmds.setAttr('%s.%s' % (self.name, attr), keyable=False, channelBox=True) for attr in channels]
        elif type(channels) == str:
            print channels
            print '%s.%s' % (self.name, channels)
            cmds.setAttr('%s.%s' % (self.name, channels), keyable=False, channelBox=True)
        else:
            return False
        return True

    def duplicate(self):
        cmds.duplicate(self.name)
