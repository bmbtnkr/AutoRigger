"""
Module for creating a metadata rig object
"""
import maya.cmds as cmds
import os
from src.rigLib.metaNodes import metaNode
from src.utils import apiUtils
reload(metaNode)
reload(apiUtils)

# __VERSION__ = 0.11

# ToDo: store zero pose - in biped compound
# ToDo: pose mirroring per frame or time-line / ranges
# ToDo: store poses in an attr
# ToDo: store mirror data?
# ToDo: store attribute settings and values in json to revert to bind pose state
# ToDo: allow mass hierarchy or single node attribute locking / hiding


class MetaRig(metaNode.MetaNode):
    """some doc info"""
    def __init__(self, rootJnt=None, rigType='metaRig_root', *args, **kwargs):
        self.rootJnt = rootJnt
        self.rigType = rigType
        super(MetaRig, self).__init__(*args, **kwargs)

        self.set_metaType('metaRig')
        self.set_version(self.version)

    def create_node(self):
        super(MetaRig, self).create_node()

        if not cmds.objExists(self.rootJnt):
            cmds.warning('Root joint nodes not exist: %s' % self.rootJnt)
            cmds.delete(self.name)
            return None

        self.add_attr('metaRig_type', attr_type='string')
        self.set_rigType()

        self.add_attr('metaRig_rootJnt')
        self.connect_attr_to_obj('metaRig_rootJnt', self.rootJnt, 'metaParent')

    def get_rootJnt(self):
        return self.rootJnt

    def set_rootJnt(self, rootJnt):
        if cmds.objExists(rootJnt):
            self.rootJnt = rootJnt
            return self.rootJnt
        return None

    def set_rigType(self, rigType=None):
        cmds.setAttr('%s.metaRig_type' % self.name, lock=False)
        if rigType:
            self.rigType = rigType
            cmds.setAttr('%s.metaRig_type' % self.name, self.rigType, type='string')
            cmds.setAttr('%s.metaRig_type' % self.name, lock=True)
            return self.rigType
        elif self.rigType:
            cmds.setAttr('%s.metaRig_type' % self.name, self.rigType, type='string')
            cmds.setAttr('%s.metaRig_type' % self.name, lock=True)
            return self.rigType
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
from src.rigLib.metaNodes import metaRig

reload(transform)
reload(joint)
reload(control)
reload(apiUtils)
reload(fkIkChain)
reload(fkChain)
reload(metaNode)
reload(metaMesh)
reload(metaRig)

meta_mesh1 = metaMesh.MetaMesh(name='meta_mesh1', mesh='elsaMech_mesh')
meta_rig1 = metaRig.MetaRig(name='meta_rig1', rootJnt='jt_all_bind', metaChildren=meta_mesh1.name)
"""