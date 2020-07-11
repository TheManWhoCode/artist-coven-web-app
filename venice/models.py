from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
class UserGallery(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    artwork = models.BinaryField()