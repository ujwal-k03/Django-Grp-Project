from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Poll(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.title

class Choice(models.Model):
    parent_poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

