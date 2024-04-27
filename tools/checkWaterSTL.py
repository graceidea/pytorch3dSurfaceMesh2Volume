
import trimesh

def check_stl_watertight(stl_file):
    # Load STL file
    mesh = trimesh.load(stl_file)

    # Check if mesh is watertight
    watertight = mesh.is_watertight

    # Print result
    if watertight:
        print("The mesh is watertight.")
    else:
        print("The mesh is not watertight.")

# Example usage
stl_file = 'input.stl'
check_stl_watertight(stl_file)
