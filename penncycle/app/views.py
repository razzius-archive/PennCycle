# Create your views here.
from django.core.mail import send_mail
from app.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from bootstrap.forms import BootstrapModelForm, Fieldset
import random, json, hashlib, hmac
from app.docs import addPerson

class SignupForm(BootstrapModelForm):
  class Meta:
    model = Student
    exclude = ('join_date', 'status', 'waiver_signed', 'paid', 'last_two', 'payment_type', 'at_desk')

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
  available = Bike.objects.filter(status='available')
  context = {
    'available': available,
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
      print "saved form"
      reply = {'success': True, 'form_valid': True}
    else:
      print "INVALID bullshit"
      reply = {'success': True,
               'form_valid': False,
               'new_form': str(form)}
    print reply
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

@csrf_exempt
def verify_payment(request):
  if request.method=='POST':
    print "in verify_payment"
    # gets the student with penncard specified in POST data
    student = Student.objects.get(penncard=request.POST.get('merchantDefinedData1'))
    print student

    source = request.META.get('HTTP_REFERER')
    print 'referrer is %s ' % source
    source_needed = 'https://orderpage.ic3.com/hop/orderform.jsp'
    
    amount = str(request.POST.get('orderAmount', 0))
    print amount
    
    # add in test that amount is $10
    
    # if source matches CyberSource, payment completed
    #if source == source_needed and (int(request.POST.get('reasonCode')) == (100 or 200)) and amount == .01:
    reasonCode = request.POST.get('reasonCode')
    good_reasons = [100,200]
    print reasonCode
    if (int(reasonCode) in good_reasons) and (amount == '10.00' or amount == '10'):
      print "check passed"
      student.paid = True
      student.payment_type = 'credit'
      student.save()
      print "paid"
    return HttpResponse('Verifying...')
  else:
    return HttpResponse('Not a POST')

@csrf_exempt
def thankyou(request, penncard):
  print "in thanks view"
  student = get_object_or_404(Student, penncard=penncard)
  #student = Student.objects.get(penncard=request.POST.get('merchantDefinedData1'))
  print student
  type = request.GET.get('type', 'credit')
  if type == 'penncash' or type == 'bursar':
    message = '''Please allow up to 48 hours for your payment to be registered
      (but we'll try hard to be as fast as possible!). 
      </p><p> You will not be able to check out a bike until the payment has registered successfully.'''
  elif type == 'cash':
    message = "Once you've paid and your payment has been registered, you'll be good to go!"
  elif student.paid == True:
    message = 'You\'re ready to ride!'
  else:
    message = 'Something went wrong with your payment. Please email us at messenger@penncycle.org.'
  return render_to_response('thanks.html', {'message':message})

def verify_waiver(request):
  print 'in verify_waiver'
  if request.method=='POST':
    print 'its a post'
    pennid = request.POST.get('pennid')
    print pennid
    student = Student.objects.get(penncard=pennid)
    print student
    student.waiver_signed = True
    student.save()
    print 'waiver signed'
    return HttpResponse(json.dumps({'message': 'success'}), content_type="application/json")
  return HttpResponse('failure')

def pay(request, type, penncard):
  if request.method == 'POST':
    type = str(request.POST.get('type')).lower()
    print type
    print penncard
    student = get_object_or_404(Student, penncard=penncard) # verify form is filled out well!
    print student
    last_two = request.POST.get('last_two')
    print last_two
    student.last_two = last_two
    #student.payment_type = type
    student.save()
    print 'saved'
    message = '''
      Name: %s \n
      PennCard: %s \n
      Last Two Digits: %s \n
      Type: %s \n
      
      bill them and remember to check 'paid'! 
      Thanks d00d >.<
    ''' % (student.name, student.penncard, student.last_two, type)
    send_mail('Student Registered w/ %s' % (type), message, 
      'messenger@penncycle.org', ['messenger@penncycle.org'], fail_silently=False)
    addPerson(student.name, student.penncard, student.last_two, type) # adds to the google spreadsheet
    return HttpResponseRedirect('../../../thankyou/%s/?type=%s' % (penncard, type))
  else: 
    print type
    student = Student.objects.get(penncard=penncard)
    student.payment_type = type
    student.save()
    context = {
      'type': type,
      'penncard': penncard,
      'student': student,
    }
    return render_to_response('pay.html', RequestContext(request, context))
