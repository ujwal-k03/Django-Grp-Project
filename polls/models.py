from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

def returnNone():
    no_users = User.objects.none()
    return no_users

class Poll(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    users_voted = models.ManyToManyField(User,related_name='usersvoted',default=returnNone)
    total_votes = models.IntegerField(default=0)
    no_of_options_to_be_selected = models.PositiveIntegerField(default=1)
    anonymous_poll = models.BooleanField(default=True)
    public_results = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    
class Choice(models.Model):
    parent_poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100,)
    vote_count = models.IntegerField(default=0)
    voted_by = models.ManyToManyField(User,default=returnNone)

    def __str__(self):
        return self.choice_text

