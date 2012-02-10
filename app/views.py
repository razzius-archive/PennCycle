# Create your views here.
from app.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django import forms
from bootstrap.forms import BootstrapModelForm, Fieldset
import random

#class SignupForm(forms.ModelForm):
class SignupForm(BootstrapModelForm):
  class Meta:
    model = Student
    exclude = ('join_date', 'status',)

def index(request):
  m = 'Sign up <a href="#">here</a>'
  
  context = {
      'message': m,
  }
  return render_to_response('index.html', context)


def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      # Process the data in form.cleaned data
      form.save()
      return HttpResponseRedirect('#video')
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

def thanks(request):
  return render_to_response('thanks.html', {})
