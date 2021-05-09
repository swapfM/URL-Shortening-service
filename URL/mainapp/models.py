from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class shorty(models.Model):
    long_url = models.URLField( blank = False)
    short_url = models.CharField(blank = False , max_length = 8)
    visits = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
