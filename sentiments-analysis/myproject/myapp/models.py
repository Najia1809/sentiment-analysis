from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



class Sentence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    sentiment = models.CharField(max_length=10, default="normal")  # Lowercase 'sentiment' for consistency
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username}: {self.text[:50]} - ({self.sentiment})"






