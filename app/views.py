# Create your views here.
from app.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django import forms


class SignupForm(forms.ModelForm):
  class Meta:
    model = Student

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
      return HttpResponseRedirect('/thanks/')
      #return render_to_response('thanks.html', {})
  else:
    form = SignupForm()

  context = {
      'form': form,
  }
  context_instance = RequestContext(request, context)
  return render_to_response('signup.html', context_instance)

def thanks(request):
  return render_to_response('thanks.html', {})

#def signup(request):
#  m = "Sign up for PennCycle"
#  form = SignupForm()
#  c = {}
#  c.update(csrf(request))
#  csrfContext = RequestContext(request)
#  c = {
#      'message': m,
#      'form': form,
#  }
#  c.update(csrf(request))
#  return render_to_response('signup.html', c)
