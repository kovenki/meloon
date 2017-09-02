from django.contrib import admin

from .models import Answer, QuestionShindan

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionShindanAdmin(admin.ModelAdmin):
    list_filter = ['pub_date']
    search_fields = ['questionShindan_text','questionShindan_title']
    fieldsets = [
        (None,               {'fields': ['questionShindan_title','questionShindan_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [AnswerInline]
    list_display = ('questionShindan_title','questionShindan_text', 'pub_date', 'was_published_recently')


admin.site.register(QuestionShindan, QuestionShindanAdmin)
