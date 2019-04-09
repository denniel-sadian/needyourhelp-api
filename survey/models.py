from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    date_started = models.DateField(auto_now=True)
    done = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Interviewee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_interviewed = models.DateField(auto_now=True)
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)


class Question(models.Model):
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE)


class Response(models.Model):
    date_responded = models.DateField(auto_now=True)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    by = models.ForeignKey(to=Interviewee, on_delete=models.CASCADE)


class TextAnswerable(Question):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Opinion(Response):
    text = models.CharField(max_length=255)


"""
class MultipleChoice(Question):
    text = models.CharField(max_length=255)
    choose_all = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Choice(Response):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
"""
