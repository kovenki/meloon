from django.contrib import admin

from .models import Hint, QuestionDiagnosis

class HintInline(admin.TabularInline):
    model = Hint
    extra = 3


class QuestionDiagnosisAdmin(admin.ModelAdmin):
    list_filter = ['pub_date']
    search_fields = ['questiondiagnosis_text','questiondiagnosis_title']
    fieldsets = [
        (None,               {'fields': ['questiondiagnosis_title','questiondiagnosis_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [HintInline]
    list_display = ('questiondiagnosis_title','questiondiagnosis_text', 'pub_date', 'was_published_recently')


admin.site.register(QuestionDiagnosis, QuestionDiagnosisAdmin)
