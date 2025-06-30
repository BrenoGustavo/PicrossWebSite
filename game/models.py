from django.db import models
from django.utils import timezone

class Puzzle(models.Model):
    date = models.DateField(default=timezone.now, unique=True)
    solution = models.TextField()  # matriz 0 e 1 em JSON
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(default=10)

    def __str__(self):
        return f"Puzzle de {self.date}"