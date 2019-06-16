from rest_framework import serializers

from . import models


class TopicSerializer(serializers.ModelSerializer):
    """
    Topic serializer.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_firstname = serializers.ReadOnlyField(source='owner.first_name')
    owner_lastname = serializers.ReadOnlyField(source='owner.last_name')

    class Meta:
        model = models.Topic
        fields = ('id', 'title', 'description', 'date_started', 'done',
                  'owner', 'owner_firstname', 'owner_lastname')


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question serializer.
    """

    class Meta:
        model = models.TextAnswerableQuestion
        fields = '__all__'


class MultipleChoiceSerializer(serializers.ModelSerializer):
    """
    Multiple choice serializer.
    """
    choices = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.MultipleChoice
        fields = ('id', 'topic', 'text', 'multiple', 'choices')


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Choice serializer.
    """
    topic = serializers.ReadOnlyField(source='question.topic.id')

    class Meta:
        model = models.Choice
        fields = ('id', 'text', 'count', 'question', 'topic')


class IntervieweeSerializer(serializers.ModelSerializer):
    """
    Interviewee serializer.
    """

    class Meta:
        model = models.Interviewee
        fields = '__all__'
