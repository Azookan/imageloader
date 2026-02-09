import bpy
from bpy import context

bl_info = {
    "name": "imageloader",
    "blender": (2, 80, 0),
    "category": "Object",
}
              
class Settings(bpy.types.PropertyGroup):
    
    my_string : bpy.props.StringProperty(
    name = "Search",
    description = ":",
    default = "",
    maxlen = 1024, 
    )
    
    my_bool : bpy.props.BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
    )


def enumPrev(self, context):
    wm = context.window_manager
    
    pcoll = preview_collections["main"]
    
    directory = "/Users/kevinyang/imageloader/images"
    
    image_paths = []
    for fn in os.listdir(directory):
            if fn.lower().endswith((".png", ".jpg", ".webp")):
                image_paths.append(fn)
    
    for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            icon = pcoll.get(name)
            if not icon:
                thumb = pcoll.load(name, filepath, 'IMAGE')
            else:
                thumb = pcoll[name]
            enum_items.append((name, name, "", thumb.icon_id, i))
            
    pcoll.my_previews = enum_items
    pcoll.my_previews_dir = directory
    return pcoll.my_previews

class loadImage(bpy.types.Operator):
    """Image Loading Script"""  #tooltip for menu items and buttons
    bl_idname = "object.loadimage" 
    bl_label = "Load Image"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        
        text_image_path = "/Users/kevinyang/imageloader/images/"
        
        if bpy.context.scene.my_tool.my_bool:
            bpy.ops.object.empty_image_add(filepath = text_image_path + bpy.data.window_managers["WinMan"].my_previews)
        else:
            bpy.ops.object.empty_image_add(filepath = text_image_path + bpy.data.window_managers["WinMan"].my_previews, align = 'VIEW')
            
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
        #icon_id = bpy.types.UILayout.icon(img)
        
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        wm = context.window_manager
        
        
        layout.prop(mytool, "my_string", text="Search")
        
        #layout.template_icon(icon_value = icon_id, scale = 5)
        
        row = self.layout.row()
        row.template_icon_view(wm, "my_previews")
        print(wm)
        
        
        layout.prop(mytool, "my_bool", text="Load at cursor")
        
        if bpy.context.scene.my_tool.my_bool is False:
            load_to_view = False
            
        prop = layout.operator(loadImage.bl_idname, text="Load Image")
        
classes = [
    loadImage,
    loadImageSideBar,
    Settings,
]
        
preview_collections = {}

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    
    pcoll = bpy.utils.previews.new()
    preview_collections["main"] = pcoll
    
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=Settings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.my_tool
    del WindowManager.my_previews
    
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()    
    
    


if __name__ == "__main__": #testing
    register()
