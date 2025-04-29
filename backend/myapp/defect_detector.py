import open3d as o3d
import numpy as np
import os
import json
from datetime import datetime

class DefectDetector:
    @staticmethod
    def load_model(model_path):
        try:
            print(f"Attempting to load {model_path} as a mesh...")
            mesh = o3d.io.read_triangle_mesh(model_path)

            if mesh.is_empty():
                print(f"Warning: Mesh is empty. Trying to load as a point cloud...")
                return None, None, False
            else:
                point_cloud = mesh.sample_points_uniformly(number_of_points=10000)
                watertight = False
                print(f"Loaded mesh with {len(mesh.vertices)} vertices, {len(mesh.triangles)} triangles, watertight: {watertight}")
                return mesh, point_cloud, watertight
        except Exception as e:
            print(f"Error loading mesh: {e}")

        try:
            print(f"Attempting to load {model_path} as a point cloud...")
            point_cloud = o3d.io.read_point_cloud(model_path)
            if point_cloud.is_empty():
                raise ValueError("Failed to load as point cloud.")
            print(f"Loaded point cloud with {len(point_cloud.points)} points")
            return None, point_cloud, False  
        except Exception as e:
            print(f"Error loading point cloud: {e}")

        return None, None, False


    @staticmethod
    def detect_holes(mesh):
        if mesh is None:
            return []

        mesh.compute_vertex_normals()
        boundary_edges = mesh.get_non_manifold_edges()
        boundary_vertices = set()

        for edge in boundary_edges:
            boundary_vertices.add(edge[0])
            boundary_vertices.add(edge[1])

        boundary_vertices = list(boundary_vertices)

        if boundary_vertices:
            points = np.asarray([mesh.vertices[v] for v in boundary_vertices])
            center = np.mean(points, axis=0)

            defect = {
                "type": "hole",
                "severity": "medium" if len(boundary_vertices) > 20 else "low",
                "location": center.tolist(),
                "points_count": len(boundary_vertices)
            }

            return [defect]
        else:
            return []

    @staticmethod
    def detect_noise(point_cloud, std_ratio=None):
        if point_cloud is None:
            return []

        if std_ratio is None:
            std_ratio = 1.5 if len(point_cloud.points) > 50000 else 2.5

        _, ind = point_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=std_ratio)

        noise_indices = list(set(range(len(point_cloud.points))) - set(ind))

        if noise_indices:
            noise_points = np.asarray(point_cloud.points)[noise_indices]
            center = np.mean(noise_points, axis=0)

            defect = {
                "type": "noise",
                "severity": "high" if len(noise_indices) > 100 else "medium",
                "location": center.tolist(),
                "points_count": len(noise_indices)
            }

            return [defect]
        else:
            return []

    @staticmethod
    def detect_inconsistent_normals(mesh, angle_threshold=60):
        if mesh is None:
            return []

        mesh.compute_vertex_normals()
        normals = np.asarray(mesh.vertex_normals)

        inconsistent_indices = []
        for i in range(len(normals) - 1):
            dot_product = np.dot(normals[i], normals[i + 1])
            angle = np.arccos(np.clip(dot_product, -1.0, 1.0)) * 180 / np.pi
            if angle > angle_threshold:
                inconsistent_indices.append(i)

        if inconsistent_indices:
            inconsistent_points = np.asarray(mesh.vertices)[inconsistent_indices]
            center = np.mean(inconsistent_points, axis=0)

            defect = {
                "type": "inconsistent_normals",
                "severity": "high" if len(inconsistent_indices) > 100 else "medium",
                "location": center.tolist(),
                "points_count": len(inconsistent_indices)
            }

            return [defect]
        else:
            return []

    @staticmethod
    def detect_all_defects(mesh, point_cloud):
        defects = []
        if mesh:
            defects.extend(DefectDetector.detect_holes(mesh))
            defects.extend(DefectDetector.detect_inconsistent_normals(mesh))
        if point_cloud:
            defects.extend(DefectDetector.detect_noise(point_cloud))
        return defects

    @staticmethod
    def save_defects_json(model_path, defects, watertight, output_path):
        result = {
            "model_path": model_path,
            "defect_count": len(defects),
            "watertight": watertight,
            "defects": defects,
            "timestamp": datetime.now().isoformat()
        }

        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

  