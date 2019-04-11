from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

from . import models
from . import serializers
from . import permissions as perms


def get_or_create_interviewee(request, data):
    """Getting or creating the interviewee"""
    interviewee = models.Interviewee
    if request.user.is_authenticated:
        data['first_name'] = request.user.first_name
        data['last_name'] = request.user.last_name
    if models.Interviewee.objects.filter(
            first_name=data['first_name'], last_name=data['last_name']).exists():
        interviewee = get_object_or_404(
            models.Interviewee, first_name=data['first_name'],
            last_name=data['last_name'])
    else:
        interviewee = models.Interviewee(
            first_name=data['first_name'], last_name=data['last_name'])
        interviewee.save()
    return interviewee


def get_or_create_survey(topic, interviewee):
    """Getting or creating the survey"""
    survey = models.Survey
    if topic.survey_set.filter(interviewee=interviewee).exists():
        survey = topic.survey_set.get(interviewee=interviewee)
    else:
        survey = models.Survey(topic=topic, interviewee=interviewee)
        survey.save()
    return survey


class TopicViewSet(ModelViewSet):
    """Viewset for topics"""
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          perms.IsTopicOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['GET', 'POST'],
            serializer_class=serializers.QuestionSerializer)
    def questions(self, request, *args, **kwargs):
        """Extra action for listing all the topic's questions"""
        if request.method == 'GET':
            s = serializers.QuestionSerializer(
                self.get_object().textanswerablequestion_set.all(),
                context={'request': request}, many=True)
            return Response(data=s.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            q = models.TextAnswerableQuestion(
                topic=self.get_object(), text=request.data['text'])
            q.save()
            return Response(data=serializers.QuestionSerializer(q).data,
                            status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET', 'POST'],
            serializer_class=serializers.MultipleChoiceSerializer)
    def multiplechoices(self, request, *args, **kwargs):
        """Extra action for listing all the topic's
           multiple choice questions"""
        if request.method == 'GET':
            s = serializers.MultipleChoiceSerializer(
                self.get_object().multiplechoice_set.all(),
                context={'request': request}, many=True)
            return Response(data=s.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            q = models.MultipleChoice(
                topic=self.get_object(), text=request.data['text'])
            q.save()
            return Response(data=serializers.MultipleChoiceSerializer(q).data,
                            status=status.HTTP_201_CREATED)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    """View for displaying the question's detail"""
    queryset = models.TextAnswerableQuestion.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = (perms.IsTopicOwnerOrReadOnly,)
    lookup_field = 'id'

    def get_object(self):
        topic = get_object_or_404(models.Topic, id=self.kwargs['topic_id'])
        return topic.textanswerablequestion_set.get(id=self.kwargs['id'])


class MultipleChoiceDetail(generics.RetrieveUpdateDestroyAPIView):
    """View for displaying the multiple choice question's detail"""
    queryset = models.TextAnswerableQuestion.objects.all()
    serializer_class = serializers.MultipleChoiceSerializer
    permission_classes = (perms.IsTopicOwnerOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    lookup_field = 'id'

    def get_object(self):
        topic = get_object_or_404(models.Topic, id=self.kwargs['topic_id'])
        return topic.multiplechoice_set.get(id=self.kwargs['id'])


class ChoiceViewSet(ModelViewSet):
    queryset = models.Choice.objects.all()
    serializer_class = serializers.ChoiceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          perms.IsTopicOwnerOrReadOnly)

    def get_queryset(self):
        params = self.kwargs
        t = get_object_or_404(models.Topic, id=params['topic_id'])
        mc = t.multiplechoice_set.get(id=params['id'])
        return mc.choice_set.all()

    def get_object(self):
        params = self.kwargs
        t = get_object_or_404(models.Topic, id=params['topic_id'])
        mc = t.multiplechoice_set.get(id=params['mc_id'])
        return mc.choice_set.get(id=params['id'])

    def perform_create(self, serializer):
        params = self.kwargs
        t = get_object_or_404(models.Topic, id=params['topic_id'])
        mc = t.multiplechoice_set.get(id=params['id'])
        serializer.save(question=mc)

    @action(detail=True, methods=['POST'],
            serializer_class=serializers.IntervieweeSerializer)
    def choose(self, request, *args, **kwargs):
        data = request.data
        params = kwargs

        # Getting the topic
        topic = get_object_or_404(models.Topic, id=params['topic_id'])

        # Checking whether the topic is done
        if topic.done:
            return Response(data={'detail': 'The topic is already done.'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        # Getting the question
        question = topic.multiplechoice_set.get(id=params['mc_id'])

        # Getting the choice
        choice = question.choice_set.get(id=params['id'])

        # Getting the interviewee
        interviewee = get_or_create_interviewee(request, data)

        # Getting or creating the survey
        survey = get_or_create_survey(topic, interviewee)

        # Interviewee can only choose one if the question asks
        # for one choice only
        response_to_question_exists = models.MultipleResponse.objects.filter(
            survey=survey, question=question).exists()
        if not question.multiple and response_to_question_exists:
            return Response(data={'detail': 'You had choosen already.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Interviewee can only choose the choice once
        response_to_question_choice_exists = models.MultipleResponse.objects.filter(
            survey=survey, question=question, choice=choice).exists()
        if question.multiple and response_to_question_choice_exists:
            return Response(data={'detail': 'You had choosen this choice already.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Creates the response to the survey and question including the choice
        models.MultipleResponse.objects.create(
            survey=survey, question=question, choice=choice)

        # Finally increments the choice's count and saves it
        choice.count += 1
        choice.save()

        return Response(data=serializers.ChoiceSerializer(choice).data,
                        status=status.HTTP_201_CREATED)


class RespondToQuestionView(APIView):
    """View for responding to a question"""

    def post(self, request, *args, **kwargs):
        """POST is only available"""
        data = request.data
        params = kwargs

        # Getting the topic
        topic = get_object_or_404(models.Topic, id=params['topic_id'])

        # Checking whether the topic is done
        if topic.done:
            return Response(data={'detail': 'The topic is already done.'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        # Getting the question
        question = get_object_or_404(
            models.TextAnswerableQuestion, id=params['question'])

        # Getting the interviewee
        interviewee = get_or_create_interviewee(request, data)

        # Getting or creating the survey
        survey = get_or_create_survey(topic, interviewee)

        # Checks whether the interviewee had responded already to the question.
        # Creates the response if not.
        if models.TextResponse.objects.filter(survey=survey,
                                              question=question).exists():
            return Response(data={'detail': 'You have responded to this question '
                                            'already.'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            models.TextResponse.objects.create(
                survey=survey, question=question, text=data['text'])
            return Response(data={'detail': 'Response created.'},
                            status=status.HTTP_201_CREATED)
