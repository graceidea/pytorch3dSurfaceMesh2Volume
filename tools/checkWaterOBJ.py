import numpy as np


def load_obj_file(file_path):
    vertices = []
    triangles = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertices.append([float(v) for v in line.strip().split()[1:]])
            elif line.startswith('f '):
                triangles.append([int(i.split('/')[0]) for i in line.strip().split()[1:]])
    return vertices, triangles

def calculate_triangle_normal(vertices, triangle):
    v1_idx, v2_idx, v3_idx = triangle
    try:
        v1 = np.array(vertices[triangle[0] - 1])
        v2 = np.array(vertices[triangle[1] - 1])
        v3 = np.array(vertices[triangle[2] - 1])

        edge1 = v2 - v1
        edge2 = v3 - v1
        normal = np.cross(edge1, edge2)
        normal /= np.linalg.norm(normal)

        return normal
    except IndexError:
        print("Error: Triangle indices out of range:", triangle)
        return None

def are_faces_oriented(vertices, triangles):
    # Calculate the normal of the first triangle
    reference_normal = calculate_triangle_normal(vertices, triangles[0])
    
    if reference_normal is None:
        return False

    # Check if the normals of all triangles are consistent with the reference normal
    for triangle in triangles[1:]:
        normal = calculate_triangle_normal(vertices, triangle)
        if normal is None or not np.allclose(normal, reference_normal):
            return False        
        #if not np.allclose(normal, reference_normal):
         #   return False
    return True

def is_water_tight(vertices, triangles):
    # Dictionary to store the adjacent triangles for each edge
    edge_to_triangles = {}

    # Populate the dictionary with edges and adjacent triangles
    for triangle in triangles:
        for i in range(3):
            edge = tuple(sorted([triangle[i], triangle[(i + 1) % 3]]))
            if edge in edge_to_triangles:
                edge_to_triangles[edge].append(triangle)
            else:
                edge_to_triangles[edge] = [triangle]

    # Check if any edge is shared by more or fewer than two triangles
    for edge, adjacent_triangles in edge_to_triangles.items():
        if len(adjacent_triangles) != 2:
            return False

    return True


# Example usage
obj_file_path = '/home/mint/AI_Source/pytorch3d/YLTset/tools/merged.obj'  # Replace 'example.obj' with your OBJ file path
vertices, triangles = load_obj_file(obj_file_path)
if is_water_tight(vertices, triangles):
    print("The mesh /home/mint/AI_Source/pytorch3d/YLTset/tools/test.obj is water-tight.")
else:
    print("The mesh /home/mint/AI_Source/pytorch3d/YLTset/tools/test.obj is NOT water-tight.")
    
#obj_file_path = '/home/mint/AI_Source/pytorch3d/YLTset/tools/test.obj'  # Replace 'example.obj' with your OBJ file path    
if are_faces_oriented(vertices, triangles):
    print("The faces are consistently oriented.")
else:
    print("The faces are not consistently oriented.")
