"""
Module for creating an AutoRigger fk/ik chain component

FK/IK chain component - Animateable component
Requires a joint chain length of 3
Contains two sets of controls for animating in FK and IK
Control Flags: FK[...], IK, Pole Vector, FK/IK Switch
"""

# create an fk/ik chain metadata node first

# needs fk joints x3
# ik joints x3

# pole vector transform?
#

# fk/ik switch attribute - in metadata node???


# tagging arm joints:
# chain root = "arm"
# chain end = "arm"
# chain terminator = "arm"

# Features
# ToDo: make this work with any number of middle joints
# ToDo: add bendy/rotate joints in between each bone
# ToDo: make sure hide attrs is working - done
# ToDo: finish ik stretch setup - done
# ToDo: setup blend color node for result chain, but for translate as well - done
# ToDo: setup ik knee pinning - done
# ToDo: connect ik handle twist into new ik ctrl knee twist attribute - done
# ToDo: add addtional tweak offset control to knee joint
# ToDo: add soft Ik solver

# Cleanup
# ToDo: remove dist_ctrl_l_foot_ik_mid_stretch - done
# ToDo: remove dist_ctrl_l_foot_ik_end_stretch - done
# ToDo: remove jt_l_thigh_ik_pos_null - done
# ToDo: connect rootIkJnt to kneePin and stretch matrix1 - done
# ToDo: knee pinning solve cleanup: when stretch is on use the stretch distance in knee pinning mult
#                                   when stretch is off, use root to end ik jnt distance in knee pinning mult

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import math
from src.rigLib.base import transform
from src.rigLib.base import control
from src.rigLib.base import joint
from src.utils import apiUtils


