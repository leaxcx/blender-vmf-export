bl_info = {
    "name": "VMF Exporter",
    "blender": (3, 6, 0),
    "category": "Export",
}

import bpy
import math
import mathutils

def apply_modifiers_to_obj(obj):
    for modifier in obj.modifiers:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=modifier.name)
        
def separate_loose_parts(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')

def calculate_uv_scale(obj, mesh, face):
    default_uv_scale = 0.25
    
    if obj.get("useMeshUV") == 1:
        if not mesh.uv_layers:
            return default_uv_scale

        uv_layer = mesh.uv_layers.active.data
        uvs = [uv_layer[loop_index].uv for loop_index in face.loop_indices]

        uv_width = max(uv.x for uv in uvs) - min(uv.x for uv in uvs)
        uv_height = max(uv.y for uv in uvs) - min(uv.y for uv in uvs)

        uv_scale = (uv_width + uv_height) / 2 if (uv_width + uv_height) > 0 else default_uv_scale
        
        return uv_scale
    
    return default_uv_scale

def rename_objects_in_collection(collection, start_id):
    id = start_id
    for obj in collection.objects:
        if obj.type == 'MESH':
            obj.name = f"brush_{id}"
            id += 1

class ExportVMFOperator(bpy.types.Operator):
    bl_idname = "export.vmf"
    bl_label = "Export VMF"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.vmf_export_settings
        write_vmf(settings.filepath, rename_objects=settings.rename_objects)
        return {'FINISHED'}

def write_vmf(filepath, rename_objects):
    scene = bpy.context.scene
    
    collection_name = "brushes"
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"Collection '{collection_name}' not found!")
        return

    if rename_objects:
        rename_objects_in_collection(collection, start_id=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        id = 1
        
        f.write('world\n')
        f.write('{\n')
        f.write('\t"id" "1"\n')
        f.write('\t"skyname" "sky_day01_01"\n')
        f.write('\t"maxpropscreenwidth" "-1"\n')
        f.write('\t"detailvbsp" "detail.vbsp"\n')
        f.write('\t"detailmaterial" "detail/detailsprites"\n')
        f.write('\t"mapversion" "68"\n')
        f.write('\t"classname" "worldspawn"\n')

        for obj in bpy.context.scene.objects:
            if obj.type == 'EMPTY':
                id += 1
                f.write('\tentity\n\t{\n')
                f.write('\t\t"id" "{}"\n'.format(id))
                f.write('\t\t"origin" "{} {} {}"\n'.format(*obj.location)) 
                f.write('\t\t"angles" "{} {} {}"\n'.format(*obj.rotation_euler)) 
                if obj.name == "info_player_start":
                    f.write('\t\t"classname" "info_player_start"\n')
                f.write('\t}\n')
                
            if collection.name in [collection.name for collection in obj.users_collection]:
                if obj.type == 'MESH':
                    id += 1
                        
                    apply_modifiers_to_obj(obj)
                
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                
                    separate_loose_parts(obj)

                    f.write('\tsolid\n\t{\n')
                    f.write('\t\t"id" "{}"\n'.format(id))
                        
                    mesh = obj.data

                    for face in mesh.polygons:
                        f.write('\t\tside\n\t\t{\n')
                        id += 1
                        f.write('\t\t\t"id" "{}"\n'.format(id))
                            
                        v1_world = obj.matrix_world @ mesh.vertices[face.vertices[0]].co
                        v2_world = obj.matrix_world @ mesh.vertices[face.vertices[1]].co
                        v3_world = obj.matrix_world @ mesh.vertices[face.vertices[2]].co

                        coords1 = (v1_world.x, -v1_world.y, v1_world.z)
                        coords2 = (v2_world.x, -v2_world.y, v2_world.z)
                        coords3 = (v3_world.x, -v3_world.y, v3_world.z)

                        f.write('\t\t\t"plane" "({:.6f} {:.6f} {:.6f}) ({:.6f} {:.6f} {:.6f}) ({:.6f} {:.6f} {:.6f})"\n'.format(*coords1, *coords2, *coords3))
                            
                        f.write('\t\t\tvertices_plus\n\t\t\t{\n')
                        f.write('\t\t\t\t"v" "({:.6f} {:.6f} {:.6f})"\n'.format(*coords1))
                        f.write('\t\t\t\t"v" "({:.6f} {:.6f} {:.6f})"\n'.format(*coords2))
                        f.write('\t\t\t\t"v" "({:.6f} {:.6f} {:.6f})"\n'.format(*coords3))
                        f.write('\t\t\t}\n')

                        material_name = "dev/dev_blendmeasure"
                        if obj.material_slots and face.material_index < len(obj.material_slots):
                            material = obj.material_slots[face.material_index].material
                            if material:
                                material_name = material.name.upper()

                        f.write('\t\t\t"material" "{}"\n'.format(material_name))
                            
                        uv_scale = calculate_uv_scale(obj, mesh, face)
                        normal = face.normal
                        if abs(normal.z) < 0.1:
                            f.write('\t\t\t"uaxis" "[0 1 0 0] {:.6f}"\n'.format(uv_scale))
                            f.write('\t\t\t"vaxis" "[0 0 -1 0] {:.6f}"\n'.format(uv_scale))
                        else:
                            f.write('\t\t\t"uaxis" "[1 0 0 0] {:.6f}"\n'.format(uv_scale))
                            f.write('\t\t\t"vaxis" "[0 -1 0 0] {:.6f}"\n'.format(uv_scale))
                        if abs(normal.y) > 0.9:
                            f.write('\t\t\t"uaxis" "[1 0 0 0] {:.6f}"\n'.format(uv_scale))
                            f.write('\t\t\t"vaxis" "[0 0 -1 0] {:.6f}"\n'.format(uv_scale))
                        f.write('\t\t\t"rotation" "0"\n')
                        f.write('\t\t\t"lightmapscale" "16"\n')
                        f.write('\t\t\t"smoothing_groups" "0"\n')
                            
                        f.write('\t\t}\n')
                        
                    f.write('\t}\n')

        f.write('}\n')

class VMFExportSettings(bpy.types.PropertyGroup):
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Path to save the VMF file",
        default="//",
        subtype='FILE_PATH'
    )
    rename_objects: bpy.props.BoolProperty(
        name="Rename Objects to ID",
        description="Rename objects in the collection 'brushes' to their ID",
        default=True
    )

class VMFExportPanel(bpy.types.Panel):
    bl_label = "Export Scene to VMF"
    bl_idname = "PT_VMF_Export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Level Editor'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.vmf_export_settings

        layout.prop(settings, "filepath")
        layout.prop(settings, "rename_objects")
        layout.operator("export.vmf", text="Export VMF")

def register():
    bpy.utils.register_class(ExportVMFOperator)
    bpy.utils.register_class(VMFExportSettings)
    bpy.utils.register_class(VMFExportPanel)
    bpy.types.Scene.vmf_export_settings = bpy.props.PointerProperty(type=VMFExportSettings)

def unregister():
    bpy.utils.unregister_class(ExportVMFOperator)
    bpy.utils.unregister_class(VMFExportSettings)
    bpy.utils.unregister_class(VMFExportPanel)
    del bpy.types.Scene.vmf_export_settings

if __name__ == "__main__":
    register()

