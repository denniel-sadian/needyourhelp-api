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


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    """View for displaying the question's detail"""
    queryset = models.TextAnswerableQuestion.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = (perms.IsTopicOwnerOrReadOnly,)
    lookup_field = 'id'

    def get_object(self):
        topic = get_object_or_404(models.Topic, id=self.kwargs['topic_id'])
        return topic.textanswerablequestion_set.get(id=self.kwargs['id'])


class RespondToQuestionView(APIView):
    """View for responding to a question"""

    def post(self, request, *args, **kwargs):
        """POST is only available"""
        data = request.data
        params = kwargs

        # Getting the topic and question
        topic = get_object_or_404(models.Topic, id=params['topic'])
        question = get_object_or_404(
            models.TextAnswerableQuestion, id=params['question'])

        # Getting or creating the interviewee
        interviewee = models.Interviewee
        if models.Interviewee.objects.filter(
                first_name=data['first_name'], last_name=data['last_name']).exists():
            interviewee = get_object_or_404(
                models.Interviewee, first_name=data['first_name'],
                last_name=data['last_name'])
        else:
            interviewee = models.Interviewee(
                first_name=data['first_name'], last_name=data['last_name'])
            interviewee.save()

        # Getting of creating the survey
        survey = models.Survey
        if topic.survey_set.filter(interviewee=interviewee).exists():
            survey = topic.survey_set.get(interviewee=interviewee)
        else:
            survey = models.Survey(topic=topic, interviewee=interviewee)
            survey.save()

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
