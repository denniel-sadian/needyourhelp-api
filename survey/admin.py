from django.contrib import admin

from .models import Survey
from .models import Interviewee
from .models import TextAnswerable
from .models import Opinion
# from .models import MultipleChoice
# from .models import Choice


class IntervieweeAdmin(admin.ModelAdmin):
    list_display = ('date_interviewed', 'survey')


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_started', 'done', 'user')


class OpinionInline(admin.StackedInline):
    model = Opinion
    extra = 3


class TextAnswerableAdmin(admin.ModelAdmin):
    list_display = ('survey', 'text')
    inlines = [OpinionInline]


"""
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class MultipleChoiceAdmin(admin.ModelAdmin):
    list_display = ('survey', 'text')
    inlines = [ChoiceInline]
"""


admin.site.register(Survey, SurveyAdmin)
admin.site.register(TextAnswerable, TextAnswerableAdmin)
admin.site.register(Interviewee, IntervieweeAdmin)
# admin.site.register(MultipleChoice, MultipleChoiceAdmin)
