"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('surveys', views.SurveyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('surveys/<int:survey_id>/textanswerables/',
         views.TextAnswerableListCreateView.as_view(), name='textanswerable-list'),
    path('textanswerables/<int:pk>/',
         views.TextAnswerableDetail.as_view(), name='textanswerable-detail'),
    path('textanswerables/<int:pk>/respond/',
         views.TextAnswerableRespond.as_view(), name='textanswerable-respond'),
    path('textanswerables/<int:pk>/responses/',
         views.OpinionView.as_view(), name='textanswerable-responses')
]

"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('topics', views.TopicViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('topics/<int:topic_id>/questions/<int:id>/', views.QuestionDetail.as_view(),
         name='textanswerablequestion-detail'),
    path('topics/<int:topic>/questions/<int:question>/respond/',
         views.RespondToQuestionView.as_view(), name='question-respond'),
]
