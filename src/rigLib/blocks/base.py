from src.rigLib.base import transform
from src.rigLib.base import control
import maya.cmds as cmds

class Base(object):
    def __init__(self, basePos=None):
        self.basePos = basePos

    def create_block(self):
        rootGrp = transform.Transform(name='root_grp')
        geoGrp = transform.Transform(name='geo_grp', parent=rootGrp.name)
        mvmtGrp = transform.Transform(name='mvmt_grp', parent=rootGrp.name)

        scaleGrp = transform.Transform(name='scale_grp', parent=mvmtGrp.name)

        ctrlGrp = transform.Transform(name='ctrl_grp', parent=scaleGrp.name)
        deformerGrp = transform.Transform(name='def_grp', parent=scaleGrp.name)

        skelGrp = transform.Transform(name='skel_grp', parent=scaleGrp.name)
        ikSkelGrp = transform.Transform(name='skel_ik_grp', parent=skelGrp.name)
        fkSkelGrp = transform.Transform(name='skel_fk_grp', parent=skelGrp.name)

        bindSkelGrp = transform.Transform(name='skel_bind_grp', parent=skelGrp.name)

        rootCtrl = control.Control(name='root_ctrl', shape='circle', hideAttrs='s')
        rootCtrlNullGrps = rootCtrl.create_null_grps()
        cmds.addAttr(rootCtrl.name, longName='masterScale', minValue=0.001, defaultValue=1, keyable=True)
        cmds.parent(rootCtrlNullGrps[0], mvmtGrp.name)


"""
root
    geo
    mvmt

"""


"""
Char_Rig
    grp_char
        grp_charScale
            grp_deformers
                grp_spine
                grp_l_leg
                grp_eyes
            grp_ctrl
            grp_skel
                grp_ik
                grp_fk
                grp_template (grp_result)
                grp_bind
            grp_misc - don't need
            constrain_jt_all_DONTTOUCH - for all_bind_Cheat
            null_ctrl_shadow - don't need
    grp_other
        grp_geo
        null_ctrl_world
            ctrl_world
"""