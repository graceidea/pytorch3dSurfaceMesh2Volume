import trimesh

def make_watertight(obj_file_path, output_file_path):
    # Load the non-water-tight mesh
    mesh = trimesh.load(obj_file_path)
    
    # Check if the mesh is watertight
    if mesh.is_watertight:
        print("Mesh is already watertight.")
        return
    
    # Attempt to fill holes
    mesh_filled = mesh.fill_holes()

    # Check if the mesh is watertight after filling holes
    if not mesh_filled.is_watertight:
        print("Failed to make mesh watertight by filling holes.")
        return
    
    # Save the watertight mesh
    mesh_filled.export(output_file_path)

    print("Watertight mesh saved successfully.")

# Example usage
obj_file_path = "/home/mint/AI_Source/pytorch3d/YLTset/surfaceMeshModels/test.obj"
output_file_path = "watertight.obj"
make_watertight(obj_file_path, output_file_path)
