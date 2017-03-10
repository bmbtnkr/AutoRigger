"""
Module for creating a Maya joint object
"""
import maya.cmds as cmds
import os
from src.rigLib.metaNodes import metaNode
from src.utils import apiUtils
reload(metaNode)
reload(apiUtils)


class MetaMesh(metaNode.MetaNode):
    def __init__(self, mesh=None, textures=(), skinCluster=None, *args, **kwargs):
        self.mesh = mesh
        self.textures = textures
        self.skinCluster = skinCluster
        super(MetaMesh, self).__init__(*args, **kwargs)

        if self.create:
            self.create_meshMetaNode()

    def create_meshMetaNode(self):
        self.set_metaType('metaMesh')
        self.add_attr('metaMesh_transform')
        self.add_attr('metaMesh_shape')
        self.add_attr('metaMesh_shaders', multi=True)
        self.add_attr('metaMesh_textures', multi=True)
        self.add_attr(attr='metaMesh_skinCluster')
        self.add_attr('metaMesh_file', attr_type='string')

        self.connect_attr_to_obj('metaMesh_transform', self.mesh, 'metaMesh_transform')
        self.connect_attr_to_obj('metaMesh_shape', apiUtils.get_shapeNodes(self.mesh)[0], 'metaMesh_shape')

    def get_shapeNodes(self):
        print 'shapeNodes:'  # wip

    def get_skinCluster(self):
        pass

    def get_shaders(self):
        pass

    def get_textures(self):
        pass

    def set_file(self):
        # make this a method in scene utils
        current_path = cmds.file(sceneName=True, q=1)
        rig_file = current_path.rpartition('/')[-1]
        rig_folder = current_path.split('/')[-2]

        model_file = rig_file.replace('_rig', '_mesh')
        model_folder = rig_folder.replace('rig', 'model')
        model_path = current_path.replace(rig_file, model_file).replace(rig_folder, model_folder)

        if os.path.exists(model_path):
            cmds.setAttr('%s.metaMesh_file' % self.name, model_path, type='string')
            return model_path
        else:
            cmds.setAttr('%s.metaMesh_file' % self.name, 'MODEL_FILE_NOT_FOUND', type='string')
            cmds.warning('Model file: %s not found' % model_path)

    def get_file(self):
        pass

"""
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
from src.rigLib.metaNodes import metaMesh

reload(transform)
reload(joint)
reload(control)
reload(apiUtils)
reload(fkIkChain)
reload(fkChain)
reload(metaNode)
reload(metaMesh)

#cmds.file(new=1, force=1)

meta_child1 = metaNode.MetaNode('meta_child1', version=2.3)
meta_child2 = metaNode.MetaNode('meta_child2')
meta_child3 = metaNode.MetaNode('meta_child3')
meta_parent1 = metaNode.MetaNode('meta_parent1', metaType='metaType_parentType', metaChildren=meta_child1.name)

meta_child2.set_metaParent(meta_parent1.name)
meta_child2.set_metaChildren(meta_child3.name)

print meta_child1.get_metaParent()
print meta_child2.get_metaParent()
print meta_child3.get_metaParent()
print meta_parent1.get_metaParent()

print meta_child1.get_metaChildren()
print meta_child2.get_metaChildren()
print meta_child3.get_metaChildren()
print meta_parent1.get_metaChildren()

meta_mesh1 = metaMesh.MetaMesh(name='meta_mesh1', mesh='elsaMech_mesh')

#meta_mesh1.connect_attr_to_obj('metaMesh_transform', 'elsaMech_mesh', 'metaMesh_transform')

"""