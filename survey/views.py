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

    @action(detail=True)
    def questions(self, request, *args, **kwargs):
        """Extra action for listing all the topic's questions"""
        s = serializers.QuestionSerializer(
            self.get_object().textanswerablequestion_set.all(),
            context={'request': request}, many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    """View for displaying the question's detail"""
    queryset = models.TextAnswerableQuestion.objects.all()
    serializer_class = serializers.QuestionSerializer
    lookup_field = 'id'


class RespondToQuestionView(APIView):
    """View for responding to a question"""

    def post(self, request, *args, **kwargs):
        """POST is only available"""
        data = request.data
        params = kwargs

        # Getting the topic and question
        topic = models.Topic.objects.get(id=params['topic'])
        question = models.TextAnswerableQuestion.objects.get(
            id=params['question'])

        # Getting or creating the interviewee and survey
        interviewee = models.Interviewee
        survey = models.Survey
        if models.Interviewee.objects.filter(
                first_name=data['first_name'], last_name=data['last_name']).exists():
            interviewee = models.Interviewee.objects.get(
                first_name=data['first_name'], last_name=data['last_name'])
            survey = topic.survey_set.get(interviewee=interviewee)
        else:
            interviewee = models.Interviewee(
                first_name=data['first_name'], last_name=data['last_name'])
            interviewee.save()
            survey = models.Survey(topic=topic, interviewee=interviewee)
            survey.save()

        # Checks whether the interviewee had responded already to the question.
        # Creates the response if not.
        if models.TextResponse.objects.filter(survey=survey,
                                              question=question).exists():
            return Response(data={'detail': 'You have responded to this question '
                                            'already'},
                            status=status.HTTP_200_OK)
        else:
            models.TextResponse.objects.create(
                survey=survey, question=question, text=data['text'])

        return Response(data={'detail': 'Response created.'},
                        status=status.HTTP_201_CREATED)
