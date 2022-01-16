import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    closed_at = models.DateTimeField("date closed", default=timezone.now() + timezone.timedelta(weeks=1))
    max_choices = models.IntegerField(default=5)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def is_closed(self):
        return self.closed_at >= timezone.now()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

    def was_created_recently(self):
        return self.created_on >= timezone.now() - datetime.timedelta(days=1)


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, related_name='replies')

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
