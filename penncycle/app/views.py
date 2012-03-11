# Create your views here.
from app.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from bootstrap.forms import BootstrapModelForm, Fieldset
import random, json, hashlib

class SignupForm(BootstrapModelForm):
  class Meta:
    model = Student
    exclude = ('join_date', 'status', 'quiz_completed', 'waiver_signed', 'paid',)

class InfoSubmitForm(forms.ModelForm):
  class Meta:
    model = Student
    exclude = ('join_date', 'status', 'quiz_completed', 'waiver_signed', 'paid',)

def index(request):
  
  context = {
      #'message': m,
  }
  return render_to_response('index.html', context)

def info_submit(request):
  if request.method == 'POST':
    print "its a post!"
    form = SignupForm(request.POST)
    print form
    if form.is_valid():
      print "shit is validd"
      form.save()
      reply = {'success': True, 'form_valid': True}
    else:
      print "INVALID bullshit"
      reply = {'success': True,
               'form_valid': False,
               'new_form': str(form)}
    return HttpResponse(json.dumps(reply), content_type="application/json")
      

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

def verify_payment(request):
  if request.method == 'POST':
    print "received POST from pay server"
    # gets the student with penncard specified in POST data
    stu = Student.objects.get(Penncard=request.POST.get('ordernumber'))

    # generate token from penncard number and shared password
    token = hmac.new("uPENNBIK3S!", request.POST.get('ordernumber'), hashlib.sha256).hexdigest()

    # if token matches with token from CyberPay, payment completed
    if(token == request.POST.get('token'))
      stu.paid = True
      stu.save()
      return render_to_response('thanks.html', {})
    else
      return render_to_response('paymentfailed.html', {})

'''
def payment(request):
   if request.method == 'POST':
    print "posted form from payment"
    form = SignupForm(request.POST)
    print form
    if form.is_valid():
      print "this code should be unreachable"
    else:
      print "invalid form as expected"
      penncard = form.cleaned_data['Penncard']
      print "penncard = " + penncard 
      reply = {'success': True,
               'form_valid': False,
               'penncard': penncard,}
    return HttpResponse(json.dumps(reply), content_type="application/json")
'''
'''
def reserve(request):
  context = {

  }
  return render_to_response('reserve.html', context)

def thanks(request):
  return render_to_response('thanks.html', {})
 '''
