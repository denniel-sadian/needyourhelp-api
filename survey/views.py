from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

from . import models
from . import serializers
from . import permissions as perms


def get_or_create_interviewee(request, data):
    """Getting or creating the interviewee."""
    interviewee = models.Interviewee
    firstname = ''
    lastname = ''

    # Uses the authenticated user's credentials.
    names_not_present = (
        'first_name' not in data and 'last_name' not in data
    )
    if request.user.is_authenticated and names_not_present:
        firstname = request.user.first_name.lower()
        lastname = request.user.last_name.lower()
    else:
        firstname = data['first_name'].lower()
        lastname = data['last_name'].lower()

    # Checks if there's an interviewee already.
    # Creates it if none yet.
    if models.Interviewee.objects.filter(
            first_name=firstname, last_name=lastname).exists():
        interviewee = get_object_or_404(
            models.Interviewee, first_name=firstname,
            last_name=lastname)
    else:
        interviewee = models.Interviewee(
            first_name=firstname, last_name=lastname)
        interviewee.save()

    return interviewee


def get_or_create_survey(topic, interviewee):
    """Getting or creating the survey."""
    survey = models.Survey

    # Gets or creates the survey for the topic and interviewee.
    if topic.survey_set.filter(interviewee=interviewee).exists():
        survey = topic.survey_set.get(interviewee=interviewee)
    else:
        survey = models.Survey(topic=topic, interviewee=interviewee)
        survey.save()
    return survey


class TopicViewSet(ModelViewSet):
    """Viewset for topics."""
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          perms.IsTopicOwnerOrReadOnly)

    def perform_create(self, serializer):
        """Saves the user as the owner."""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['GET', 'POST'],
            serializer_class=serializers.QuestionSerializer)
    def questions(self, request, *args, **kwargs):
        """Extra action for listing all or creating
           topic's questions."""
        if request.method == 'GET':
            questions = (
                self.get_object().textanswerablequestion_set.all())
            serializer = serializers.QuestionSerializer(
                questions, many=True)
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        elif request.method == 'POST':
            question = models.TextAnswerableQuestion(
                topic=self.get_object(), text=request.data['text'])
            question.save()
            serializer = serializers.QuestionSerializer(question)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET', 'POST'],
            serializer_class=serializers.MultipleChoiceSerializer)
    def multiplechoices(self, request, *args, **kwargs):
        """Extra action for listing all the topic's
           multiple choice questions."""
        if request.method == 'GET':
            questions = self.get_object().multiplechoice_set.all()
            serializer = serializers.MultipleChoiceSerializer(
                questions, many=True)
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        elif request.method == 'POST':
            question = models.MultipleChoice(
                topic=self.get_object(), text=request.data['text'])
            question.save()
            serializer = serializers.MultipleChoiceSerializer(question)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    """View for displaying the question's detail."""
    queryset = models.TextAnswerableQuestion.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = (perms.IsTopicOwnerOrReadOnly,)
    lookup_field = 'id'

    def get_object(self):
        """Gets the question from the topic's set."""
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
        """Gets the multiple choice from the topic's set."""
        topic = get_object_or_404(models.Topic, id=self.kwargs['topic_id'])
        return topic.multiplechoice_set.get(id=self.kwargs['id'])


