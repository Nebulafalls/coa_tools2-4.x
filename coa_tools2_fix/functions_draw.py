import bpy
import gpu
from gpu_extras.batch import batch_for_shader
import blf

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def draw_edit_mode(self,context,color=[0.41, 0.38, 1.0, 1.0],text="Edit Shapekey Mode",offset=0):
    region = context.region
    x = region.width
    y = region.height
    
    scale = x / 1200
    scale = clamp(scale,.5,1.5)
    
    r_offset = 0
    if context.preferences.system.use_region_overlap:
        r_offset = context.area.regions[1].width

    ### draw box behind text
    b_width = int(240*scale)
    b_height = int(36*scale)
    
    # 使用gpu模块替换bgl绘图代码
    coords = [
        (x-b_width, 0), (x, 0),
        (x, b_height), (x-b_width, b_height),
        (x-b_width, 0)
    ]
    
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
    
    gpu.state.blend_set('ALPHA')
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)
    
    ### draw edit type
    font_id = 0  # XXX, need to find out how best to get this.
    blf.color(font_id, 0.041613, 0.041613, 0.041613, 1.000000)
    text_offset = int((220+offset)*scale)
    text_y_offset = int(11 * scale)
    blf.position(font_id, x-text_offset, text_y_offset, 0)
    blf.size(font_id, 20, int(72*scale))
    blf.draw(font_id, text)
    
    ### draw viewport outline
    outline_coords = [
        (r_offset, 0), (r_offset+x, 0),
        (r_offset+x, y), (r_offset+0, y),
        (r_offset, 0)
    ]
    
    outline_shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    outline_batch = batch_for_shader(outline_shader, 'LINE_STRIP', {"pos": outline_coords})
    
    gpu.state.blend_set('ALPHA')
    gpu.state.line_width_set(4)
    outline_shader.bind()
    outline_shader.uniform_float("color", color)
    outline_batch.draw(outline_shader)
    
    # 恢复默认状态
    gpu.state.line_width_set(1)
    gpu.state.blend_set('NONE')