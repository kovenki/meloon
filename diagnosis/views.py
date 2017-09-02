from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Hint, QuestionDiagnosis, KakikomiForm
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse



class IndexView(generic.ListView):
    template_name = 'diagnosis/index.html'
    context_object_name = 'latest_question_list'
#    def get_queryset(self):
#        """Return the last five published questions."""
#        return QuestionDiagnosis.objects.order_by('-pub_date')[:5]
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return QuestionDiagnosis.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = QuestionDiagnosis
    template_name = 'diagnosis/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return QuestionDiagnosis.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = QuestionDiagnosis
    template_name = 'diagnosis/results.html'



def vote(request, questionDiagnosis_id):
    questionDiagnosis = get_object_or_404(QuestionDiagnosis, pk=questionDiagnosis_id)
    try:
        selected_hint = questionDiagnosis.hint_set.get(pk=request.POST['hint'])
    except (KeyError, Hint.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'diagnosis/detail.html', {
            'questionDiagnosis': questionDiagnosis,
            'error_message': "エラー：何も選択されていません。",
        })
    else:
        selected_hint.votes += 1
        selected_hint.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('diagnosis:results', args=(questionDiagnosis.id,)))
