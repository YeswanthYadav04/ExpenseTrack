from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):

    TYPE_CHOICES = [
        ('income','Income'),
        ('expense','Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.FloatField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title