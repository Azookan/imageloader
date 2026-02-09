import bpy
from bpy import context

bl_info = {
    "name": "imageloader",
    "blender": (2, 80, 0),
    "category": "Object",
}

load_to_view = True

class loadImage(bpy.types.Operator):
    """Image Loading Script"""  #tooltip for menu items and buttons
    bl_idname = "object.loadimage" 
    bl_label = "Load Image"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        
        text_image_path = "/Users/kevinyang/imageloader/test image.webp"
        
        if load_to_view:
            bpy.ops.object.empty_image_add(filepath = text_image_path, align = 'VIEW')
        else:
            bpy.ops.object.empty_image_add(filepath = text_image_path)
        

        return {'FINISHED'}
    
class loadImageSideBar(bpy.types.Panel):
    bl_idname = "Test"
    bl_label = "Load Image"
    bl_options = {"DEFAULT_CLOSED"}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Load Image"
    
    def draw(self, context):
        
        img = bpy.data.images.get("test image.webp")
        icon_id = bpy.types.UILayout.icon(img)
        
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "my_tool")
        layout.template_icon(icon_value = icon_id, scale = 5)
        prop = layout.operator(loadImage.bl_idname, text="Load Image")
        
        
        
        
        
        

def menu_func(self, context):
    self.layout.operator(loadImage.bl_idname)
    
classes = [
    loadImage,
    loadImageSideBar,

]

def register():
    bpy.utils.register_class(loadImage)
    bpy.utils.register_class(loadImageSideBar)
    bpy.types.Scene.my_tool = bpy.props.StringProperty(
    name = "Search",
    description = ":",
    default = "",
    maxlen = 1024, 
    )
    #bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(loadImage)
    bpy.utils.unregister_class(loadImageSideBar)


if __name__ == "__main__": #testing
    register()
