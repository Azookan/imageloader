import os
import bpy
from bpy import context
from bpy.types import WindowManager
from bpy.props import (
    StringProperty,
    EnumProperty,
)

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

def enum_previews_from_directory_items(self, context):
    """EnumProperty callback"""
    enum_items = []
    wm = context.window_manager
    directory = wm.my_previews_dir
    
    bpy.data.window_managers["WinMan"].my_previews_dir = directory

    # Get the preview collection (defined in register func).
    pcoll = preview_collections["main"]

        # Scan the directory for png files
    image_paths = []
    for fn in os.listdir(directory):
        if fn.lower().endswith((".png",".webp", ".jpg")):
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



WindowManager.my_previews_dir = StringProperty(
    name="Folder Path",
    subtype='DIR_PATH',
    default="/Users/kevinyang/imageloader/images"
)

WindowManager.my_previews = EnumProperty(
    items=enum_previews_from_directory_items,
)

class loadImage(bpy.types.Operator):
    """Image Loading Script"""  #tooltip for menu items and buttons
    bl_idname = "object.loadimage" 
    bl_label = "Load Image"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        directory = "/Users/kevinyang/imageloader/images"
        name = bpy.data.window_managers["WinMan"].my_previews
        file_path = os.path.join(directory, name)
        bpy.data.images.load(file_path, check_existing = False)
        
        if bpy.context.scene.my_tool.my_bool:
            bpy.ops.object.empty_image_add(filepath = file_path)
        else:
            bpy.ops.object.empty_image_add(filepath = file_path, align = 'VIEW')
            
        return {'FINISHED'}  


class loadImageSideBar(bpy.types.Panel):
    bl_idname = "Test"
    bl_label = "Load Image"
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
        
        row = layout.row()
        layout.prop(mytool, "my_string", text="Search")
        
        #layout.template_icon(icon_value = icon_id, scale = 5)
        
        row = layout.row()
        row.template_icon_view(wm, "my_previews")
        
        row = layout.row()
        layout.prop(mytool, "my_bool", text="Load at cursor")
            
        row = layout.row()    
        prop = layout.operator(loadImage.bl_idname, text="Load Image")
        
# We can store multiple preview collections here,
# however in this example we only store "main"
preview_collections = {}

classes = [
    loadImage,
    loadImageSideBar,
    Settings,
]


def register():
    

    # Note that preview collections returned by bpy.utils.previews
    # are regular Python objects - you can use them to store custom data.
    #
    # This is especially useful here, since:
    # - It avoids us regenerating the whole enum over and over.
    # - It can store enum_items' strings
    #   (remember you have to keep those strings somewhere in py,
    #   else they get freed and Blender references invalid memory!).
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()
    pcoll.my_previews_dir = "/Users/kevinyang/imageloader/images"
    pcoll.my_previews = ()

    preview_collections["main"] = pcoll
    
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=Settings)


def unregister():
    del WindowManager.my_previews

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
    
    