import bpy
import math
import mathutils

def apply_modifiers_to_obj(obj):
    # Apply all modifiers for the object
    for modifier in obj.modifiers:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=modifier.name)

def write_vmf(filepath):
    scene = bpy.context.scene
    
    collection_name = "brushes"
    # Add all of your geometry to "brushes" collection or it will not be ported!
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"Collection '{collection_name}' not found!")
        return

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

        for obj in scene.objects:
            # WIP: entities are not supported yet!
            if obj.type == 'EMPTY':
                id += 1
                f.write('\tentity\n\t{\n')
                f.write('\t\t"id" "{}"\n'.format(id))
                # Find origin
                f.write('\t\t"origin" "{} {} {}"\n'.format(*obj.location)) 
                # Find angles
                f.write('\t\t"angles" "{} {} {}"\n'.format(*obj.rotation_euler)) 
                # If name of entity you placed in Blender is:
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
                            
                            # Transform vertex coordinates to world space
                            v1_world = obj.matrix_world @ mesh.vertices[face.vertices[0]].co
                            v2_world = obj.matrix_world @ mesh.vertices[face.vertices[1]].co
                            v3_world = obj.matrix_world @ mesh.vertices[face.vertices[2]].co

                            # Convert Blender coordinates to Valve (x, -y, z)
                            coords1 = (v1_world.x, -v1_world.y, v1_world.z)
                            coords2 = (v2_world.x, -v2_world.y, v2_world.z)
                            coords3 = (v3_world.x, -v3_world.y, v3_world.z)

                            # Write plane in Valve format
                            f.write('\t\t\t"plane" "({:.6f} {:.6f} {:.6f}) ({:.6f} {:.6f} {:.6f}) ({:.6f} {:.6f} {:.6f})"\n'.format(*coords1, *coords2, *coords3))
                            
                            # Write vertices_plus
                            f.write('\t\t\tvertices_plus\n\t\t\t{\n')
                            f.write('\t\t\t\t"v" "({:.6f} {:.6f} {:.6f})"\n'.format(*coords1))
                            f.write('\t\t\t\t"v" "({:.6f} {:.6f} {:.6f})"\n'.format(*coords2))
                            f.write('\t\t\t\t"v" "({:.6f} {:.6f} {:.6f})"\n'.format(*coords3))
                            f.write('\t\t\t}\n')

                            # Get the material name in uppercase
                            material_name = "dev/dev_blendmeasure"  # Default material
                            if obj.material_slots and face.material_index < len(obj.material_slots):
                                material = obj.material_slots[face.material_index].material
                                if material:
                                    material_name = material.name.upper()

                            f.write('\t\t\t"material" "{}"\n'.format(material_name))
                            
                            # U and V axis fix
                            normal = face.normal
                            # If face is mostly vertical
                            if abs(normal.z) < 0.1:  
                                f.write('\t\t\t"uaxis" "[0 1 0 0] 0.25"\n')
                                f.write('\t\t\t"vaxis" "[0 0 -1 0] 0.25"\n')
                            # Horizontal
                            else:  
                                f.write('\t\t\t"uaxis" "[1 0 0 0] 0.25"\n')
                                f.write('\t\t\t"vaxis" "[0 -1 0 0] 0.25"\n')
                            # Left and right
                            if abs(normal.y) > 0.9:  
                                f.write('\t\t\t"uaxis" "[1 0 0 0] 0.25"\n')
                                f.write('\t\t\t"vaxis" "[0 0 -1 0] 0.25"\n')
                            f.write('\t\t\t"rotation" "0"\n')
                            f.write('\t\t\t"lightmapscale" "16"\n')
                            f.write('\t\t\t"smoothing_groups" "0"\n')
                            
                            f.write('\t\t}\n')
                        
                        f.write('\t}\n')

        f.write('}\n')

# Set your filepath here
if __name__ == "__main__":
    filepath = r"E:/Projects/blender-vmf-export/files/.vmf/file1.vmf"
    write_vmf(filepath) 
