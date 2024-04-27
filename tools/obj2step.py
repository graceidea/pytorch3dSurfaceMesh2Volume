
import numpy as np
import meshio

def obj_to_stl(obj_file, stl_file):
    # Load OBJ file
    vertices, faces = load_obj(obj_file)

    # Create mesh data
    mesh = meshio.Mesh(vertices, {'triangle': faces})

    # Write STL file
    meshio.write(stl_file, mesh, file_format='stl')

def load_obj(file_path):
    vertices = []
    faces = []

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                vertices.append([float(v) for v in line.strip().split()[1:]])
            elif line.startswith('f '):
                face_vertices = [int(vertex.split('/')[0]) - 1 for vertex in line.strip().split()[1:]]
                faces.append(face_vertices)

    return np.array(vertices), np.array(faces)

# Example usage
obj_file = 'input.obj'
stl_file = 'output.stl'
obj_to_stl(obj_file, stl_file)