class FkIkChain(object):
    def __init__(self, joints=(), rootJnt=None, midJnt=None, endJnt=None, ikCtrl=None, ikPvCtrl=None, ikTweakCtrl=None,
                 fkRootCtrl=None, fkMidCtrl=None, fkEndCtrl=None, fkIkSwitch=None):
        self.joints = joints

        self.rootJnt = rootJnt
        self.midJnt = midJnt
        self.endJnt = endJnt

        self.poleVector = None
        self.ikHandle = None

        self.ikCtrl = ikCtrl
        self.ikPvCtrl = ikPvCtrl
        self.ikTweakCtrl = ikTweakCtrl

        self.fkRootCtrl = fkRootCtrl
        self.fkMidCtrl = fkMidCtrl
        self.fkEndCtrl = fkEndCtrl

        self.fkIkSwitch = fkIkSwitch

        self.ikCtrls = (self.ikCtrl, self.ikPvCtrl, self.ikTweakCtrl)
        self.fkCtrls = (self.fkRootCtrl, self.fkMidCtrl, self.fkEndCtrl)

    def create_block(self):
        if len(self.joints) < 3:
            cmds.warning('Could not build FkIkChain block, not enough joints', self.joints)
            return False

        # create joints
        rootJntBind = joint.Joint(name=self.joints[0], create=False)
        midJntBind = joint.Joint(name=self.joints[1], create=False)
        endJntBind = joint.Joint(name=self.joints[2], create=False)

        self.rootJnt = joint.Joint(name=rootJntBind.name.replace('bind', 'result'),
                                   translateTo=rootJntBind, rotateTo=rootJntBind,
                                   jointOrient=rootJntBind.get_joint_orient(), jointTag='ikfkChain_root')
        self.midJnt = joint.Joint(name=midJntBind.name.replace('bind', 'result'),
                                  translateTo=midJntBind, rotateTo=midJntBind,
                                  jointOrient=midJntBind.get_joint_orient(), jointTag='ikfkChain_mid', parent=self.rootJnt)
        self.endJnt = joint.Joint(name=endJntBind.name.replace('bind', 'result'),
                                  translateTo=endJntBind, rotateTo=endJntBind,
                                  jointOrient=endJntBind.get_joint_orient(), jointTag='ikfkChain_end', parent=self.midJnt)
        cmds.makeIdentity(self.rootJnt, apply=True)


        self.rootJntFk = joint.Joint(name=self.rootJnt.name.replace('result', 'fk'), translateTo=self.rootJnt, rotateTo=self.rootJnt)
        self.midJntFk = joint.Joint(name=self.midJnt.name.replace('result', 'fk'), translateTo=self.midJnt, rotateTo=self.midJnt, parent=self.rootJntFk)
        self.endJntFk = joint.Joint(name=self.endJnt.name.replace('result', 'fk'), translateTo=self.endJnt, rotateTo=self.endJnt, parent=self.midJntFk)
        cmds.makeIdentity(self.rootJntFk, apply=True)

        self.rootJntIk = joint.Joint(name=self.rootJnt.name.replace('result', 'ik'), translateTo=self.rootJnt, rotateTo=self.rootJnt)
        self.midJntIk = joint.Joint(name=self.midJnt.name.replace('result', 'ik'), translateTo=self.midJnt, rotateTo=self.midJnt, parent=self.rootJntIk)
        self.endJntIk = joint.Joint(name=self.endJnt.name.replace('result', 'ik'), translateTo=self.endJnt, rotateTo=self.endJnt, parent=self.midJntIk)
        cmds.makeIdentity(self.rootJntIk, apply=True)

        # create fk ctrls
        self.fkRootCtrl = control.Control(name=self.rootJnt.name.replace('jt', 'ctrl').replace('result', 'fk'),
                                          translateTo=self.rootJnt, rotateTo=self.rootJnt, normal=(1, 0, 0))

        self.fkMidCtrl = control.Control(name=self.midJnt.name.replace('jt', 'ctrl').replace('result', 'fk'),
                                         translateTo=self.midJnt, rotateTo=self.midJnt, normal=(1, 0, 0))

        self.fkEndCtrl = control.Control(name=self.endJnt.name.replace('jt', 'ctrl').replace('result', 'fk'),
                                         translateTo=self.endJnt, rotateTo=self.endJnt)

        self.fkRootCtrl.create_null_grps()
        self.fkMidCtrl.create_null_grps()
        self.fkEndCtrl.create_null_grps()

        self.fkMidCtrl.nullGrp.set_parent(self.fkRootCtrl.name)
        self.fkEndCtrl.nullGrp.set_parent(self.fkMidCtrl.name)

        self.fkRootCtrl.lockChannels(('t', 's', 'v'))
        self.fkMidCtrl.lockChannels(('t', 's', 'v'))
        self.fkEndCtrl.lockChannels(('t', 's', 'v'))

        self.fkRootCtrl.hideChannels(('t', 's', 'v'))
        self.fkMidCtrl.hideChannels(('t', 's', 'v'))
        self.fkEndCtrl.hideChannels(('t', 's', 'v'))

        fkRootOrientConstraint = cmds.orientConstraint(self.fkRootCtrl.name, self.rootJntFk)[0]
        fkMidOrientConstraint = cmds.orientConstraint(self.fkMidCtrl.name, self.midJntFk)[0]
        fkEndOrientConstraint = cmds.orientConstraint(self.fkEndCtrl.name, self.endJntFk)[0]

        # create ik ctrls
        self.ikCtrl = control.Control(name=self.endJnt.name.replace('jt', 'ctrl').replace('result', 'ik'),
                                      translateTo=self.endJnt)
        self.ikCtrl.create_null_grps()
        self.ikCtrl.lockChannels(('r', 's', 'v'))
        self.ikCtrl.hideChannels(('r', 's', 'v'))
        self.ikCtrl.nullGrp.set_scale((2,2,2))

        cmds.addAttr(self.ikCtrl.name, longName='ikBlend', attributeType='float', defaultValue=1, minValue=0, maxValue=1, keyable=True)
        cmds.addAttr(self.ikCtrl.name, longName='stretch', attributeType='float', defaultValue=0, minValue=0, maxValue=1, keyable=True)
        cmds.addAttr(self.ikCtrl.name, longName='kneePin', attributeType='float', defaultValue=0, minValue=0, maxValue=1, keyable=True)
        cmds.addAttr(self.ikCtrl.name, longName='twist', attributeType='float', defaultValue=0, keyable=True)

        self.ikHandle = cmds.ikHandle(name='%s_ikHandle' % self.ikCtrl.name, startJoint=self.rootJntIk, endEffector=self.endJntIk,
                                      solver='ikRPsolver')

        cmds.rename(self.ikHandle[1], '%s_eff' % self.endJntIk)
        self.ikHandle = transform.Transform(name=self.ikHandle[0], create=False)
        ikHandleParentConstraint = cmds.parentConstraint(self.ikCtrl.name, self.ikHandle.name)[0]
        cmds.connectAttr('%s.twist' % self.ikCtrl.name, '%s.twist' % self.ikHandle.name)

        # create pv ctrl
        self.ikPvCtrl = control.Control(name=self.midJnt.name.replace('jt', 'ctrl').replace('result', 'pv'),
                                        translate=self.set_pole_vector()[0], rotate=self.set_pole_vector()[1])
        self.ikPvCtrl.create_null_grps()
        cmds.poleVectorConstraint(self.ikPvCtrl.name, self.ikHandle.name)
        self.ikPvCtrl.lockChannels(('r', 's', 'v'))
        self.ikPvCtrl.hideChannels(('r', 's', 'v'))

        # Setup stretchy ik
        # rootJntIkPosNull = transform.Transform(name='%s_pos_null' % self.rootJntIk, translateTo=self.rootJnt)

        ikStretchMidDistance = cmds.createNode('distanceBetween', name='dist_%s_mid_stretch' % self.ikCtrl.name)
        cmds.connectAttr('%s.worldMatrix[0]' % self.rootJntIk, '%s.inMatrix1' % ikStretchMidDistance)
        cmds.connectAttr('%s.worldMatrix[0]' % self.midJntIk, '%s.inMatrix2' % ikStretchMidDistance)

        ikStretchEndDistance = cmds.createNode('distanceBetween', name='dist_%s_end_stretch' % self.ikCtrl.name)
        cmds.connectAttr('%s.worldMatrix[0]' % self.midJntIk, '%s.inMatrix1' % ikStretchEndDistance)
        cmds.connectAttr('%s.worldMatrix[0]' % self.endJntIk, '%s.inMatrix2' % ikStretchEndDistance)

        ikStretchCtrlDistance = cmds.createNode('distanceBetween', name='dist_%s_ctrl_stretch' % self.ikCtrl.name)
        cmds.connectAttr('%s.worldMatrix[0]' % self.rootJntIk, '%s.inMatrix1' % ikStretchCtrlDistance)
        cmds.connectAttr('%s.worldMatrix[0]' % self.ikCtrl.name, '%s.inMatrix2' % ikStretchCtrlDistance)

        ikStretchFactorMult = cmds.createNode('multiplyDivide', name='div_%s_stretch' % self.ikCtrl.name)
        cmds.setAttr('%s.operation' % ikStretchFactorMult, 2)
        cmds.connectAttr('%s.distance' % ikStretchCtrlDistance, '%s.input1X' % ikStretchFactorMult)
        ikStretchSumDistance = float(cmds.getAttr('%s.distance' % ikStretchMidDistance) + cmds.getAttr('%s.distance' % ikStretchEndDistance))
        cmds.setAttr('%s.input2X' % ikStretchFactorMult, ikStretchSumDistance)

        ikStretchFactorCond = cmds.createNode('condition', name='cond_%s_stretch' % self.ikCtrl.name)
        cmds.setAttr('%s.operation' % ikStretchFactorCond, 2)
        cmds.connectAttr('%s.distance' % ikStretchCtrlDistance, '%s.firstTerm' % ikStretchFactorCond)
        cmds.setAttr('%s.secondTerm' % ikStretchFactorCond, ikStretchSumDistance)
        cmds.connectAttr('%s.outputX' % ikStretchFactorMult, '%s.colorIfTrueR' % ikStretchFactorCond)

        ikStretchMidMult = cmds.createNode('multiplyDivide', name='mult_%s_mid_stretch' % self.ikCtrl.name)
        cmds.connectAttr('%s.outColorR' % ikStretchFactorCond, '%s.input1X' % ikStretchMidMult)
        cmds.setAttr('%s.input2X' % ikStretchMidMult, cmds.getAttr('%s.distance' % ikStretchMidDistance))

        ikStretchEndMult = cmds.createNode('multiplyDivide', name='mult_%s_end_stretch' % self.ikCtrl.name)
        cmds.connectAttr('%s.outColorR' % ikStretchFactorCond, '%s.input1X' % ikStretchEndMult)
        cmds.setAttr('%s.input2X' % ikStretchEndMult, cmds.getAttr('%s.distance' % ikStretchEndDistance))

        ikStretchAttrColor = cmds.createNode('blendColors', name='blend_%s_attr_stretch' % self.ikCtrl.name)
        cmds.connectAttr('%s.stretch' % self.ikCtrl.name, '%s.blender' % ikStretchAttrColor)
        cmds.connectAttr('%s.outputX' % ikStretchMidMult, '%s.color1R' % ikStretchAttrColor)
        cmds.connectAttr('%s.outputX' % ikStretchEndMult, '%s.color1G' % ikStretchAttrColor)
        cmds.setAttr('%s.color2R' % ikStretchAttrColor, cmds.getAttr('%s.distance' % ikStretchMidDistance))
        cmds.setAttr('%s.color2G' % ikStretchAttrColor, cmds.getAttr('%s.distance' % ikStretchEndDistance))
        cmds.delete(ikStretchMidDistance, ikStretchEndDistance)

        # Setup knee pinning
        ikKneePinRootDistance = cmds.createNode('distanceBetween', name='dist_%s_root_kneePin' % self.ikCtrl.name)
        cmds.connectAttr('%s.worldMatrix[0]' % self.rootJntIk, '%s.inMatrix1' % ikKneePinRootDistance)
        cmds.connectAttr('%s.worldMatrix[0]' % self.ikPvCtrl.name, '%s.inMatrix2' % ikKneePinRootDistance)

        ikKneePinEndDistance = cmds.createNode('distanceBetween', name='dist_%s_end_kneePin' % self.ikCtrl.name)
        cmds.connectAttr('%s.worldMatrix[0]' % self.ikPvCtrl.name, '%s.inMatrix1' % ikKneePinEndDistance)
        cmds.connectAttr('%s.worldMatrix[0]' % self.ikCtrl.name, '%s.inMatrix2' % ikKneePinEndDistance)

        ikKneePinAttrColor = cmds.createNode('blendColors', name='blend_%s_attr_kneePin' % self.ikCtrl.name)
        cmds.connectAttr('%s.kneePin' % self.ikCtrl.name, '%s.blender' % ikKneePinAttrColor)
        cmds.connectAttr('%s.distance' % ikKneePinRootDistance, '%s.color1R' % ikKneePinAttrColor)
        cmds.connectAttr('%s.distance' % ikKneePinEndDistance, '%s.color1G' % ikKneePinAttrColor)
        cmds.connectAttr('%s.outputR' % ikStretchAttrColor, '%s.color2R' % ikKneePinAttrColor)
        cmds.connectAttr('%s.outputG' % ikStretchAttrColor, '%s.color2G' % ikKneePinAttrColor)
        cmds.connectAttr('%s.outputR' % ikKneePinAttrColor, '%s.translateX' % self.midJntIk)
        cmds.connectAttr('%s.outputG' % ikKneePinAttrColor, '%s.translateX' % self.endJntIk)

        # Setup ik/fk-to-result chain blend
        thighResultPosBlendColors = cmds.createNode('blendColors', name='blend_%s_pos' % self.rootJnt.name)
        kneeResultPosBlendColors = cmds.createNode('blendColors', name='blend_%s_pos' % self.midJnt.name)
        ankleResultPosBlendColors = cmds.createNode('blendColors', name='blend_%s_pos' % self.endJnt.name)

        cmds.connectAttr('%s.translate' % self.rootJntIk, '%s.color1' % thighResultPosBlendColors)
        cmds.connectAttr('%s.translate' % self.rootJntFk, '%s.color2' % thighResultPosBlendColors)
        cmds.connectAttr('%s.output' % thighResultPosBlendColors, '%s.translate' % self.rootJnt)
        cmds.connectAttr('%s.ikBlend' % self.ikCtrl.name, '%s.blender' % thighResultPosBlendColors)

        cmds.connectAttr('%s.translate' % self.midJntIk, '%s.color1' % kneeResultPosBlendColors)
        cmds.connectAttr('%s.translate' % self.midJntFk, '%s.color2' % kneeResultPosBlendColors)
        cmds.connectAttr('%s.output' % kneeResultPosBlendColors, '%s.translate' % self.midJnt)
        cmds.connectAttr('%s.ikBlend' % self.ikCtrl.name, '%s.blender' % kneeResultPosBlendColors)

        cmds.connectAttr('%s.translate' % self.endJntIk, '%s.color1' % ankleResultPosBlendColors)
        cmds.connectAttr('%s.translate' % self.endJntFk, '%s.color2' % ankleResultPosBlendColors)
        cmds.connectAttr('%s.output' % ankleResultPosBlendColors, '%s.translate' % self.endJnt)
        cmds.connectAttr('%s.ikBlend' % self.ikCtrl.name, '%s.blender' % ankleResultPosBlendColors)

        thighResultRotBlendColors = cmds.createNode('blendColors', name='blend_%s_rot' % self.rootJnt.name)
        kneeResultRotBlendColors = cmds.createNode('blendColors', name='blend_%s_rot' % self.midJnt.name)
        ankleResultRotBlendColors = cmds.createNode('blendColors', name='blend_%s_rot' % self.endJnt.name)

        cmds.connectAttr('%s.rotate' % self.rootJntIk, '%s.color1' % thighResultRotBlendColors)
        cmds.connectAttr('%s.rotate' % self.rootJntFk, '%s.color2' % thighResultRotBlendColors)
        cmds.connectAttr('%s.output' % thighResultRotBlendColors, '%s.rotate' % self.rootJnt)
        cmds.connectAttr('%s.ikBlend' % self.ikCtrl.name, '%s.blender' % thighResultRotBlendColors)

        cmds.connectAttr('%s.rotate' % self.midJntIk, '%s.color1' % kneeResultRotBlendColors)
        cmds.connectAttr('%s.rotate' % self.midJntFk, '%s.color2' % kneeResultRotBlendColors)
        cmds.connectAttr('%s.output' % kneeResultRotBlendColors, '%s.rotate' % self.midJnt)
        cmds.connectAttr('%s.ikBlend' % self.ikCtrl.name, '%s.blender' % kneeResultRotBlendColors)

        cmds.connectAttr('%s.rotate' % self.endJntIk, '%s.color1' % ankleResultRotBlendColors)
        cmds.connectAttr('%s.rotate' % self.endJntFk, '%s.color2' % ankleResultRotBlendColors)
        cmds.connectAttr('%s.output' % ankleResultRotBlendColors, '%s.rotate' % self.endJnt)
        cmds.connectAttr('%s.ikBlend' % self.ikCtrl.name, '%s.blender' % ankleResultRotBlendColors)


    def set_pole_vector(self):
        startV = apiUtils.set_mVector(self.rootJntIk.get_translation())
        midV = apiUtils.set_mVector(self.midJntIk.get_translation())
        endV = apiUtils.set_mVector(self.endJntIk.get_translation())

        startEnd = endV - startV
        startMid = midV - startV
        dotP = startMid * startEnd
        proj = float(dotP) / float(startEnd.length())
        startEndN = startEnd.normal()
        projV = startEndN * proj
        arrowV = startMid - projV
        arrowV *= 2
        finalV = arrowV + midV
        pos = (finalV.x, finalV.y, finalV.z)

        cross1 = startEnd ^ startMid
        cross1.normalize()
        cross2 = cross1 ^ arrowV
        cross2.normalize()
        arrowV.normalize()
        matrixV = [arrowV.x, arrowV.y, arrowV.z, 0,
                   cross1.x, cross1.y, cross1.z, 0,
                   cross2.x, cross2.y, cross2.z, 0,
                   0, 0, 0, 1]

        matrixM = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList(matrixV, matrixM)
        matrixFn = OpenMaya.MTransformationMatrix(matrixM)

        rot = matrixFn.eulerRotation()
        rotEuler = (rot.x/math.pi*180, rot.y/math.pi*180, rot.z/math.pi*180)

        return pos, rotEuler

    def get_pole_vector(self):
        return self.poleVector

    def get_joints(self):
        return self.joints()


