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
    owner_firstname = serializers.ReadOnlyField(source='owner.first_name')
    owner_lastname = serializers.ReadOnlyField(source='owner.last_name')

    class Meta:
        model = models.Topic
        fields = ('id', 'title', 'description', 'date_started', 'done',
                  'owner', 'owner_firstname', 'owner_lastname')


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TextAnswerableQuestion
        fields = '__all__'


class MultipleChoiceSerializer(serializers.ModelSerializer):
    choices = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.MultipleChoice
        fields = ('id', 'topic', 'text', 'multiple', 'choices')


class ChoiceSerializer(serializers.ModelSerializer):
    topic = serializers.ReadOnlyField(source='question.topic.id')

    class Meta:
        model = models.Choice
        fields = ('id', 'text', 'count', 'question', 'topic')


class IntervieweeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Interviewee
        fields = '__all__'
