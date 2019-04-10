from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_started = models.DateField(auto_now=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TextAnswerableQuestion(models.Model):
    topic = models.ForeignKey(to=Topic, on_delete=models.PROTECT)
    text = models.TextField()

    def __str__(self):
        return self.text


class Interviewee(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Survey(models.Model):
    topic = models.ForeignKey(to=Topic, on_delete=models.PROTECT)
    interviewee = models.ForeignKey(to=Interviewee, on_delete=models.PROTECT)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.interviewee} to {self.topic}'


class TextResponse(models.Model):
    survey = models.ForeignKey(to=Survey, on_delete=models.PROTECT)
    question = models.ForeignKey(
        to=TextAnswerableQuestion, on_delete=models.PROTECT)
    text = models.TextField()

    def __str__(self):
        return self.text
