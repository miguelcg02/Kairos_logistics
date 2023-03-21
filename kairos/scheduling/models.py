from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rol = models.IntegerField(blank=False)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        db_table = "profile"

    def __str__(self):
        return str(self.usuario.username)