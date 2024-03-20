import bpy
from bpy.props import BoolProperty, FloatVectorProperty, IntProperty, FloatProperty, StringProperty, EnumProperty, PointerProperty, CollectionProperty
# from . functions import *
from . import functions
from bpy.app.handlers import persistent

def selected_update(self, context):
    if self.entry_type in ["SPRITE", "OBJECT"]:
        obj = bpy.data.objects[self.display_name]
        if self.selected:
            obj.select_set(True)
        else:
            obj.select_set(False)
    elif self.entry_type in ["BONE"]:
        obj = bpy.data.objects[self.name]
        context.view_layer.objects.active = obj
        if obj.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="POSE")
        bone = obj.data.bones[self.display_name]
        if self.selected:
            bone.select = True
            bone.select_head = True
            bone.select_tail = True
        else:
            bone.select = False
            bone.select_head = False
            bone.select_tail = False

def select_outliner_object(self, context):
    if self.outliner_index < len(self.outliner)-1:
        selected_item = self.outliner[self.outliner_index]
        if selected_item.entry_type in ["SPRITE", "OBJECT"]:
            sprite_object = bpy.data.objects[selected_item.sprite_object_name]
            edit_mode_active = sprite_object != None and (
            sprite_object.coa_tools2.edit_mesh or sprite_object.coa_tools2.edit_armature or sprite_object.coa_tools2.edit_weights or sprite_object.coa_tools2.edit_shapekey)
            if not edit_mode_active:

                selected_object = context.view_layer.objects[selected_item.name]
                for obj in context.view_layer.objects:
                    if obj in sprite_object.children:
                        obj.select_set(False)
                for item in self.outliner:
                    if item.selected:
                        bpy.data.objects[item.name].select_set(True)
                context.view_layer.objects.active = selected_object

