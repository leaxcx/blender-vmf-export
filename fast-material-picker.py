bl_info = {
    "name": "List Materials in 3D View Panel",
    "blender": (3, 0, 0),
    "category": "Material",
}

import bpy

class MATERIALS_OT_DropToFace(bpy.types.Operator):
    """Drop material to selected face"""
    bl_idname = "materials.drop_to_face"
    bl_label = "Drop Material to Face"
    bl_description = "Assign this material to the selected face"
    
    material_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.active_object
        mat = bpy.data.materials.get(self.material_name)

        if obj and mat and obj.type == 'MESH' and obj.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
            selected_faces = [poly for poly in obj.data.polygons if poly.select]

            # Assign the material to selected faces
            if selected_faces:
                if mat.name not in obj.data.materials:
                    obj.data.materials.append(mat)
                mat_index = obj.data.materials.find(mat.name)
                for poly in selected_faces:
                    poly.material_index = mat_index
            
            bpy.ops.object.mode_set(mode='EDIT')
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No active object or material found, or not in edit mode")
            return {'CANCELLED'}

    def invoke(self, context, event):
        return self.execute(context)


class MATERIALS_PT_ListMaterials(bpy.types.Panel):
    """Creates a Panel in the 3D View side panel"""
    bl_label = "Materials"
    bl_idname = "MATERIALS_PT_list_materials"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Level Editor"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Collect all materials in the scene
        materials = {mat for obj in scene.objects for mat in obj.data.materials if mat}

        # Display the materials with drag-and-drop functionality
        for mat in materials:
            box = layout.box()  # Create a box to group material information and functionality

            # Display the material name
            box.label(text=mat.name)

            # Add drag-and-drop functionality to assign material to selected face
            box.operator("materials.drop_to_face", text="Assign to Selected Face", icon='MATERIAL').material_name = mat.name


def register():
    bpy.utils.register_class(MATERIALS_OT_DropToFace)
    bpy.utils.register_class(MATERIALS_PT_ListMaterials)

def unregister():
    bpy.utils.unregister_class(MATERIALS_OT_DropToFace)
    bpy.utils.unregister_class(MATERIALS_PT_ListMaterials)

if __name__ == "__main__":
    register()
