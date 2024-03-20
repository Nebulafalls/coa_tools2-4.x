"""
Copyright (C) 2023 Aodaruma
hi@aodaruma.net

Created by Aodaruma

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import bpy
import bpy_extras
import bpy_extras.view3d_utils
from math import radians
import mathutils
from mathutils import Vector, Matrix, Quaternion
import math
import bmesh
from bpy.props import (
    FloatProperty,
    IntProperty,
    BoolProperty,
    StringProperty,
    CollectionProperty,
    FloatVectorProperty,
    EnumProperty,
    IntVectorProperty,
)
import os
from bpy_extras.io_utils import ExportHelper, ImportHelper
import json
from bpy.app.handlers import persistent
from ..functions import *


######################################################################################################################################### Create Sprite Object
class COATOOLS2_OT_CreateSpriteObject(bpy.types.Operator):
    bl_idname = "coa_tools2.create_sprite_object"
    bl_label = "Create Sprite Object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object

        if (
            context.active_object != None
            and obj.type == "ARMATURE"
            and obj.mode == "POSE"
        ):
            context.view_layer.objects.active = None
        bpy.ops.object.armature_add(
            radius=1,
            enter_editmode=False,
            align="WORLD",
            location=(0, 0, 0),
            rotation=(0, 0, 0),
        )
        sprite_object = bpy.context.active_object
        sprite_object.name = "SpriteObject"
        sprite_object.show_name = True
        sprite_object.coa_tools2["sprite_object"] = True
        sprite_object.show_axis = True
        bpy.ops.object.mode_set(mode="EDIT")
        for bone in sprite_object.data.edit_bones:
            sprite_object.data.edit_bones.remove(bone)
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.ed.undo_push(message="Create Sprite Object")
        return {"FINISHED"}


######################################################################################################################################### Create Sprite Object
class COATOOLS2_OT_DefineSpriteObject(bpy.types.Operator):
    bl_idname = "coa_tools2.define_sprite_object"
    bl_label = "Define as Sprite Object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.active_object.type == "ARMATURE":
            return context.active_object
        return False

    def execute(self, context):
        obj = context.active_object
        obj.coa_tools2["sprite_object"] = True
        mode = obj.mode
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.object.mode_set(mode=mode)

        bpy.ops.ed.undo_push(message="Define as Sprite Object")
        return {"FINISHED"}
