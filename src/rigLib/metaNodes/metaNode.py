"""
Module for creating an AutoRigger meta data node
"""

import maya.cmds as cmds
from src.utils import apiUtils

# ToDo: code cleanup, comments, stub cleanup
# ToDo: dynamic adding/removing children as a multi type attribute with indexing

__VERSION__ = 1.0
__PROJECT__ = 'Marvel'


def lazy_property(fn):
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


class MetaNode(object):
    def __init__(self, name='_metanode', create=True, metaChildren=()):
        self.name = name
        self.create = create
        self.metaChildren = metaChildren

        if self.create:
            self.create_node()

        if self.metaChildren:
            self.set_metaChildren(self.metaChildren)

    def __repr__(self):
        return self.name

    def create_node(self):
        if cmds.objExists(self.name):
            cmds.error('Meta node already exists: %s' % self.name)
            return None

        cmds.createNode('network', name=self.name)
        cmds.addAttr(self.name, longName='metaType', dataType='string', keyable=False)
        cmds.addAttr(self.name, longName='version', attributeType='float', defaultValue=0, keyable=False)
        cmds.addAttr(self.name, longName='project', dataType='string', keyable=False)
        cmds.addAttr(self.name, longName='metaParent', attributeType='message', readable=False, writable=True)
        cmds.addAttr(self.name, longName='metaChildren', attributeType='message', multi=True)
        # cmds.addAttr(self.name, longName='metaChildren', attributeType='message')

        self.metaType = 'metaNode'
        self.version = __VERSION__
        self.project = __PROJECT__

    def connect_attr_to_obj(self, source_attr, obj, target_attr):
        if cmds.objExists(obj):
            if not apiUtils.get_plug(obj, target_attr):
                cmds.warning('Creating attribute: %s.%s' % (obj, target_attr))
                cmds.addAttr(obj, longName=target_attr, attributeType='message', keyable=False)
            try:
                cmds.connectAttr('%s.%s' % (self.name, source_attr), '%s.%s' % (obj, target_attr), force=True)
            except RuntimeError:
                cmds.warning('Attribute %s.%s already connected.' % (obj, target_attr))

    def get_connected_obj(self):
        pass

    def add_attr(self, attr, attr_type='message', multi=False):
        if attr_type == 'string':
            cmds.addAttr(self.name, longName=attr, dataType='string')
            return

        cmds.addAttr(self.name, longName=attr, attributeType=attr_type, multi=multi)

    def get_attr(self, attr):
        return cmds.getAttr('%s.%s' % (self.name, attr))

    def get_attrs(self):
        return apiUtils.get_extra_attrs(self.name)

    @property
    def metaParent(self):
        try:
            return cmds.listConnections('%s.metaParent' % self.name)[0]
        except (TypeError, IndexError):
            return None

    @metaParent.setter
    def metaParent(self, metaParent):
        try:
            cmds.connectAttr('%s.metaChildren' % metaParent, '%s.metaParent' % self.name, force=True)
        except RuntimeError:
            cmds.warning('%s is already connected to %s' % (metaParent, self.name))

    @property
    def metaType(self):
        return 'metaNode'

    @metaType.getter
    def metaType(self):
        if not apiUtils.get_plug(self.name, 'metaType'):
            return None
        return cmds.getAttr('%s.metaType' % self.name)

    @metaType.setter
    def metaType(self, metaType):
        if not apiUtils.get_plug(self.name, 'metaType'):
                metaType = None
        cmds.setAttr('%s.metaType' % self.name, lock=False)
        cmds.setAttr('%s.metaType' % self.name, metaType, type='string')
        cmds.setAttr('%s.metaType' % self.name, lock=True)

    @property
    def project(self):
        return __PROJECT__

    @project.getter
    def project(self):
        if not apiUtils.get_plug(self.name, 'project'):
            return None
        return cmds.getAttr('%s.project' % self.name)

    @project.setter
    def project(self, project):
        cmds.setAttr('%s.project' % self.name, lock=False)
        cmds.setAttr('%s.project' % self.name, project, type='string')
        cmds.setAttr('%s.project' % self.name, lock=True)

    @property
    def version(self):
        return __VERSION__

    @version.getter
    def version(self):
        if not apiUtils.get_plug(self.name, 'version'):
            return None
        return cmds.getAttr('%s.version' % self.name)

    @version.setter
    def version(self, version):
        cmds.setAttr('%s.version' % self.name, lock=False)
        cmds.setAttr('%s.version' % self.name, version)
        cmds.setAttr('%s.version' % self.name, lock=True)

    def get_metaChildren(self):
        self.metaChildren = cmds.listConnections('%s.metaChildren' % self.name)
        if self.metaChildren:
            return self.metaChildren
        return None

    def set_metaChildren(self, metaChildren, index=None):
        """
        :param metaChildren: type(str, list) metaChildren nodes to connect to this node via parent/children connection
        :return: None
        """
        if not metaChildren:
            return None

        if type(metaChildren) is str:
            metaChildren = [metaChildren]

        for metaChild in metaChildren:
            print 'Connecting %s ----> %s' % (self.name, metaChild)
            try:
                cmds.connectAttr('%s.metaChildren' % self.name, '%s.metaParent' % metaChild, force=True)
                self.metaChildren = self.get_metaChildren()
            except RuntimeError:
                cmds.warning('%s is already connected to %s' % (self.name, metaChild))
                continue

    def get_metaRoot(self, node=None):
        """
        recursively trace up the connection chain until terminated at the root
        :return: type(metaNode) base root meta node
        """
        if not node:
            node = self.name

        # base case - node has no metaParent
        if not cmds.listConnections('%s.metaParent' % node):
            return node
        # recursive case - get node's metaParent, run function again to get parent node's metaParent until base case
        else:
            parent = cmds.listConnections('%s.metaParent' % node)[0]
            return self.get_metaRoot(parent)

    def get_metaChildren_of_type(self, metaType):
        """
        :param type: type(str) meta node metaType
        :return: type(list) of all meta node metaChildren of this metaType via parent/children connections
        """
        children_of_type = []

        for child in self.get_metaChildren():
            if cmds.attributeQuery('metaType', node=child, exists=True):
                if cmds.getAttr('%s.metaType' % child) == metaType:
                    children_of_type.append(child)

        if not children_of_type:
            return None

        return children_of_type

    def get_all_metaChildren(self):
        """
        :return: type(list) iterative search of all nodes below this meta node via parent/children connections
        """
        pass

    def get_all_connections(self, recursive=False):
        """
        :param recursive: type(bool) recursive search option, default False
        :return: type(list) all meta nodes and plugs connected to this meta node
        """
        pass

    def get_single_connection(self, node, attr):
        """
        :param node:
        :param attr:
        :return: type(metaNode) specific node and plug connected to this node
        """
        pass

