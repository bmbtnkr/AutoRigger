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

# ToDo: make this work with any number of middle joints

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

        self.rootJnt = joint.Joint(name=rootJntBind.name.replace('bind', 'template'),
                                   translateTo=rootJntBind, rotateTo=rootJntBind,
                                   jointOrient=rootJntBind.get_joint_orient(), jointTag='ikfkChain_root')

        self.midJnt = joint.Joint(name=midJntBind.name.replace('bind', 'template'),
                                  translateTo=midJntBind, rotateTo=midJntBind,
                                  jointOrient=midJntBind.get_joint_orient(), jointTag='ikfkChain_mid', parent=self.rootJnt)

        cmds.makeIdentity(self.midJnt, apply=True)

        self.endJnt = joint.Joint(name=endJntBind.name.replace('bind', 'template'),
                                  translateTo=endJntBind, rotateTo=endJntBind,
                                  jointOrient=endJntBind.get_joint_orient(), jointTag='ikfkChain_end', parent=self.midJnt)

        # create fk ctrls
        self.fkRootCtrl = control.Control(name=self.rootJnt.name.replace('jt', 'ctrl').replace('template', 'fk'),
                                          translateTo=self.rootJnt, rotateTo=self.rootJnt, normal=(1, 0, 0))

        self.fkMidCtrl = control.Control(name=self.midJnt.name.replace('jt', 'ctrl').replace('template', 'fk'),
                                         translateTo=self.midJnt, rotateTo=self.midJnt, normal=(1, 0, 0))

        self.fkEndCtrl = control.Control(name=self.endJnt.name.replace('jt', 'ctrl').replace('template', 'fk'),
                                         translateTo=self.endJnt, rotateTo=self.endJnt)

        self.fkRootCtrl.create_null_grps()
        self.fkMidCtrl.create_null_grps()
        self.fkEndCtrl.create_null_grps()

        self.fkMidCtrl.nullGrp.set_parent(self.fkRootCtrl.name)
        self.fkEndCtrl.nullGrp.set_parent(self.fkMidCtrl.name)

        self.fkRootCtrl.lockChannels(('t', 's', 'v'))
        self.fkMidCtrl.lockChannels(('t', 's', 'v'))
        self.fkEndCtrl.lockChannels(('t', 's', 'v'))

        fkRootOrientConstraint = cmds.orientConstraint(self.fkRootCtrl.name, self.rootJnt)[0]
        fkMidOrientConstraint = cmds.orientConstraint(self.fkMidCtrl.name, self.midJnt)[0]
        fkEndOrientConstraint = cmds.orientConstraint(self.fkEndCtrl.name, self.endJnt)[0]

        # create ik ctrls
        self.ikCtrl = control.Control(name=self.endJnt.name.replace('jt', 'ctrl').replace('template', 'ik'),
                                      translateTo=self.endJnt, rotateTo=self.endJnt, lockAttrs=('r', 's', 'v'))
        self.ikCtrl.create_null_grps()
        self.ikCtrl.nullGrp.set_scale((2,2,2))
        cmds.addAttr(self.ikCtrl.name, longName='ikBlend', attributeType='float', defaultValue=1, minValue=0, maxValue=1, keyable=True)

        self.ikHandle = cmds.ikHandle(name='%s_ikHandle' % self.ikCtrl.name, startJoint=self.rootJnt, endEffector=self.endJnt,
                                      solver='ikRPsolver')

        cmds.rename(self.ikHandle[1], '%s_effector' % self.endJnt)
        self.ikHandle = transform.Transform(name=self.ikHandle[0], create=False)
        ikHandleParentConstraint = cmds.parentConstraint(self.ikCtrl.name, self.ikHandle.name)[0]
        constraintTargets = cmds.parentConstraint(ikHandleParentConstraint, weightAliasList=True, query=True)

        cmds.connectAttr('%s.ikBlend' % self.ikCtrl.name, '%s.ikBlend' % self.ikHandle.name)
        cmds.connectAttr('%s.ikBlend' % self.ikCtrl.name, '%s.%s' % (ikHandleParentConstraint, constraintTargets[0]))

        fkOrientConstraintReverse = cmds.createNode('reverse', name='rev_%s' % self.fkRootCtrl.name)
        cmds.connectAttr('%s.ikBlend' % self.ikCtrl.name, '%s.inputX' % fkOrientConstraintReverse)

        for constraint in [fkRootOrientConstraint, fkMidOrientConstraint, fkEndOrientConstraint]:
            constraintTarget = cmds.orientConstraint(constraint, weightAliasList=True, query=True)[0]
            cmds.connectAttr('%s.outputX' % fkOrientConstraintReverse, '%s.%s' % (constraint, constraintTarget))

        # create pv ctrl
        self.ikPvCtrl = control.Control(name=self.midJnt.name.replace('jt', 'ctrl').replace('template', 'pv'),
                                        translate=self.set_pole_vector()[0], rotate=self.set_pole_vector()[1])
        cmds.poleVectorConstraint(self.ikPvCtrl.name, self.ikHandle.name)

    def set_pole_vector(self):
        startV = apiUtils.set_mVector(self.rootJnt.get_translation())
        midV = apiUtils.set_mVector(self.midJnt.get_translation())
        endV = apiUtils.set_mVector(self.endJnt.get_translation())

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