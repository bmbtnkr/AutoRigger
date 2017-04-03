"""
Module for creating a Maya joint object
"""
import maya.cmds as cmds
import os
from src.rigLib.metaNodes import metaNode
from src.utils import apiUtils
reload(metaNode)
reload(apiUtils)

# __VERSION__ = 0.11

# todo: self.shape not getting set correctly during init

class MetaMesh(metaNode.MetaNode):
    def __init__(self, mesh=None, shader=None, texture=None, texturePath=None, skinCluster=None, *args, **kwargs):
        self.mesh = mesh
        self.shader = shader
        self.texture = texture
        self.texturePath = texturePath
        self.skinCluster = skinCluster
        super(MetaMesh, self).__init__(*args, **kwargs)
        # self.version = __VERSION__

        self.shape = None
        self.file = None

        self.set_metaType('metaMesh')
        self.set_version(self.version)

    def create_node(self):
        super(MetaMesh, self).create_node()

        if not cmds.objExists(self.mesh):
            cmds.warning('Mesh name does not exist: %s' % self.mesh)
            cmds.delete(self.name)
            return None

        self.add_attr('metaMesh_transform')
        self.add_attr('metaMesh_shape')
        self.add_attr('metaMesh_shader')
        self.add_attr('metaMesh_texture')
        self.add_attr('metaMesh_texturePath', attr_type='string')
        self.add_attr('metaMesh_skinCluster')
        self.add_attr('metaMesh_file', attr_type='string')

        self.shape = apiUtils.get_shapeNodes(self.mesh)[0]
        self.file = self.set_file()
        self.skinCluster = self.set_skinCluster()

        self.connect_attr_to_obj('metaMesh_transform', self.mesh, 'metaParent')
        self.connect_attr_to_obj('metaMesh_shape', self.shape, 'metaParent')
        self.connect_attr_to_obj('metaMesh_skinCluster', self.skinCluster, 'metaParent')
        self.connect_attr_to_obj('metaMesh_shader', self.set_shader(), 'metaParent')
        self.connect_attr_to_obj('metaMesh_texture', self.set_texture(), 'metaParent')

        self.set_texturePath()

    # def update_meshMetaAttrs(self):
    #     self.set_metaType(self.metaType)
    #     self.set_version(self.version)
    #     self.shape = apiUtils.get_shapeNodes(self.mesh)[0]
    #     self.file = self.set_file()
    #     self.skinCluster = self.set_skinCluster()
    #     self.connect_attr_to_obj('metaMesh_transform', self.mesh, 'metaParent')
    #     self.connect_attr_to_obj('metaMesh_shape', self.shape, 'metaParent')
    #     self.connect_attr_to_obj('metaMesh_skinCluster', self.set_skinCluster(), 'metaParent')
    #     self.connect_attr_to_obj('metaMesh_shader', self.set_shader(), 'metaParent')
    #     self.connect_attr_to_obj('metaMesh_texture', self.set_texture(), 'metaParent')
    #     self.set_texturePath()

    def get_shapeNodes(self):
        if self.mesh:
            return apiUtils.get_shapeNodes(self.mesh)
        return None

    def get_skinCluster(self):
        return self.skinCluster

    def set_skinCluster(self):
        if not self.mesh or not self.shape:
            return None

        self.skinCluster = apiUtils.get_skinCluster(self.shape)
        return self.skinCluster

    def get_shader(self):
        return self.shader

    def set_shader(self):
        self.shader = apiUtils.get_shaders(self.shape).name()
        return self.shader

    def get_texture(self):
        return self.texture

    def set_texture(self):
        self.texture = apiUtils.get_texture(self.shape)
        if not self.texture:
            return None
        return self.texture.name()

    def get_texturePath(self):
        return self.texturePath

    def set_texturePath(self):
        self.texturePath = str(apiUtils.get_texturePath(self.shape))
        cmds.setAttr('%s.metaMesh_texturePath' % self.name, lock=False)
        cmds.setAttr('%s.metaMesh_texturePath' % self.name, self.texturePath, type='string', lock=True)
        return self.texturePath

    def get_file(self):
        return self.file

    def set_file(self):
        # make this a method in scene utils
        current_path = cmds.file(sceneName=True, q=1)


        try:
            rig_file = current_path.rpartition('/')[-1]
            rig_folder = current_path.split('/')[-2]

            model_file = rig_file.replace('_rig', '_mesh')
            model_folder = rig_folder.replace('rig', 'model')
            model_path = current_path.replace(rig_file, model_file).replace(rig_folder, model_folder)

            if os.path.exists(model_path):
                cmds.setAttr('%s.metaMesh_file' % self.name, lock=False)
                cmds.setAttr('%s.metaMesh_file' % self.name, model_path, type='string', lock=True)
                return model_path

        except IndexError:
            cmds.setAttr('%s.metaMesh_file' % self.name, lock=False)
            cmds.setAttr('%s.metaMesh_file' % self.name, 'None', type='string', lock=True)
            cmds.warning('Model file: %s not found' % self.mesh)
            return None


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