class ChoiceViewSet(ModelViewSet):
    """Viewset for choices."""
    queryset = models.Choice.objects.all()
    serializer_class = serializers.ChoiceSerializer
    permission_classes = (perms.IsTopicOwnerOrReadOnly, perms.IsAbleToCreateOrChoose)

    def get_queryset(self):
        """Gets the choices from the question coming from the topic."""
        params = self.kwargs
        topic = get_object_or_404(models.Topic, id=params['topic_id'])
        question = topic.multiplechoice_set.get(id=params['id'])
        return question.choices.all()

    def get_object(self):
        """Gets the choice from the question coming from the topic."""
        params = self.kwargs
        topic = get_object_or_404(models.Topic, id=params['topic_id'])
        question = topic.multiplechoice_set.get(id=params['mc_id'])
        return question.choices.get(id=params['id'])

    def perform_create(self, serializer):
        """Gets the question from the topic then saves it with
           the choice from the serializer."""
        params = self.kwargs
        topic = get_object_or_404(models.Topic, id=params['topic_id'])
        question = topic.multiplechoice_set.get(id=params['id'])
        serializer.save(question=question)

    @action(detail=True, methods=['POST'],
            serializer_class=serializers.IntervieweeSerializer)
    def choose(self, request, *args, **kwargs):
        """Extra action for choosing the choice."""
        data = request.data
        params = kwargs

        # Getting the topic
        topic = get_object_or_404(models.Topic, id=params['topic_id'])

        # Limits whether the topic is done.
        if topic.done:
            return Response(data={'detail': 'The topic is already done.'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        # Getting the question.
        question = topic.multiplechoice_set.get(id=params['mc_id'])

        # Getting the choice.
        choice = question.choices.get(id=params['id'])

        # Getting the interviewee.
        interviewee = get_or_create_interviewee(request, data)

        # Getting or creating the survey.
        survey = get_or_create_survey(topic, interviewee)

        # Interviewee can only choose one if the question asks
        # for one choice only.
        response_to_question_exists = models.MultipleResponse.objects.filter(
            survey=survey, question=question).exists()
        if not question.multiple and response_to_question_exists:
            return Response(data={'detail': 'You had choosen already.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Interviewee can only choose the choice once.
        response_to_question_choice_exists = models.MultipleResponse.objects.filter(
            survey=survey, question=question, choice=choice).exists()
        if question.multiple and response_to_question_choice_exists:
            return Response(data={'detail': 'You had choosen this choice already.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Creates the response which is used for determining whether
        # the interviewee had chosen the choice already.
        models.MultipleResponse.objects.create(
            survey=survey, question=question, choice=choice)

        # Finally increments the choice's count and saves it.
        choice.count += 1
        choice.save()

        return Response(data=serializers.ChoiceSerializer(choice).data,
                        status=status.HTTP_201_CREATED)


class RespondToQuestionView(APIView):
    """View for responding to a question."""

    def post(self, request, *args, **kwargs):
        """POST is only available."""
        data = request.data
        params = kwargs

        # Getting the topic.
        topic = get_object_or_404(models.Topic, id=params['topic_id'])

        # Limiting the interviewee if the topic is done.
        if topic.done:
            return Response(data={'detail': 'The topic is already done.'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        # Getting the question.
        question = get_object_or_404(
            models.TextAnswerableQuestion, id=params['question'])

        # Getting the interviewee.
        interviewee = get_or_create_interviewee(request, data)

        # Getting or creating the survey.
        survey = get_or_create_survey(topic, interviewee)

        # Checks whether the interviewee had responded already
        # to the question. Creates the response if not yet.
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


class ResultView(APIView):
    """View for viewing topics' results."""
    permission_classes = (perms.IsOwnerOrTopicDone,)

    def get(self, request, *args, **kwargs):
        """Get is only available."""
        params = kwargs
        results = {
            'respondents': set(),
            'total-respondents': int,
            'questions': [],
            'multiple-choice-questions': []
        }

        # Getting the topic.
        topic = get_object_or_404(models.Topic, id=params['topic_id'])

        # Getting the interviewees.
        for survey in models.Survey.objects.filter(topic=topic):
            results['respondents'].add(str(survey.interviewee).upper())
        results['total-respondents'] = len(results['respondents'])

        # Getting the answers to the questions.
        for question in topic.textanswerablequestion_set.all():
            answers = {'question': str(question), 'answers': []}
            for response in models.TextResponse.objects.filter(
                    question=question, survey__topic=topic):
                answers['answers'].append([{
                    'respondent': str(response.survey.interviewee).upper(),
                    'answer': response.text
                }])
            results['questions'].append(answers)

        # Getting the multiple choice questions.
        for multiple in topic.multiplechoice_set.all():
            question = {
                'question': str(multiple),
                'choose-all': multiple.multiple,
                'choices': []
            }
            # Getting the choices to the multiple choices.
            for choice in multiple.choices.all():
                item = {
                    'choice': str(choice),
                    'counts': choice.count,
                    'respondents-who-chose': set()
                }
                item['percent'] = round(
                    (choice.count*100) / results['total-respondents'], 2)
                # Getting those respondents who chose the choices.
                for response in models.MultipleResponse.objects.filter(
                        question=multiple, survey__topic=topic, choice=choice):
                    item['respondents-who-chose'].add(
                        str(response.survey.interviewee).upper())
                question['choices'].append(item)
            results['multiple-choice-questions'].append(question)

        return Response(data=results, status=status.HTTP_200_OK)
