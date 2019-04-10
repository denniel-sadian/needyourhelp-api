"""
from rest_framework import serializers

from .models import Survey
from .models import TextAnswerable
from .models import Opinion
from .models import Interviewee


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Survey
        fields = ('url', 'id', 'title', 'description', 'done',
                  'first_name', 'last_name', 'email')


class TextAnswerableSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TextAnswerable
        fields = ('id', 'text')


class OpinionSerializer(serializers.ModelSerializer):
    by = serializers.ReadOnlyField(source='by.full_name')

    class Meta:
        model = Opinion
        fields = ('text', 'by', 'date_responded')


class IntervieweeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interviewee
        fields = ('first_name', 'last_name')
"""
from rest_framework import serializers

from . import models


class TopicSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = models.Topic
        fields = ('id', 'title', 'description',
                  'date_started', 'done', 'owner')


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TextAnswerableQuestion
        fields = ('id', 'text', 'topic')