"""
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

from src.rigLib.base import transform
from src.rigLib.base import joint
from src.rigLib.base import locator
from src.rigLib.base import control
from src.utils import apiUtils
from src.rigLib.blocks import fkIkChain

reload(fkIkChain)
reload(joint)

legJnts = ('jt_thigh_bind', 'jt_knee_bind', 'jt_ankle_bind')
test = fkIkChain.FkIkChain(legJnts)
#test.create_block()


obj = apiUtils.get_mObject('jt_knee_bind')

fnNode = OpenMaya.MFnDependencyNode(obj)

matrixAttr = fnNode.attribute('worldMatrix')

matrixPlug = OpenMaya.MPlug(obj, matrixAttr)
matrixPlug = matrixPlug.elementByLogicalIndex(0)

matrixObj = matrixPlug.asMObject()

matrixData = OpenMaya.MFnMatrixData(matrixObj)
matrix = matrixData.matrix()

transformMatrix = OpenMaya.MTransformationMatrix(matrix)

trans = transformMatrix.translation(OpenMaya.MSpace.kWorld)

print trans.x, trans.y, trans.z



obj = apiUtils.get_mObject('jt_knee_bind')

fn = OpenMaya.MFnTransform(obj)
matrix = fn.transformation().asMatrix()

mt = OpenMaya.MTransformationMatrix(matrix)
trans = mt.translation(OpenMaya.MSpace.kWorld)
print trans.x, trans.y, trans.z

"""