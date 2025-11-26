import bpy
from bpy.types import Menu
from bpy.props import FloatProperty, IntProperty, BoolProperty, StringProperty, CollectionProperty, FloatVectorProperty, EnumProperty, IntVectorProperty
from .. functions import *
#from .. ui import preview_collections

preview_collections_pie = {}

class COATOOLS2_MT_menu(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "COA 工具"
    bl_idname = "COATOOLS2_MT_menu"
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        sprite_object = get_sprite_object(obj)
        if context.area.type == "NLA_EDITOR ":
            return True

        if sprite_object != None:
            if (obj != None and ("sprite" in obj.coa_tools2 or "sprite_object" in obj.coa_tools2) or ("coa_sprite" in obj or "sprite_object" in obj)) or (sprite_object != None and obj.type == "ARMATURE"):
                return True
    
    def draw(self, context):
        obj = context.active_object
        
        layout = self.layout
        pie = layout.menu_pie()
        if obj != None and context.area.type == "VIEW_3D":
            #pie.operator_enum("view3d.coa_pie_menu_options", "selected_mode")
            if obj.type == "MESH":
                pie.operator("coa_tools2.select_frame_thumb",text="选择帧",icon="IMAGE_RGB")
                pie.operator("wm.call_menu_pie", icon="KEYTYPE_MOVING_HOLD_VEC", text="添加关键帧(s)").name = "COATOOLS2_MT_keyframe_menu_add"
                pie.operator("coa_tools2.edit_weights",text="编辑权重",icon="MOD_VERTEX_WEIGHT")
                op = pie.operator("coa_tools2.edit_mesh",text="编辑网格",icon="GREASEPENCIL")
                op.mode = "EDIT_MESH"
                pie.operator("coa_tools2.quick_armature",text="编辑骨骼",icon="ARMATURE_DATA")
                pie.operator("coa_tools2.edit_shapekey",text="编辑形状键",icon="SHAPEKEY_DATA")
                pie.row()    
                pie.operator("wm.call_menu_pie", icon="HANDLETYPE_ALIGNED_VEC", text="删除关键帧(s)").name = "COATOOLS2_MT_keyframe_menu_remove"
                
            elif obj.type == "ARMATURE":
                pie.operator("coa_tools2.set_ik",text="创建IK骨",icon="CONSTRAINT_BONE")
                pie.operator("wm.call_menu_pie", icon="KEYTYPE_MOVING_HOLD_VEC", text="添加关键帧(s)").name = "COATOOLS2_MT_keyframe_menu_add"
                pie.operator("coa_tools2.draw_bone_shape",text="骨骼形状",icon="BONE_DATA")
                pie.operator("coa_tools2.flip_bone_x",text="翻转骨骼",icon="ARROW_LEFTRIGHT")
                pie.operator("coa_tools2.quick_armature",text="编辑骨骼",icon="ARMATURE_DATA")
                pie.operator("coa_tools2.set_stretch_bone",text="创建拉伸骨",icon="CONSTRAINT_BONE")
                pie.operator("wm.call_menu_pie", icon="HANDLETYPE_ALIGNED_VEC", text="删除关键帧").name = "COATOOLS2_MT_keyframe_menu_remove"
            elif obj.type == "EMPTY":
                pie.operator("import.coa_import_sprites",text="导入精灵",icon="FILEBROWSER")
                if get_addon_prefs(context).dragon_bones_export:
                    pie.operator("coa_tools2.export_dragon_bones",text="导出 Dragonbones",icon_value=db_icon.icon_id)
                else:
                    pie.row()    
                pie.operator("wm.coa_create_ortho_cam",text="创建正交相机",icon="CAMERA_DATA")
                pie.operator("coa_tools2.batch_render",text="批量渲染动画",icon="CLIP")

class COATOOLS2_MT_keyframe_menu_01(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "COA Tools"
    bl_idname = "COATOOLS2_MT_keyframe_menu_01"
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        sprite_object = get_sprite_object(obj)
        if (obj != None and "coa_sprite" in obj) or (sprite_object != None and obj.type == "ARMATURE"):
            return True
    
    def draw(self, context):
        obj = context.active_object
        
        layout = self.layout
        pie = layout.menu_pie()
        if obj != None:
            pie.operator("wm.call_menu_pie", icon="KEYTYPE_MOVING_HOLD_VEC", text="Add Keyframe(s)").name = "view3d.coa_pie_keyframe_menu_add"
            pie.operator("wm.call_menu_pie", icon="HANDLETYPE_ALIGNED_VEC", text="Delete Keyframe(s)").name = "view3d.coa_pie_keyframe_menu_remove"

class COATOOLS2_MT_keyframe_menu_add(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "COA Add Keyframe"
    bl_idname = "COATOOLS2_MT_keyframe_menu_add"
    
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        add_remove_keyframe(pie,True)
        
class COATOOLS2_MT_keyframe_menu_remove(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "COA Remove Keyframe"
    bl_idname = "COATOOLS2_MT_keyframe_menu_remove"
    
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        add_remove_keyframe(pie,False)


def add_remove_keyframe(pie, add):
    context = bpy.context
    obj = context.active_object
    if obj.type == "MESH":
        op = pie.operator("coa_tools2.add_keyframe", text="Slot Index", icon="IMAGE_RGB")
        op.prop_name = "coa_tools2.slot_index"
        op.add_keyframe = add
        op.default_interpolation = "CONSTANT"

        op = pie.operator("coa_tools2.add_keyframe", text="Sprite Alpha", icon="RESTRICT_VIEW_OFF")
        op.prop_name = "coa_tools2.alpha"
        op.add_keyframe = add
        op.default_interpolation = "BEZIER"

        op = pie.operator("coa_tools2.add_keyframe", text="Modulate Color", icon="COLOR")
        op.prop_name = "coa_tools2.modulate_color"
        op.add_keyframe = add
        op.default_interpolation = "BEZIER"

        op = pie.operator("coa_tools2.add_keyframe", text="Z Value", icon="IMAGE_ZDEPTH")
        op.prop_name = "coa_tools2.z_value"
        op.add_keyframe = add
        op.default_interpolation = "CONSTANT"

    elif obj.type == "ARMATURE":
        bone = context.active_pose_bone
        op = pie.operator("coa_tools2.add_keyframe", text="Location")
        op.prop_name = "location"
        op.add_keyframe = add
        op.default_interpolation = "BEZIER"

        op = pie.operator("coa_tools2.add_keyframe", text="Scale")
        op.prop_name = "scale"
        op.add_keyframe = add
        op.default_interpolation = "BEZIER"

        op = pie.operator("coa_tools2.add_keyframe", text="Rotation")
        op.prop_name = "rotation"
        op.add_keyframe = add
        op.default_interpolation = "BEZIER"

        op = pie.operator("coa_tools2.add_keyframe", text="Location Rotation Scale", icon="MOD_ARMATURE")
        op.prop_name = "LocRotScale"
        op.add_keyframe = add
        op.default_interpolation = "BEZIER"
