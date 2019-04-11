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
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TextAnswerableQuestion
        fields = '__all__'


class MultipleChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MultipleChoice
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    topic = serializers.ReadOnlyField(source='question.topic.id')

    class Meta:
        model = models.Choice
        fields = ('id', 'text', 'count', 'question', 'topic')


class IntervieweeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Interviewee
        fields = '__all__'
