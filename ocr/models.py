from django.db import models

# Create your models here.
class IDInfo(models.Model):
    id_type = models.CharField(max_length=10)
    id_number = models.CharField(max_length=12)
    name = models.CharField(max_length=100)
    dob = models.CharField(max_length=10)
    encrypted_id_number = models.CharField(max_length=1000)
    
    def __str__(self):
        return f"{self.id_type} - {self.name}"