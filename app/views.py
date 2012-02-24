# Create your views here.
from app.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from bootstrap.forms import BootstrapModelForm, Fieldset
import random

class SignupForm(BootstrapModelForm):
  class Meta:
    model = Student
    exclude = ('join_date', 'status',)

def index(request):
  
  context = {
      #'message': m,
  }
  return render_to_response('index.html', context)


def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      # Process the data in form.cleaned data
      form.save()
      return HttpResponse('ok')
      #return render_to_response('thanks.html', {})
  else:
    form = SignupForm()
  
  quiz = []
  for q in Quiz.objects.all():
    print q
    choices = [
          q.answer, 
          q.wrong1,
          q.wrong2,
          q.wrong3,
          q.wrong4]
    random.shuffle(choices)
    question = {'question': q.question, 
        'choices': choices,
        'answer':q.answer
        }
    print question
    quiz.append(question)
    print quiz

  context = {
      'form': form,
      'quiz':quiz,
  }
  context_instance = RequestContext(request, context)
  return render_to_response('signup.html', context_instance)

def reserve(request):
  context = {

  }
  return render_to_response('reserve.html', context)

def thanks(request):
  return render_to_response('thanks.html', {})
