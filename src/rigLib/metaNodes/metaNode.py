"""
Module for creating an AutoRigger meta data node
"""

import maya.cmds as cmds
from src.utils import apiUtils

# ToDo: code cleanup, comments, stub cleanup

class MetaNode(object):
    def __init__(self, name='_metanode', create=True, metaParent=None, metaType='_metatype', version=0.0, metaChildren=()):
        self.name = name
        self.create = create
        self.metaParent = metaParent
        self.metaType = metaType
        self.version = version
        self.metaChildren = metaChildren

        if self.create:
            self.create_node()

    def __repr__(self):
        return self.name

    def create_node(self):
        cmds.createNode('network', name=self.name)
        cmds.addAttr(self.name, longName='metaType', dataType='string')
        cmds.addAttr(self.name, longName='version', attributeType='float', defaultValue=self.version, keyable=False)
        cmds.addAttr(self.name, longName='metaParent', attributeType='message', readable=False)
        cmds.addAttr(self.name, longName='metaChildren', attributeType='message', writable=False)

        self.set_type(self.metaType)
        self.set_metaParent(self.metaParent)
        self.set_metaChildren(self.metaChildren)

    def add_attr(self, attr):
        pass

    def get_attr(self, attr):
        pass

    def get_attrs(self):
        return apiUtils.get_extra_attrs(self.name)

    def get_metaParent(self):
        self.metaParent = cmds.listConnections('%s.metaParent' % self.name)
        if self.metaParent:
            return self.metaParent[0]
        return None

    def set_metaParent(self, metaParent):
        if not metaParent:
            return None

        try:
            cmds.connectAttr('%s.metaChildren' % metaParent, '%s.metaParent' % self.name, force=True)
            self.metaParent = self.get_metaParent()
        except RuntimeError:
            cmds.warning('%s is already connected to %s' % (metaParent, self.name))
            return None

    def get_type(self):
        return self.metaType

    def set_type(self, metaType):
        cmds.setAttr('%s.metaType' % self.name, metaType, type='string')

    def get_metaChildren(self):
        self.metaChildren = cmds.listConnections('%s.metaChildren' % self.name)
        if self.metaChildren:
            return self.metaChildren
        return None

    def set_metaChildren(self, metaChildren):
        """
        :param metaChildren: type(str, list) metaChildren nodes to connect to this node via parent/children connection
        :return: None
        """
        if not metaChildren:
            return None

        if type(metaChildren) is str:
            try:
                cmds.connectAttr('%s.metaChildren' % self.name, '%s.metaParent' % metaChildren, force=True)
                self.metaChildren = self.get_metaChildren()
            except RuntimeError:
                cmds.warning('%s is already connected to %s' % (self.name, metaChildren))
                return None

        elif type(metaChildren) is list and len(metaChildren) > 1:
            for metaChild in metaChildren:
                try:
                    cmds.connectAttr('%s.metaChildren' % self.name, '%s.metaParent' % metaChild, force=True)
                    self.metaChildren = self.get_metaChildren()
                except RuntimeError:
                    cmds.warning('%s is already connected to %s' % (self.name, metaChild))
                    return None

    def get_metaRoot(self):
        """
        recursively trace up the connection chain until terminatated at the root
        :return: type(metaNode) base root meta node
        """
        pass

    def get_metaChildren_of_type(self, type):
        """
        :param type: type(str) meta node metaType
        :return: type(list) of all meta node metaChildren of this metaType via parent/children connections
        """
        pass

    def get_all_metaChildren(self):
        """
        :return: type(list) recusive search of all nodes below this meta node via parent/children connections
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
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

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

legJnts = ('jt_thigh_bind', 'jt_knee_bind', 'jt_ankle_bind')

test = fkIkChain.FkIkChain(legJnts)
#test.create_block()

#print test.midJnt.get_translation()

#test2 = fkChain.FkChain(legJnts)
#print test2.create_joints(legJnts)

def try_del(node):
    try:
        cmds.delete(node)
    except:
        pass

try_del('foo_meta')
try_del('foo_meta2')
try_del('foo_meta3')

foo_meta2 = metaNode.MetaNode('test_node_child1', version=2.3)
foo_meta3 = metaNode.MetaNode('test_node_child2')

foo_meta = metaNode.MetaNode('test_node1', metaType='meta_foobar_node',
 metaChildren=foo_meta2.name)

print foo_meta.get_metaChildren()
print foo_meta.get_metaParent()
print foo_meta2.get_metaParent()

#foo_meta.set_metaChildren(foo_meta3.name)
#foo_meta3.set_metaParent(foo_meta.name)
'''









