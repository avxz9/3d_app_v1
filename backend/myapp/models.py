from django.db import models

from django.contrib.auth.models import User

class ModelFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)

    """
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    """
    def __str__(self):
        return f"{self.file_name} by {self.user.username}"
