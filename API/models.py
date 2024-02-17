from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name}-{self.user}"