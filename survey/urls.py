from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'survey'

router = DefaultRouter()
router.register('topics', views.TopicViewSet)

choice_list = views.ChoiceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
choice_detail = views.ChoiceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('', include(router.urls)),

    path('topics/<int:topic_id>/questions/<int:id>/',
         views.QuestionDetail.as_view(), name='textanswerablequestion-detail'),

    path('topics/<int:topic_id>/multiplechoices/<int:id>/',
         views.MultipleChoiceDetail.as_view(), name='multiplechoice-detail'),

    path('topics/<int:topic_id>/multiplechoices/<int:id>/choices/',
         choice_list, name='choice-list'),

    path('topics/<int:topic_id>/multiplechoices/<int:mc_id>/choices/<int:id>/',
         choice_detail, name='choice-detail'),

    path('topics/<int:topic_id>/multiplechoices/<int:mc_id>/choices/<int:id>/choose/',
         views.ChoiceViewSet.as_view({
             'post': 'choose'
         }), name='choose-choice'),

    path('topics/<int:topic_id>/questions/<int:question>/respond/',
         views.RespondToQuestionView.as_view(), name='question-respond'),
     
    path('topics/<int:topic_id>/responded/',
         views.RespondedToQuestionView.as_view(), name='responded-already'),

    path('topics/<int:topic_id>/results/',
         views.ResultView.as_view(), name='topic-results'),

    path('create-interviewee/',
         views.IntervieweeCreateView.as_view(),
         name='create-interviewee')
]
