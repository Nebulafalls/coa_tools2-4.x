import bpy
import os

# 创建预览集并注册图标
preview_collection = bpy.utils.previews.new()
icon_path = os.path.join(os.path.dirname(__file__), "icon")
preview_collection.load("draw_bone", os.path.join(icon_path, "coa_tools2.draw_bone.png"), 'IMAGE')
bpy.types.WindowManager.my_icons = preview_collection
