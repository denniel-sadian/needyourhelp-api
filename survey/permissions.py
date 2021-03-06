from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from . import models


class IsTopicOwnerOrReadOnly(BasePermission):
    """
    Is the user the topic owner, or is it read only?
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if type(obj) == models.Topic:
            return obj.owner == request.user
        elif type(obj) == models.Choice:
            return obj.question.topic.owner == request.user
        elif type(obj) in [models.TextAnswerableQuestion,
                           models.MultipleChoice]:
            return obj.topic.owner == request.user


class IsAbleToCreateOrChoose(BasePermission):
    """
    Is the user able to create or choose?
    """

    def has_permission(self, request, view):
        topic = get_object_or_404(models.Topic, id=view.kwargs['topic_id'])
        if 'id' in view.kwargs:
            return True
        if request.method not in SAFE_METHODS:
            return request.user == topic.owner
        return True


class IsOwnerOrTopicDone(BasePermission):
    """
    Is the user the owner or is the topic done?
    """
    message = "The survey isn't yet done or you're not the topic owner."

    def has_permission(self, request, view):
        topic_id = view.kwargs['topic_id']
        topic = get_object_or_404(models.Topic, id=topic_id)
        if topic.owner == request.user:
            return True
        return topic.done
