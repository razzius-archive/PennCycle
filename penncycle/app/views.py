# Create your views here.
from app.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from bootstrap.forms import BootstrapModelForm, Fieldset
import random, json, hashlib, hmac

class SignupForm(BootstrapModelForm):
  class Meta:
    model = Student
    exclude = ('join_date', 'status', 'waiver_signed', 'paid',)

class InfoSubmitForm(forms.ModelForm):
  class Meta:
    model = Student
    exclude = ('join_date', 'status', 'waiver_signed', 'paid',)

def pages():
  pages = [
    {'name':'Home','url':'../../'},
    {'name':'Sign Up','url':'../../signup/'},
    ]
  for page in Page.objects.all():
    pages.append({
      'name': page.name,
      'url': '../../about/%s/' % page.slug
      })
  return pages

def index(request):
  
  context = {
      'pages':pages()
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
      
def page(request, slug):
  page = get_object_or_404(Page, slug=slug)
  context = {'page':page}
  context.update({'pages':pages()})
  return render_to_response('page.html', context)

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
  
  safety_info = Page.objects.get(slug='safety')
  
  context = {
      'safety_info': safety_info,
      'form': form,
  }
  context.update({'pages':pages()})
  context_instance = RequestContext(request, context)
  return render_to_response('signup.html', context_instance)

def verify_payment(request):
  print "in verify_payment"
  # gets the student with penncard specified in POST data
  student = Student.objects.get(penncard_number=request.GET.get('merchantDefinedData1'))
  print student

  source = request.META.get('HTTP_REFERER')
  print 'referrer is %s ' % source
  source_needed = 'https://orderpage.ic3.com/hop/orderform.jsp'
  
  amount = int(request.GET.get('amount', 0))
  print amount
  
  # add in test that amount is $10
  
  # if source matches CyberSource, payment completed
  if source == source_needed and (int(request.GET.get('reasonCode')) == (100 or 200)) and amount == .01:
    student.paid = True
    student.save()
    print "paid"
    # return render_to_response('thanks.html', {})
  # else:
    # return render_to_response('paymentfailed.html', {})
  return HttpResponse('Verifying...')

def thanks(request):
  print "in thanks view"
  student = Student.objects.get(penncard_number=request.GET.get('ordernumber'))
  print student

  if student.paid == true:
    return render_to_respone('thanks.html', {})
  else
    return HttpResponse('Something went wrong with your payment')

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