def set_hide(self, value):
    if self.entry_type in ["OBJECT", "SPRITE", "BONE_PARENT"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        selected_object.hide_set(value)
        selected_object.hide_viewport = value
        selected_object.hide_render = value
        self["hide"] = value
        if self.id_data.coa_tools2.outliner[self.id_data.coa_tools2.outliner_index].name == self.name:
            selected_object.select_set(not value)

    elif self.entry_type in ["BONE"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        bone = selected_object.data.bones[self.display_name]
        self["hide"] = value
        bone.hide = value

def get_hide(self):
    if self.entry_type in ["OBJECT", "SPRITE", "BONE_PARENT"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        return True if selected_object.hide_viewport or selected_object.hide_get() or selected_object.hide_render else False
    elif self.entry_type in ["BONE"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        bone = selected_object.data.bones[self.display_name]
        return bone.hide
    else:
        return False

def set_hide_select(self, value):
    if self.entry_type in ["OBJECT", "SPRITE", "BONE_PARENT"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        selected_object.hide_select = value
        self["hide_select"] = value
    elif self.entry_type in ["BONE"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        bone = selected_object.data.bones[self.display_name]
        self["hide_select"] = value
        bone.hide_select = value

def get_hide_select(self):
    if self.entry_type in ["OBJECT", "SPRITE", "BONE_PARENT"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        return selected_object.hide_select
    elif self.entry_type in ["BONE"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        bone = selected_object.data.bones[self.display_name]
        return bone.hide_select
    else:
        return False

def set_favorite(self, value):
    if self.entry_type in ["OBJECT", "SPRITE", "BONE_PARENT"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        selected_object.coa_tools2.favorite = value
        self["favorite"] = value
    elif self.entry_type in ["BONE"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        bone = selected_object.data.bones[self.display_name]
        self["favorite"] = value
        bone.coa_tools2.favorite = value

def get_favorite(self):
    if self.entry_type in ["OBJECT", "SPRITE", "BONE_PARENT"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        return selected_object.coa_tools2.favorite
    elif self.entry_type in ["BONE"]:
        selected_object = bpy.context.view_layer.objects[self.name]
        bone = selected_object.data.bones[self.display_name]
        return bone.coa_tools2.favorite
    else:
        return False

class COAOutliner(bpy.types.PropertyGroup):
    name: StringProperty(name="Sprite Name")
    display_name: StringProperty(name="Name")
    index: IntProperty()
    object_type: StringProperty()
    entry_type: StringProperty(default="SPRITE") # ["SPRITE", "OBJECT","SLOT", "BONE", "BONE_PARENT"]
    hierarchy_level: IntProperty()
    slot_type: StringProperty()
    selected: BoolProperty(default=False, update=selected_update)#, update=select_object)
    active: BoolProperty(default=False)
    hide: BoolProperty(default=False, set=set_hide, get=get_hide)
    hide_select: BoolProperty(default=False, set=set_hide_select, get=get_hide_select)
    favorite: BoolProperty(default=False, set=set_favorite, get=get_favorite)
    sprite_object_name: StringProperty()
    slot_index: IntProperty()

class COATOOLS2_UL_Outliner(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        active_object = context.active_object
        obj = bpy.data.objects[item.name] if item.entry_type in ["SPRITE", "OBJECT"] else None

        if item.entry_type == "UPDATE_SPRITE_OBJECT":
            layout.operator("coa_tools2.convert_deprecated_data", text="Update Data", icon="LIBRARY_DATA_BROKEN")
        else:
            col = layout.grid_flow(row_major=True, columns=2)
            # master_row = col.row(align=True)
            row_left = col.row(align=False)
            row_left.alignment = "LEFT"
            row_right = col.row(align=True)
            row_right.alignment = "RIGHT"
            row_active = layout.row(align=True)
            sprite_object = bpy.data.objects[item.sprite_object_name] if item.sprite_object_name in bpy.data.objects else None

            edit_mode_active = sprite_object != None and (sprite_object.coa_tools2.edit_mesh or sprite_object.coa_tools2.edit_armature or sprite_object.coa_tools2.edit_weights or sprite_object.coa_tools2.edit_shapekey)
            if edit_mode_active:
                row_left.active = False
                row_right.active = False
                row_left.enabled = False
                row_right.enabled = False

            selected_icon = "LAYER_ACTIVE" if item.selected else "LAYER_USED"
            hide_icon = "HIDE_ON" if item.hide else "HIDE_OFF"
            hide_select_icon = "RESTRICT_SELECT_ON" if item.hide_select else "RESTRICT_SELECT_OFF"
            favorite_icon = "SOLO_ON" if item.favorite else "SOLO_OFF"
            show_children_icon = "DISCLOSURE_TRI_RIGHT" if obj != None and not obj.coa_tools2.show_children else "DISCLOSURE_TRI_DOWN"

            object_icon = "NONE"
            if item.object_type == "ARMATURE":
                object_icon = "ARMATURE_DATA"
            elif item.object_type == "MESH":
                object_icon = "TEXTURE"
            elif item.object_type == "CAMERA":
                object_icon = "VIEW_CAMERA"
            elif item.object_type == "LIGHT":
                object_icon = "LIGHT"

            if item.entry_type not in ["SLOT","BONE_PARENT"]:
                row_left.prop(item, "selected", text="", icon=selected_icon)
            else:
                row_left.label(text="", icon="NONE")
            for i in range(item.hierarchy_level):
                row_left.separator()

            if item.entry_type in ["SPRITE","OBJECT"]:
                # row_left.label(text="", icon=selected_icon)
                row_left.label(text="", icon=object_icon)
                if item.object_type == "ARMATURE":
                    row_left.prop(obj.coa_tools2, "show_children", text="", emboss=False, icon=show_children_icon)

                op = row_left.operator("coa_tools2.select_child", text=item.name, emboss=False)
                op.mode = "object"
                op.outliner_index = item.index
                op.ob_name = item.name

                if len(obj.coa_tools2.slot) > 0:
                    if obj.coa_tools2.slot_show:
                        row_right.prop(obj.coa_tools2, "slot_show", text="", icon="TRIA_DOWN", emboss=False)
                    else:
                        row_right.prop(obj.coa_tools2, "slot_show", text="", icon="TRIA_LEFT", emboss=False)

                if obj != sprite_object:
                    if sprite_object!= None and not sprite_object.coa_tools2.change_z_ordering:
                        row_right.prop(item, "favorite", text="", icon=favorite_icon, emboss=False)
                        row_right.prop(item, "hide", text="", icon=hide_icon, emboss=False)
                        row_right.prop(item, "hide_select", text="", icon=hide_select_icon, emboss=False)
                    else:
                        if obj.type == "MESH":
                            children_names = []
                            children = []
                            for child in sprite_object.children:
                                if child.type == "MESH":
                                    children.append(child)
                            children.sort(key=lambda x: x.location.y, reverse=False)
                            for child in children:
                                children_names.append(child.name)

                            op = row_right.operator("coa_tools2.change_z_ordering", text="", icon="TRIA_DOWN")
                            op.index = item.index
                            op.direction = "UP"
                            op.active_sprite = item.display_name
                            op.all_sprites_string = str(children_names)
                            op = row_right.operator("coa_tools2.change_z_ordering", text="", icon="TRIA_UP")
                            op.index = item.index
                            op.direction = "DOWN"
                            op.active_sprite = item.display_name
                            op.all_sprites_string = str(children_names)
                if obj.type == "ARMATURE":
                    pose_icon = "POSE_HLT"
                    if obj.mode == "OBJECT":
                        pose_icon = "OBJECT_DATAMODE"
                    elif obj.mode == "EDIT":
                        pose_icon = "EDITMODE_HLT"
                    op = row_right.operator("coa_tools2.toggle_pose_mode", icon=pose_icon, text="", emboss=False)
                    op.ob_name = obj.name
                if obj == sprite_object:
                    op = row_right.operator("coa_tools2.view_sprite", icon="ZOOM_SELECTED", text="", emboss=False)
                    op.type = "VIEW_ALL"
                    op.name = obj.name
                    row_right.prop(obj.coa_tools2, "change_z_ordering", text="", icon="SORTALPHA", emboss=False)

                if sprite_object != None and obj.type == "MESH" and sprite_object.coa_tools2.edit_armature:
                    op = row_active.operator("coa_tools2.bind_mesh_to_bones", text="", icon="BONE_DATA", emboss=False)
                    op.ob_name = item.name
            elif item.entry_type == "SLOT":
                obj = bpy.data.objects[item.name]
                slot = obj.coa_tools2.slot[item.slot_index]
                if slot.active:
                    row_left.prop(slot, "active", text=slot.mesh.name, icon="CHECKBOX_HLT", emboss=False)
                else:
                    row_left.prop(slot, "active", text=slot.mesh.name, icon="CHECKBOX_DEHLT", emboss=False)

                op = row_right.operator("coa_tools2.move_slot_item", icon="TRIA_DOWN", emboss=False, text="")
                op.idx = item.slot_index
                op.ob_name = item.name
                op.mode = "DOWN"
                op = row_right.operator("coa_tools2.move_slot_item", icon="TRIA_UP", emboss=False, text="")
                op.idx = item.slot_index
                op.ob_name = item.name
                op.mode = "UP"

                op = row_right.operator("coa_tools2.remove_from_slot", icon="PANEL_CLOSE", emboss=False, text="")
                op.idx = item.slot_index
                op.ob_name = item.name
            elif item.entry_type == "BONE_PARENT":
                obj = bpy.data.objects[item.name]
                row_left.label(text="", icon="BONE_DATA")
                row_left.label(text=item.display_name)

                if obj.coa_tools2.show_bones:
                    row_right.prop(obj.coa_tools2, "show_bones", text="", icon="TRIA_DOWN", emboss=False)
                else:
                    row_right.prop(obj.coa_tools2, "show_bones", text="", icon="TRIA_LEFT", emboss=False)

                row_right.prop(item, "favorite", text="", icon=favorite_icon, emboss=False)
                row_right.prop(item, "hide", text="", icon=hide_icon, emboss=False)
                row_right.prop(item, "hide_select", text="", icon=hide_select_icon, emboss=False)
            elif item.entry_type == "BONE":
                obj = bpy.data.objects[item.name]
                if obj.type == "ARMATURE":
                    # row_left.label(text="", icon=selected_icon)
                    bone = obj.data.bones[item.display_name]
                    row_left.label(text="", icon="BONE_DATA")

                    # row_left.label(text=item.display_name)
                    op = row_left.operator("coa_tools2.select_child", text=item.display_name, emboss=False)
                    op.mode = "bone"
                    op.outliner_index = item.index
                    op.ob_name = item.name
                    op.bone_name = item.display_name

                    if len(bone.children) > 0 and context.scene.coa_tools2.outliner_filter_names == "":
                        if bone.coa_tools2.show_children:
                            row_right.prop(bone.coa_tools2, "show_children", text="", icon="TRIA_DOWN", emboss=False)
                        else:
                            row_right.prop(bone.coa_tools2, "show_children", text="", icon="TRIA_LEFT", emboss=False)

                    row_right.prop(item, "favorite", text="", icon=favorite_icon, emboss=False)
                    row_right.prop(item, "hide", text="", icon=hide_icon, emboss=False)
                    row_right.prop(item, "hide_select", text="", icon=hide_select_icon, emboss=False)

i = -1
@persistent
def create_outliner_items(dummy):
    context = bpy.context
    scene = context.scene
    active_object = context.active_object
    outliner = context.scene.coa_tools2.outliner
    outliner_index = context.scene.coa_tools2.outliner_index
    for item in outliner:
        outliner.remove(0)

    sorted_sprites = []
    items = []
    for sprite_object in scene.objects:
        if "sprite_object" in sprite_object.coa_tools2:
            items.append(sprite_object)
            for obj in sprite_object.children:
                if obj.type != "MESH" and not sprite_object.coa_tools2.change_z_ordering:
                    items.append(obj)
            sorted_sprites = []
            for obj in sprite_object.children:
                if obj.type == "MESH":
                    sorted_sprites.append(obj)
            sorted_sprites.sort(key=lambda x: x.location.y, reverse=False)
    items += sorted_sprites

    sprite_object = None
    global i
    i = -1
    for j, obj in enumerate(items):
        if "sprite_object" in obj.coa_tools2:
            sprite_object = obj
        if (substring_found(scene.coa_tools2.outliner_filter_names, obj.name) or sprite_object == obj) and (not scene.coa_tools2.outliner_favorites or (scene.coa_tools2.outliner_favorites and obj.coa_tools2.favorite) or sprite_object == obj):
            if "sprite_object" in obj.coa_tools2 and obj.type == "EMPTY":
                i += 1
                item = outliner.add()
                item["entry_type"] = "UPDATE_SPRITE_OBJECT"
                break

            elif sprite_object == obj or ("sprite_object" not in obj.coa_tools2 and sprite_object.coa_tools2.show_children):
                i += 1
                item = outliner.add()
                item["name"] = obj.name
                item["display_name"] = obj.name
                item["index"] = i
                item["entry_type"] = "SPRITE" if obj.type == "MESH" and "sprite" in obj.coa_tools2 else "OBJECT"
                item["object_type"] = obj.type
                item["hierarchy_level"] = 0 if obj == sprite_object else 1
                item["slot_type"] = obj.coa_tools2.type
                item["selected"] = obj.select_get()
                item["active"] = (obj == active_object)
                item["hide"] = True if (obj.hide_viewport or obj.hide_get() or obj.hide_render) else False
                item["hide_select"] = obj.hide_select
                item["favorite"] = obj.coa_tools2.favorite
                item["sprite_object_name"] = sprite_object.name
                # if obj.type != "ARMATURE":
                #     break

                if not sprite_object.coa_tools2.change_z_ordering:
                    # retrieve bones
                    search_active = context.scene.coa_tools2.outliner_filter_names != ""
                    if obj.type == "ARMATURE" and sprite_object.coa_tools2.show_children and ((scene.coa_tools2.outliner_favorites and sprite_object.coa_tools2.favorite) or not scene.coa_tools2.outliner_favorites):
                        i += 1
                        bone_item = outliner.add()
                        bone_item["name"] = sprite_object.name
                        bone_item["index"] = i
                        bone_item["entry_type"] = "BONE_PARENT"
                        bone_item["display_name"] = "Bones"
                        bone_item["sprite_object_name"] = sprite_object.name
                        bone_item["hide"] = sprite_object.hide_get()
                        bone_item["hide_select"] = sprite_object.hide_select
                        bone_item["hierarchy_level"] = 1

                        if sprite_object.coa_tools2.show_bones or search_active:
                            for bone in obj.data.bones:
                                bone_name_found = substring_found(context.scene.coa_tools2.outliner_filter_names, bone.name)
                                if (bone.parent == None and not search_active) or (search_active and bone_name_found):
                                    hierarchy_level = bone_item["hierarchy_level"]
                                    recursive_bone_iteration(scene, outliner, sprite_object, sprite_object, item, bone, hierarchy_level)

                    # retrieve slots
                    if obj.coa_tools2.type == "SLOT" and obj.coa_tools2.slot_show and not sprite_object.coa_tools2.change_z_ordering:
                        for slot in obj.coa_tools2.slot:
                            i += 1
                            slot_item = outliner.add()
                            slot_item["name"] = obj.name
                            slot_item["display_name"] = slot.mesh.name
                            slot_item["index"] = i
                            slot_item["entry_type"] = "SLOT"
                            slot_item["hierarchy_level"] = item["hierarchy_level"] + 1
                            slot_item["slot_index"] = slot.index
                            slot_item["sprite_object_name"] = sprite_object.name

    if active_object != None and active_object.name in outliner:
        item = outliner[active_object.name]
        context.scene.coa_tools2.outliner_index = item.index
        if active_object.type == "ARMATURE" and active_object.mode == "POSE":
            for i, item in enumerate(outliner):
                if context.active_pose_bone != None and item.display_name == context.active_pose_bone.name:
                    context.scene.coa_tools2.outliner_index = item.index
                    break

def substring_found(query, string):
    return query.lower() in string.lower()

def recursive_bone_iteration(scene, outliner, sprite_object, obj, parent_item, bone, hierarchy_level):
    global i

    search_active = scene.coa_tools2.outliner_filter_names != ""
    if ((scene.coa_tools2.outliner_favorites and bone.coa_tools2.favorite) or not scene.coa_tools2.outliner_favorites):# or (search_active and bone_name_found):
        i += 1
        bone_item = outliner.add()
        bone_item["name"] = obj.name
        bone_item["display_name"] = bone.name
        bone_item["entry_type"] = "BONE"
        bone_item["index"] = i
        bone_item["sprite_object_name"] = sprite_object.name
        bone_item["hide"] = bone.hide
        bone_item["hide_select"] = bone.hide_select
        bone_item["selected"] = bone.select
        bone_item["hierarchy_level"] = parent_item["hierarchy_level"] + 1 + hierarchy_level
        if not search_active:
            for child in bone.children:
                if bone.coa_tools2.show_children:
                    recursive_bone_iteration(scene, outliner, sprite_object, obj, parent_item, child, hierarchy_level + 1)
