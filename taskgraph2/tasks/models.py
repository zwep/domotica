from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=100)
    depends_on = models.ManyToManyField('self', symmetrical=False, related_name='dependents', blank=True)
    color = models.CharField(max_length=7, default="#cccccc")  # Hex color

    def __str__(self):
        return self.name
