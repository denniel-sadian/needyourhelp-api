from django.contrib import admin

from . import models


class TextAnswerableQuestionInline(admin.StackedInline):
    model = models.TextAnswerableQuestion
    extra = 0


class ChoiceInline(admin.StackedInline):
    model = models.Choice
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'description', 'date_started', 'done')
    inlines = [TextAnswerableQuestionInline]


class MultipleChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'multiple')
    inlines = [ChoiceInline]


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('topic', 'interviewee', 'date')


class IntervieweeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


class TextResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'question', 'text')


class MultipleResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'question', 'choice')


admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Survey, SurveyAdmin)
admin.site.register(models.Interviewee, IntervieweeAdmin)
admin.site.register(models.TextResponse, TextResponseAdmin)
admin.site.register(models.MultipleResponse, MultipleResponseAdmin)
admin.site.register(models.MultipleChoice, MultipleChoiceAdmin)
