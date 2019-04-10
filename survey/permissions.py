"""
from rest_framework import permissions

from .models import Survey
from .models import TextAnswerable


class IsOwnerOrReadOnly(permissions.BasePermission):
    
Custom permission to only allow owners of an object to edit it.


    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class IsTextAnswerableCreatorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            Survey.objects.get(
                id=view.kwargs['survey_id']).user == request.user
        )


class IsTextAnswerableEditableOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        ta = TextAnswerable.objects.get(id=view.kwargs['pk'])
        return ta.survey.user == request.user

"""
from rest_framework import permissions
from . import models


class IsTopicOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if type(obj) == models.Topic:
            return obj.owner == request.user
        elif type(obj) == models.TextAnswerableQuestion:
            return obj.topic.owner == request.user
