# Create your views here.
from app.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django import forms
from bootstrap.forms import BootstrapModelForm, Fieldset

#class SignupForm(forms.ModelForm):
class SignupForm(BootstrapModelForm):
  class Meta:
    model = Student
    #layout = (
      #Fieldset("Please Login", "Name", "Email", "Phone", "Penncard", "Gender", "Grad year", "Height", "School", "Major" ),
    #)

    #Name = forms.CharField(max_length=100)
    #Email = forms.CharField(max_length=100)
    #Phone = forms.CharField(max_length=100)
    #Penncard = forms.CharField(max_length=100)


def index(request):
  m = 'Sign up <a href="#">here</a>'
  
  context = {
      'message': m,
  }
  return render_to_response('index.html', context)

#class LoginForm(BootstrapForm):
#    class Meta:
#        layout = (
#            Fieldset("Please Login", "username", "password", ),
#        )

#    username = forms.CharField(max_length=100)
#    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)


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
