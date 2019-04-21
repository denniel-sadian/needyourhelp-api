from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    date_started = models.DateField(auto_now=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TextAnswerableQuestion(models.Model):
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class MultipleChoice(models.Model):
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE)
    text = models.TextField()
    multiple = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(to=MultipleChoice, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Interviewee(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        unique_together = ('first_name', 'last_name')


class Survey(models.Model):
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE)
    interviewee = models.ForeignKey(to=Interviewee, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.interviewee} to {self.topic}'
    
    class Meta:
        unique_together = ('topic', 'interviewee')


class TextResponse(models.Model):
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(
        to=TextAnswerableQuestion, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class MultipleResponse(models.Model):
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(
        to=MultipleChoice, on_delete=models.CASCADE)
    choice = models.ForeignKey(to=Choice, on_delete=models.CASCADE)
