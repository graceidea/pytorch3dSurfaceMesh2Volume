import numpy as np
from pytorch3d.io import load_obj

def compute_face_normals(vertices, faces):
    # Extract vertices of each face
    face_vertices = vertices[faces]
    # Compute edges of each face
    edge1 = face_vertices[:, 1] - face_vertices[:, 0]
    edge2 = face_vertices[:, 2] - face_vertices[:, 0]
    # Compute face normals as cross product of edges
    face_normals = np.cross(edge1, edge2)
    # Normalize the normals
    face_normals /= np.linalg.norm(face_normals, axis=1, keepdims=True)
    return face_normals

def count_outward_normals(vertices, faces, face_normals):
    # Compute the centroid of each face
    centroids = vertices[faces[:, 0]].mean(axis=1)
    # Compute vectors from the centroid to each vertex of the face
    to_centroid = centroids[:, None] - vertices[faces[:, 0]]
    # Compute the dot product between the face normals and the vectors to centroid
    dot_products = np.einsum("ij,ij->i", face_normals, to_centroid)
    # Get the indices of faces with outward normals (negative dot products)
    outward_faces = np.where(dot_products < 0)[0]
    return outward_faces

def reverse_outward_faces(vertices, faces, outward_faces):
    # Create a new array to store reversed vertices
    reversed_faces = np.empty_like(faces)
    # Loop through outward faces and swap the order of vertices
    for idx in outward_faces:
        # Swap the order of vertices for each face
        reversed_faces[idx] = faces[idx][[0, 2, 1]]

    return reversed_faces

def write_obj(filename, vertices, faces):
    with open(filename, 'w') as f:
        for v in vertices:
            f.write("v {:.6f} {:.6f} {:.6f}\n".format(v[0], v[1], v[2]))
        for face in faces:
            f.write("f {} {} {}\n".format(face[0] + 1, face[1] + 1, face[2] + 1))

def main():
    # Load the OBJ file
    verts, faces, _ = load_obj("test.obj")
    # Compute face normals
    face_normals = compute_face_normals(verts, faces.verts_idx)
    # Find outward faces
    outward_faces = count_outward_normals(verts, faces.verts_idx, face_normals)
    # Reverse the order of vertices for outward faces
    reversed_faces = reverse_outward_faces(verts, faces.verts_idx, outward_faces)
    # Write the corrected faces to OBJ file
    write_obj("merged.obj", verts, reversed_faces)

if __name__ == "__main__":
    main()
