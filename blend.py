import bpy

bl_info = {
    "name": "imageloader",
    "blender": (2, 80, 0),
    "category": "Object",
}

class loadImage(bpy.types.Operator):
    """Image Loading Script"""  #tooltip for menu items and buttons
    bl_idname = "loadimage" 
    bl_label = "Load Image"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        return {'FINISHED'}
        

def register():
    bpy.utils.register_class(loadImage)

def unregister():
    bpy.utils.unregister_class(loadImage)


if __name__ == "__main__": #testing
    register()