'''
import sys
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

if 'C:\Users\Tom Banker\github\AutoRigger' not in sys.path:
    sys.path.append('C:\Users\Tom Banker\github\AutoRigger')

from src.rigLib.base import transform
from src.rigLib.base import joint
from src.rigLib.base import locator
from src.rigLib.base import control
from src.utils import apiUtils
from src.rigLib.blocks import fkIkChain
from src.rigLib.blocks import fkChain
from src.rigLib.metaNodes import metaNode

reload(transform)
reload(joint)
reload(control)
reload(apiUtils)
reload(fkIkChain)
reload(fkChain)
reload(metaNode)

cmds.file(new=1, force=1)

meta_child1 = metaNode.MetaNode('meta_child1')
meta_child2 = metaNode.MetaNode('meta_child2')
meta_child3 = metaNode.MetaNode('meta_child3')
meta_parent1 = metaNode.MetaNode('meta_parent1', metaChildren=meta_child1.name)

meta_child2.metaParent = meta_parent1
meta_child2.set_metaChildren(meta_child3.name)

print meta_child1.metaParent
print meta_child2.metaParent
print meta_child3.metaParent
print meta_parent1.metaParent

print meta_child1.get_metaChildren()
print meta_child2.get_metaChildren()
print meta_child3.get_metaChildren()
print meta_parent1.get_metaChildren()
'''









