from django.contrib import admin

from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['pub_date']
    search_fields = ['question_text','question_title']
    fieldsets = [
        (None,               {'fields': ['question_title','question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_title','question_text', 'pub_date', 'was_published_recently')


admin.site.register(Question, QuestionAdmin)
