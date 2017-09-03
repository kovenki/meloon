import datetime
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import QuestionDiagnosis


class QuestionDiagnosisModelTests(TestCase):

    def test_was_published_recently_with_future_questionDiagnosis(self):
        """
        was_published_recently() returns False for questionDiagnosiss whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_questionDiagnosis = QuestionDiagnosis(pub_date=time)
        self.assertIs(future_questionDiagnosis.was_published_recently(), False)
    def test_was_published_recently_with_old_questionDiagnosis(self):
        """
        was_published_recently() returns False for questionDiagnosiss whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_questionDiagnosis = QuestionDiagnosis(pub_date=time)
        self.assertIs(old_questionDiagnosis.was_published_recently(), False)

    def test_was_published_recently_with_recent_questionDiagnosis(self):
        """
        was_published_recently() returns True for questionDiagnosiss whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_questionDiagnosis = QuestionDiagnosis(pub_date=time)
        self.assertIs(recent_questionDiagnosis.was_published_recently(), True)

#-------
def create_questionDiagnosis(questionDiagnosis_text, days):
    """
    Create a questionDiagnosis with the given `questionDiagnosis_text` and published the
    given number of `days` offset to now (negative for questionDiagnosiss published
    in the past, positive for questionDiagnosiss that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return QuestionDiagnosis.objects.create(questionDiagnosis_text=questionDiagnosis_text, pub_date=time)


class QuestionDiagnosisIndexViewTests(TestCase):
    def test_no_questionDiagnosiss(self):
        """
        If no questionDiagnosiss exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('diagnosis:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No diagnosis are available.")
        self.assertQuerysetEqual(response.context['latest_questionDiagnosis_list'], [])

    def test_past_questionDiagnosis(self):
        """
        QuestionDiagnosiss with a pub_date in the past are displayed on the
        index page.
        """
        create_questionDiagnosis(questionDiagnosis_text="Past questionDiagnosis.", days=-30)
        response = self.client.get(reverse('diagnosis:index'))
        self.assertQuerysetEqual(
            response.context['latest_questionDiagnosis_list'],
            ['<QuestionDiagnosis: Past questionDiagnosis.>']
        )

    def test_future_questionDiagnosis(self):
        """
        QuestionDiagnosiss with a pub_date in the future aren't displayed on
        the index page.
        """
        create_questionDiagnosis(questionDiagnosis_text="Future questionDiagnosis.", days=30)
        response = self.client.get(reverse('diagnosis:index'))
        self.assertContains(response, "No diagnosis are available.")
        self.assertQuerysetEqual(response.context['latest_questionDiagnosis_list'], [])

    def test_future_questionDiagnosis_and_past_questionDiagnosis(self):
        """
        Even if both past and future questionDiagnosiss exist, only past questionDiagnosiss
        are displayed.
        """
        create_questionDiagnosis(questionDiagnosis_text="Past questionDiagnosis.", days=-30)
        create_questionDiagnosis(questionDiagnosis_text="Future questionDiagnosis.", days=30)
        response = self.client.get(reverse('diagnosis:index'))
        self.assertQuerysetEqual(
            response.context['latest_questionDiagnosis_list'],
            ['<QuestionDiagnosis: Past questionDiagnosis.>']
        )

    def test_two_past_questionDiagnosiss(self):
        """
        The questionDiagnosiss index page may display multiple questionDiagnosiss.
        """
        create_questionDiagnosis(questionDiagnosis_text="Past questionDiagnosis 1.", days=-30)
        create_questionDiagnosis(questionDiagnosis_text="Past questionDiagnosis 2.", days=-5)
        response = self.client.get(reverse('diagnosis:index'))
        self.assertQuerysetEqual(
            response.context['latest_questionDiagnosis_list'],
            ['<QuestionDiagnosis: Past questionDiagnosis 2.>', '<QuestionDiagnosis: Past questionDiagnosis 1.>']
        )
class QuestionDiagnosisDetailViewTests(TestCase):
    def test_future_questionDiagnosis(self):
        """
        The detail view of a questionDiagnosis with a pub_date in the future
        returns a 404 not found.
        """
        future_questionDiagnosis = create_questionDiagnosis(questionDiagnosis_text='Future questionDiagnosis.', days=5)
        url = reverse('diagnosis:detail', args=(future_questionDiagnosis.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_questionDiagnosis(self):
        """
        The detail view of a questionDiagnosis with a pub_date in the past
        displays the questionDiagnosis's text.
        """
        past_questionDiagnosis = create_questionDiagnosis(questionDiagnosis_text='Past QuestionDiagnosis.', days=-5)
        url = reverse('diagnosis:detail', args=(past_questionDiagnosis.id,))
        response = self.client.get(url)
        self.assertContains(response, past_questionDiagnosis.questionDiagnosis_text)
