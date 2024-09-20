bl_info = {
    "name": "Make Mesh Convex",
    "blender": (3, 0, 0),
    "category": "Object",
    "description": "Adds a panel to the N-panel in the 3D Viewport with a button to make a mesh convex",
}

import bpy

class OBJECT_OT_make_mesh_convex(bpy.types.Operator):
    """Make the selected mesh convex"""
    bl_idname = "object.make_mesh_convex"
    bl_label = "Make Mesh Convex"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.object
        
        # Check if the selected object is a mesh
        if obj and obj.type == 'MESH':
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.convex_hull()
            bpy.ops.object.mode_set(mode='OBJECT')
            self.report({'INFO'}, "Made Mesh Convex")
        else:
            self.report({'WARNING'}, "Selected object is not a mesh")
        
        return {'FINISHED'}

class VIEW3D_PT_make_mesh_convex_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Modeling Shortcuts"
    bl_idname = "VIEW3D_PT_make_mesh_convex_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Level Editor'  # This defines the tab in the N-panel where the button will be located

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("object.make_mesh_convex")

def register():
    bpy.utils.register_class(OBJECT_OT_make_mesh_convex)
    bpy.utils.register_class(VIEW3D_PT_make_mesh_convex_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_make_mesh_convex)
    bpy.utils.unregister_class(VIEW3D_PT_make_mesh_convex_panel)

if __name__ == "__main__":
    register()
