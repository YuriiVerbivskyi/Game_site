from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default = "")
    founded = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    players = models.CharField(max_length = 10)
    duration = models.CharField(max_length = 10)
    price = models.PositiveIntegerField(default=0)
    genre = models.CharField(max_length=100)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='games')

    def __str__(self):
        return self.name

