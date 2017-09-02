from django.shortcuts import render
from django.shortcuts import render_to_response
# Create your views here.
from django.http import HttpResponse
from .forms import KakikomiForm
from django.urls import reverse

def kakikomi(request):
     f = KakikomiForm()
     return HttpResponse(f.as_table())
