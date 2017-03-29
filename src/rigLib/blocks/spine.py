"""
Module for creating an AutoRigger fk/ik chain component

FK/IK chain component - Animateable component
Requires a joint chain length of 3
Contains two sets of controls for animating in FK and IK
Control Flags: FK[...], IK, Pole Vector, FK/IK Switch
"""

import maya.cmds as cmds
from src.rigLib.base import transform
from src.rigLib.base import control
from src.rigLib.base import joint


class Spine(object):
    def __init__(self, joints=()):
        self.joints = joints
        self.hipCtrl = None
        self.chestCtrl = None

    def create_block(self):
        hipSplineJnt = joint.Joint(name='hip_spline_jnt', translateTo=self.joints[0], rotateTo=self.joints[0])
        chestSplineJnt = joint.Joint(name='chest_spline_jnt', translateTo=self.joints[-1], rotateTo=self.joints[-1])
        cmds.makeIdentity(hipSplineJnt, apply=True)
        cmds.makeIdentity(chestSplineJnt, apply=True)

        splineIkHandle = cmds.ikHandle(name='%s_ikHandle_sp' % hipSplineJnt.name, startJoint=self.joints[0],
                                       endEffector=self.joints[-1], solver='ikSplineSolver')

        cmds.rename(splineIkHandle[1], '%s_eff' % self.joints[-1])

        cmds.skinCluster(hipSplineJnt.name, chestSplineJnt.name, splineIkHandle[2])
        cmds.rename(splineIkHandle[2], '%s_crv' % hipSplineJnt.name)

        self.hipCtrl = control.Control(name=hipSplineJnt.name.replace('jnt', 'ctrl'), normal=(1, 0, 0),
                                       translateTo=hipSplineJnt, rotateTo=hipSplineJnt)
        self.hipCtrl.create_null_grps()
        self.hipCtrl.nullGrp.set_scale((4, 4, 4))
        cmds.makeIdentity(self.hipCtrl.nullGrp, scale=True, apply=True)
        cmds.parentConstraint(self.hipCtrl.name, hipSplineJnt.name)

        self.chestCtrl = control.Control(name=chestSplineJnt.name.replace('jnt', 'ctrl'), normal=(1, 0, 0),
                                         translateTo=chestSplineJnt, rotateTo=chestSplineJnt)
        self.chestCtrl.create_null_grps()
        self.chestCtrl.nullGrp.set_scale((4, 4, 4))
        cmds.makeIdentity(self.chestCtrl.nullGrp, scale=True, apply=True)
        cmds.parentConstraint(self.chestCtrl.name, chestSplineJnt.name)

        # setup advance twist options
        cmds.setAttr('%s.dTwistControlEnable' % splineIkHandle[0], 1)
        cmds.setAttr('%s.dWorldUpType' % splineIkHandle[0], 4)
        cmds.connectAttr('%s.worldMatrix[0]' % hipSplineJnt, '%s.dWorldUpMatrix' % splineIkHandle[0])
        cmds.connectAttr('%s.worldMatrix[0]' % chestSplineJnt, '%s.dWorldUpMatrixEnd' % splineIkHandle[0])

# import maya.cmds as cmds
# import maya.OpenMaya as OpenMaya
#
# if 'C:\Users\Tom Banker\github\AutoRigger' not in sys.path:
#     sys.path.append('C:\Users\Tom Banker\github\AutoRigger')
#
# from src.rigLib.base import transform
# from src.rigLib.base import joint
# from src.rigLib.base import locator
# from src.rigLib.base import control
# from src.utils import apiUtils
# from src.rigLib.blocks import fkIkChain
# from src.rigLib.blocks import foot
# from src.rigLib.blocks import spine
#
# reload(transform)
# reload(fkIkChain)
# reload(joint)
# reload(locator)
# reload(apiUtils)
# reload(fkIkChain)
# reload(foot)
# reload(spine)
#
# legJnts = ('jt_l_thigh_bind', 'jt_l_knee_bind', 'jt_l_foot_bind')
# # legRig = fkIkChain.FkIkChain(legJnts)
# # legRig.create_block()
#
# footJnts = ('jt_l_foot_bind', 'jt_l_ball_bind', 'jt_l_toe_bind')
# heelPiv = 'heelPiv'
# insidePiv = 'insidePiv'
# outsidePiv = 'outsidePiv'
#
# # footRig = foot.Foot(joints=footJnts, legRig=legRig, heelPiv=heelPiv, insidePiv=insidePiv, outsidePiv=outsidePiv)
# # footRig.create_block()
#
# spineJnts = ['spine1_result_jnt', 'spine2_result_jnt', 'spine3_result_jnt',
#              'spine4_result_jnt' 'spine5_result_jnt', 'spine6_result_jnt',
#              'spine7_result_jnt']
#
# spineRig = spine.Spine(joints=spineJnts)
#
# spineRig.create_block()


