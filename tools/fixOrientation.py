
import torch

def read_obj(file_path):
    vertices = []
    triangles = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = list(map(float, line.strip().split()[1:]))
                vertices.append(vertex)
            elif line.startswith('f '):
                triangle = list(map(int, line.strip().split()[1:]))
                triangles.append(triangle)
    
    vertices = torch.tensor(vertices)
    triangles = torch.tensor(triangles) - 1  # Adjust indices to start from 0
    return vertices, triangles

def count_bad_orientations(vertices, triangles):
    num_bad_orientations = 0

    # Build an edge list
    edges = set()
    for triangle in triangles:
        for i in range(3):
            edge = (triangle[i], triangle[(i + 1) % 3])
            edges.add(tuple(sorted(edge)))

    # Count non-manifold edges
    for edge in edges:
        shared_triangles = [t for t in triangles if edge[0] in t and edge[1] in t]
        if len(shared_triangles) != 2:
            num_bad_orientations += 1

    return num_bad_orientations

# Example usage:
obj_file = "test.obj"
vertices, triangles = read_obj(obj_file)
bad_orientations = count_bad_orientations(vertices, triangles)
print("Number of bad orientations:", bad_orientations)











