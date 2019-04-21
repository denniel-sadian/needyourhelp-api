from django.contrib import admin

from . import models


def delete_all(model_admin, request, queryset):
    if queryset.count() > 0:
        deleted = 0
        for i in queryset:
            i.delete()
            deleted += 1
        model_admin.message_user(
            request, f'{deleted} item{" has" if deleted is 1 else "s have"} '
                     'been deleted.')


delete_all.short_description = 'Delete all selected'


class TextAnswerableQuestionInline(admin.StackedInline):
    model = models.TextAnswerableQuestion
    extra = 0


class ChoiceInline(admin.StackedInline):
    model = models.Choice
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'description', 'date_started', 'done')
    inlines = [TextAnswerableQuestionInline]
    actions = [delete_all]


class MultipleChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'multiple')
    inlines = [ChoiceInline]
    actions = [delete_all]


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('topic', 'interviewee', 'date')
    actions = [delete_all]


class IntervieweeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    actions = [delete_all]


class TextResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'question', 'text')
    actions = [delete_all]


class MultipleResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'question', 'choice')
    actions = [delete_all]


admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Survey, SurveyAdmin)
admin.site.register(models.Interviewee, IntervieweeAdmin)
admin.site.register(models.TextResponse, TextResponseAdmin)
admin.site.register(models.MultipleResponse, MultipleResponseAdmin)
admin.site.register(models.MultipleChoice, MultipleChoiceAdmin)
