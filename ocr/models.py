from django.db import models

# Create your models here.
class IDInfo(models.Model):
    unique_id = models.CharField(max_length=64, unique=True)
    id_type = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    dob = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=10)
    valid_till = models.DateTimeField(default=None, null=True, blank=True)
    encrypted_id_number = models.CharField(max_length=1000)
    
    def __str__(self):
        return f"{self.id_type} - {self.name}"