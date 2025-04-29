from django.db import models

from django.contrib.auth.models import User

class ModelFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)

    vertices_count = models.PositiveIntegerField(default=0)
    faces_count = models.PositiveIntegerField(default=0)

    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)  


    def __str__(self):
        return f"{self.file_name} by {self.user.username}"
    

class DefectAnalysis(models.Model):
    model_file = models.ForeignKey(ModelFile, on_delete=models.CASCADE, related_name="analyses")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')])
    report_path = models.CharField(max_length=500, blank=True, null=True)  
    defect_count = models.PositiveIntegerField(default=0)
    details = models.JSONField(blank=True, null=True) 
    is_watertight = models.BooleanField(default=False)
    defect_data = models.JSONField(default=dict) 
    task_id = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return f"Analysis of {self.model_file.file_name} - {self.status}"



class Report(models.Model):
    defect_analysis = models.ForeignKey(DefectAnalysis, on_delete=models.CASCADE, related_name="reports")
    generated_at = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(
        max_length=10, 
        choices=[('pdf', 'PDF'), ('excel', 'Excel')],
        default='pdf'
    )
    file_path = models.CharField(max_length=500, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Report for {self.defect_analysis.model_file.file_name} ({self.report_type.upper()})"






