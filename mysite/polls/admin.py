from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 5


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ("pub_date", "question_text")
    search_fields = ("question_text", "pub_date")
    ordering = ("pub_date",)
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "choice_text", "votes")
    list_filter = ("question", "votes",)
    search_fields = ("choice_text", "votes")


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)

