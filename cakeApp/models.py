from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cakes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    flavour=models.CharField(max_length=200)
    weight=models.PositiveIntegerField()
    tier=models.PositiveIntegerField()
    colour=models.CharField(max_length=150)
    price=models.PositiveIntegerField()
    image=models.ImageField(upload_to="images", null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name