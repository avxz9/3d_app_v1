from celery import shared_task
from .models import DefectAnalysis, ModelFile
import open3d as o3d
import time 
from .defect_detector import DefectDetector



def detect_defects(model_path):

    mesh, point_cloud, watertight = DefectDetector.load_model(model_path)

    if mesh is None and point_cloud is None:
        return {"error": "Failed to load the model file."}

    defects = DefectDetector.detect_all_defects(mesh, point_cloud)


    return {
        "defect_count": len(defects),
        "is_watertight": watertight,
        "defects": defects 
    }

@shared_task(bind=True)
def analyze_model_file(self, model_file_id):
    print(f"Task started for model_file_id: {model_file_id}, Task ID: {self.request.id}")

    try:
        model_file = ModelFile.objects.get(id=model_file_id)
        print(f"Model file found: {model_file.file_name}")

        analysis, created = DefectAnalysis.objects.get_or_create(
            model_file=model_file,
            defaults={'status': 'pending', 'task_id': self.request.id}
        )

        if not created:
            analysis.status = "processing"
            analysis.task_id = self.request.id
            analysis.save()

        print("Starting defect detection...")
        result = detect_defects(model_file.file_path)

        if "error" in result:
            analysis.status = "failed"
            analysis.error_message = result["error"]
            analysis.save()
            print(f"Task failed: {result['error']}")
            return {"error": result["error"], "analysis_id": analysis.id}

        analysis.defect_count = result["defect_count"]
        analysis.defect_data = result["defects"]
        analysis.is_watertight = result["is_watertight"]
        analysis.status = "completed"
        analysis.save()

        print(f"Task completed successfully: {analysis.id}")
        return {"status": "completed", "analysis_id": analysis.id}

    except ModelFile.DoesNotExist:
        print(f"Model file not found for ID: {model_file_id}")
        return {"error": "Model file not found"}

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e)}


    
    