"""
Module for creating an AutoRigger foot component

Foot component - Animateable component
Requires 3 joint chain plus foot chain and ground contact positions
FK/IK switch with offset pivots for ground contact and toe rotation
Control Flags: FK, IK, Pole Vector, FK/IK Switch, Toe FK
"""

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import math
from src.rigLib.base import transform
from src.rigLib.base import control
from src.rigLib.base import joint
from src.utils import apiUtils
from src.rigLib.base import locator

class Foot(object):
    def __init__(self, joints=(), legRig=None, heelPiv=None, insidePiv=None, outsidePiv=None):
        self.joints = joints
        self.legRig = legRig
        self.heelPiv = heelPiv
        self.insidePiv = insidePiv
        self.outsidePiv = outsidePiv
        # todo: add references to foot ik ctrl, foot ik end jnt, leg ik handle, leg ik handle parent constraint
        self.ikCtrl = str(legRig.ikCtrl.name)
        self.legIkHandle = str(legRig.ikHandle.name)

    def create_block(self):
        # create joints
        footJntBind = joint.Joint(name=self.joints[0], create=False)
        ballJntBind = joint.Joint(name=self.joints[1], create=False)
        toeJntBind = joint.Joint(name=self.joints[2], create=False)

        # self.footCtrl = control.Control(name=self.legRig.ikCtrl.name, create=False)

        # self.footJntIk = joint.Joint(name=self.legRig.endJntIk.name, create=False)
        self.footJntIk = joint.Joint(name='jt_l_foot_ik', create=False)
        self.ballJntIk = joint.Joint(name=ballJntBind.name.replace('bind', 'ik'), translateTo=ballJntBind, rotateTo=ballJntBind, parent=self.footJntIk)
        self.toeJntIk = joint.Joint(name=toeJntBind.name.replace('bind', 'ik'), translateTo=toeJntBind, rotateTo=toeJntBind, parent=self.ballJntIk)
        cmds.makeIdentity(self.ballJntIk, apply=True)

        # Create ik handles
        ballIkHandle = cmds.ikHandle(name='%s_ikHandle_sc' % self.ballJntIk.name, startJoint=self.footJntIk, endEffector=self.ballJntIk, solver='ikSCsolver')
        cmds.rename(ballIkHandle[1], '%s_eff' % self.ballJntIk)
        # cmds.parentConstraint(self.footCtrl.name, ballIkHandle[0], maintainOffset=True)

        toeIkHandle = cmds.ikHandle(name='%s_ikHandle_sc' % self.toeJntIk.name, startJoint=self.ballJntIk, endEffector=self.toeJntIk, solver='ikSCsolver')
        cmds.rename(toeIkHandle[1], '%s_eff' % self.toeJntIk)
        # cmds.parentConstraint(self.footCtrl.name, toeIkHandle[0], maintainOffset=True)

        # Create pivot locators - make these group nulls when done
        heelLoc = locator.Locator(name='heel_pivot_loc', translateTo=self.heelPiv)
        outsideLoc = locator.Locator(name='outside_pivot_loc', translateTo=self.outsidePiv, parent=heelLoc)
        insideLoc = locator.Locator(name='inside_pivot_loc', translateTo=self.insidePiv, parent=outsideLoc)
        toeLoc = locator.Locator(name='toe_pivot_loc', translateTo=self.toeJntIk, parent=insideLoc)
        ballLoc = locator.Locator(name='ball_pivot_loc', translateTo=self.ballJntIk, parent=toeLoc)
        cmds.parent(ballIkHandle[0], ballLoc)
        cmds.parent(toeIkHandle[0], insideLoc)

        # all locs under ctrl l foot
        # re-parent main leg ik hand under ball loc
        # todo: make a reference to ik handle via fkIkChain().ikHandle, don't hard-code it
        cmds.parent(self.legIkHandle, ballLoc)
        cmds.delete('ctrl_l_foot_ik_ikHandle_parentConstraint1') # Future Notes: Don't hard code this constraint
        heelLocNull = cmds.group(name='null_%s' % heelLoc, empty=True)
        cmds.xform(heelLocNull, t=heelLoc.get_translation())
        cmds.parent(heelLoc, heelLocNull)
        cmds.parentConstraint(self.ikCtrl, heelLocNull, maintainOffset=True)

        # add roll attributes on foot control
        cmds.addAttr(self.ikCtrl, longName='footRollControls', attributeType='enum', enumName='==========', keyable=True)
        cmds.setAttr('%s.footRollControls' % self.ikCtrl, lock=True)
        cmds.addAttr(self.ikCtrl, longName='roll', attributeType='float', defaultValue=0, minValue=-90, keyable=True)
        cmds.addAttr(self.ikCtrl, longName='bendLimitAngle', attributeType='float', defaultValue=45, keyable=True)
        cmds.addAttr(self.ikCtrl, longName='toeStraightAngle', attributeType='float', defaultValue=70, keyable=True)
        cmds.addAttr(self.ikCtrl, longName='sideRoll', attributeType='float', defaultValue=0, minValue=-90, maxValue=90, keyable=True)
        cmds.addAttr(self.ikCtrl, longName='ballLean', attributeType='float', defaultValue=0, keyable=True)
        cmds.addAttr(self.ikCtrl, longName='heelSwivel', attributeType='float', defaultValue=0, keyable=True)
        cmds.addAttr(self.ikCtrl, longName='ballSwivel', attributeType='float', defaultValue=0, keyable=True)
        cmds.addAttr(self.ikCtrl, longName='toeSwivel', attributeType='float', defaultValue=0, keyable=True)
        cmds.addAttr(self.ikCtrl, longName='toeRaise', attributeType='float', defaultValue=0, keyable=True)

        # setup reverse foot roll with nodes
        heelRotClamp = cmds.createNode('clamp', name='clamp_%s_heelRot' % self.ikCtrl)
        cmds.connectAttr('%s.roll' % self.ikCtrl, '%s.inputR' % heelRotClamp)
        cmds.setAttr('%s.minR' % heelRotClamp, -90)
        cmds.connectAttr('%s.outputR' % heelRotClamp, '%s.rotateX' % heelLoc)

        zeroToBendClamp = cmds.createNode('clamp', name='clamp_%s_ballRot' % self.ikCtrl)
        cmds.connectAttr('%s.roll' % self.ikCtrl, '%s.inputR' % zeroToBendClamp)
        cmds.connectAttr('%s.bendLimitAngle' % self.ikCtrl, '%s.maxR' % zeroToBendClamp)

        zeroToBendPercent = cmds.createNode('setRange', name='setRange_%s_ballRot' % self.ikCtrl)
        cmds.connectAttr('%s.minR' % zeroToBendClamp, '%s.oldMinX' % zeroToBendPercent)
        cmds.connectAttr('%s.maxR' % zeroToBendClamp, '%s.oldMaxX' % zeroToBendPercent)
        cmds.setAttr('%s.maxX' % zeroToBendPercent, 1)
        cmds.connectAttr('%s.inputR' % zeroToBendClamp, '%s.valueX' % zeroToBendPercent)

        bendToStraightClamp = cmds.createNode('clamp', name='clamp_%s_bentToStraight' % self.ikCtrl)
        cmds.connectAttr('%s.roll' % self.ikCtrl, '%s.inputR' % bendToStraightClamp)
        cmds.connectAttr('%s.bendLimitAngle' % self.ikCtrl, '%s.minR' % bendToStraightClamp)
        cmds.connectAttr('%s.toeStraightAngle' % self.ikCtrl, '%s.maxR' % bendToStraightClamp)

        bendToStraightPercent = cmds.createNode('setRange', name='setRange_%s_toeRot' % self.ikCtrl)
        cmds.connectAttr('%s.inputR' % bendToStraightClamp, '%s.valueX' % bendToStraightPercent)
        cmds.connectAttr('%s.minR' % bendToStraightClamp, '%s.oldMinX' % bendToStraightPercent)
        cmds.connectAttr('%s.maxR' % bendToStraightClamp, '%s.oldMaxX' % bendToStraightPercent)
        cmds.setAttr('%s.maxX' % bendToStraightPercent, 1)

        invertPercentDiff = cmds.createNode('plusMinusAverage', name='diff_%s_invertPercent' % self.ikCtrl)
        cmds.setAttr('%s.input1D[0]' % invertPercentDiff, 1)
        cmds.connectAttr('%s.outValueX' % bendToStraightPercent, '%s.input1D[1]' % invertPercentDiff)
        cmds.setAttr('%s.operation' % invertPercentDiff, 2)

        ballPercentMult = cmds.createNode('multiplyDivide', name='mult_%s_ballRotPercent' % self.ikCtrl)
        cmds.connectAttr('%s.outValueX' % zeroToBendPercent, '%s.input1X' % ballPercentMult)
        cmds.connectAttr('%s.output1D' % invertPercentDiff, '%s.input2X' % ballPercentMult)

        ballRollMult = cmds.createNode('multiplyDivide', name='mult_%s_ballRoll' % self.ikCtrl)
        cmds.connectAttr('%s.outputX' % ballPercentMult, '%s.input1X' % ballRollMult)
        cmds.connectAttr('%s.roll' % self.ikCtrl, '%s.input2X' % ballRollMult)
        cmds.connectAttr('%s.outputX' % ballRollMult, '%s.rotateX' % ballLoc)

        toeRollMult = cmds.createNode('multiplyDivide', name='mult_%s_toeRoll' % self.ikCtrl)
        cmds.connectAttr('%s.outValueX' % bendToStraightPercent, '%s.input1X' % toeRollMult)
        cmds.connectAttr('%s.inputR' % bendToStraightClamp, '%s.input2X' % toeRollMult)
        cmds.connectAttr('%s.outputX' % toeRollMult, '%s.rotateX' % toeLoc)

        # setup side roll
        posTiltRemap = cmds.createNode('remapValue', name='remap_%s_tiltPos' % self.ikCtrl)
        cmds.connectAttr('%s.sideRoll' % self.ikCtrl, '%s.inputValue' % posTiltRemap)
        cmds.setAttr('%s.inputMin' % posTiltRemap, -90)
        cmds.setAttr('%s.inputMax' % posTiltRemap, 0)
        cmds.setAttr('%s.outputMin' % posTiltRemap, 90)
        cmds.setAttr('%s.outputMax' % posTiltRemap, 0)
        cmds.connectAttr('%s.outValue' % posTiltRemap, '%s.rotateZ' % insideLoc)

        negTiltRemap = cmds.createNode('remapValue', name='remap_%s_tiltNeg' % self.ikCtrl)
        cmds.connectAttr('%s.sideRoll' % self.ikCtrl, '%s.inputValue' % negTiltRemap)
        cmds.setAttr('%s.inputMin' % negTiltRemap, 0)
        cmds.setAttr('%s.inputMax' % negTiltRemap, 90)
        cmds.setAttr('%s.outputMin' % negTiltRemap, 0)
        cmds.setAttr('%s.outputMax' % negTiltRemap, -90)
        cmds.connectAttr('%s.outValue' % negTiltRemap, '%s.rotateZ' % outsideLoc)

        # setup lean / spin
        cmds.connectAttr('%s.ballLean' % self.ikCtrl, '%s.rotateZ' % ballLoc)
        cmds.connectAttr('%s.heelSwivel' % self.ikCtrl, '%s.rotateY' % heelLoc)
        cmds.connectAttr('%s.ballSwivel' % self.ikCtrl, '%s.rotateY' % ballLoc)
        cmds.connectAttr('%s.toeSwivel' % self.ikCtrl, '%s.rotateY' % toeLoc)

        # setup toe wiggle
        toeWiggleGrp = transform.Transform(name='%s_grp' % toeIkHandle[0], translateTo=ballLoc, parent=insideLoc)
        cmds.parent(toeIkHandle[0], toeWiggleGrp)
        cmds.connectAttr('%s.toeRaise' % self.ikCtrl, '%s.rotateX' % toeWiggleGrp)

# import maya.cmds as cmds
# import maya.OpenMaya as OpenMaya
#
# from src.rigLib.base import transform
# from src.rigLib.base import joint
# from src.rigLib.base import locator
# from src.rigLib.base import control
# from src.utils import apiUtils
# from src.rigLib.blocks import fkIkChain2 as fkIkChain
# from src.rigLib.blocks import foot
#
# reload(transform)
# reload(fkIkChain)
# reload(joint)
# reload(locator)
# reload(apiUtils)
# reload(fkIkChain)
# reload(foot)
#
# legJnts = ('jt_l_thigh_bind', 'jt_l_knee_bind', 'jt_l_foot_bind')
# legRig = fkIkChain.FkIkChain(legJnts)
# legRig.create_block()
#
# footJnts = ('jt_l_foot_bind', 'jt_l_ball_bind', 'jt_l_toe_bind')
# heelPiv = 'heelPiv'
# insidePiv = 'insidePiv'
# outsidePiv = 'outsidePiv'
#
# footRig = foot.Foot(joints=footJnts, legRig=legRig, heelPiv=heelPiv, insidePiv=insidePiv, outsidePiv=outsidePiv)
# footRig.create_block()
