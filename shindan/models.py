import datetime
from django.db import models
from django.utils import timezone

class QuestionShindan(models.Model):
    questionShindan_title = models.CharField(max_length=200)
    questionShindan_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.questionShindan_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Answer(models.Model):
    question = models.ForeignKey(QuestionShindan, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.answer_text
