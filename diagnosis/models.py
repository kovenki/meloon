import datetime
from django.db import models
from django.utils import timezone
from django import forms


class QuestionDiagnosis(models.Model):
    questionDiagnosis_title = models.CharField(max_length=200)
    questionDiagnosis_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.questionDiagnosis_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Hint(models.Model):
    questionDiagnosis = models.ForeignKey(QuestionDiagnosis, on_delete=models.CASCADE)
    hint_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.hint_text
