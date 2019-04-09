from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

from .permissions import IsOwnerOrReadOnly
from .serializers import SurveySerializer
from .serializers import TextAnswerableSerializer
from .serializers import OpinionSerializer
from .serializers import IntervieweeSerializer
from .models import Survey
from .models import TextAnswerable
from .models import Interviewee
from .models import Opinion


class SurveyViewSet(ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TextAnswerableListCreateView(generics.ListCreateAPIView):
    serializer_class = TextAnswerableSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get_queryset(self):
        queryset = TextAnswerable.objects.filter(
            survey_id=self.kwargs["survey_id"])
        return queryset

    def perform_create(self, serializer):
        serializer.save(survey=Survey.objects.get(id=self.kwargs['survey_id']))


class TextAnswerableDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TextAnswerableSerializer
    queryset = TextAnswerable.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TextAnswerableRespond(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data.get('last_name'))
        ta = TextAnswerable.objects.get(id=self.kwargs['pk'])
        if Interviewee.objects.filter(
                first_name=data.get('first_name'),
                last_name=data.get('last_name')).exists():
            return Response({'details': 'You responded already.'},
                            status=status.HTTP_403_FORBIDDEN)
        i = Interviewee(first_name=data.get('first_name'),
                        last_name=data.get('last_name'),
                        survey=ta.survey)
        i.save()
        o = Opinion(text=data.get('text'), question=ta, by=i)
        o.save()
        return Response({'details': OpinionSerializer(o).data},
                        status=status.HTTP_201_CREATED)


class OpinionView(generics.ListAPIView):
    queryset = Opinion.objects.all()
    serializer_class = OpinionSerializer

    def get_queryset(self):
        return Opinion.objects.filter(question_id=self.kwargs['pk'])
