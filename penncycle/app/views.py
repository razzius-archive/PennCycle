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
import random, json, hashlib, hmac, gviz_api
from django.contrib.auth.decorators import login_required
from django.db.models import F
import datetime
#from app.docs import addPerson

class SignupForm(BootstrapModelForm):
  class Meta:
    model = Student
    exclude = ('join_date', 
                'status', 
                'waiver_signed', 
                'paid', 
                'last_two', 
                'payment_type', 
                'at_desk',
                'plan')

class InfoSubmitForm(forms.ModelForm):
  class Meta:
    model = Student
    exclude = ('join_date', 
                'status', 
                'waiver_signed', 
                'paid',)

def pages():
  pages = [
    {'name':'Home','url':'../../'},
    {'name':'Plans','url':'../../plans/'},
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
      student = form.save()
      living_location = student.living_location
      if living_location == 'Stouffer': 
        student.paid = True
        student.save()
        print "this student lives in stouffer"
        print str(student) + "; paid = " + str(student.paid)
      print "saved form"
      print "payment plan: " + str(student.plan)
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
      'plans': Plan.objects.filter(end_date__gte = datetime.date.today())
  }
  context.update({'pages':pages()})
  context_instance = RequestContext(request, context)
  return render_to_response('signup.html', context_instance)

@csrf_exempt
def verify_payment(request):
  if request.method=='POST':
    print "in verify_payment"
    print request.POST
    # gets the student with penncard specified in POST data
    payment = Payment.objects.get(id=request.POST.get('merchantDefinedData1'))
    student = payment.student
    print payment
    print student

    source = request.META.get('HTTP_REFERER')
    print 'referrer is %s ' % unicode(source)
    source_needed = 'https://orderpage.ic3.com/hop/orderform.jsp'
    
    amount = str(request.POST.get('orderAmount', 0))
    print amount
    costwtax = float(payment.plan.cost)*1.08
    print costwtax

    if float(amount) != costwtax:
      errmessage = 'student didn\'t pay the right amount! Payment: %s \n Amount: %d Cost+tax: %d' % (str(payment.id), float(amount),  costwtax)
      print errmessage
      email_alex(errmessage)
      return HttpResponse('eh okay.')
    else:
      # if source matches CyberSource, payment completed
      #if source == source_needed and (int(request.POST.get('reasonCode')) == (100 or 200)) and amount == .01:
      reasonCode = request.POST.get('reasonCode')
      good_reasons = [100,200]
      print reasonCode
      #if (int(reasonCode) in good_reasons) and (amount == '10.00' or amount == '10'):
      if (int(reasonCode) in good_reasons): 
        print "check passed"
        #student.paid = True
        payment.satisfied=True
        payment.payment_type = 'credit'
        payment.save()
        print "paid"
      return HttpResponse('Verified!')
  else:
    return HttpResponse('Not a POST')

@csrf_exempt
def thankyou(request, payment_id):
  print "in thanks view"
  try:
    payment = Payment.objects.get(id=payment_id)
    student = payment.student
  except:
    student = get_object_or_404(Student, penncard=payment_id)
  #student = Student.objects.get(penncard=request.POST.get('merchantDefinedData1'))
  print student
  type = request.GET.get('type', 'credit')
  if type == 'penncash' or type == 'bursar':
    message = '''Please allow up to 48 hours for your payment to be registered
      (but we'll try hard to be as fast as possible!). 
      </p><p> You will not be able to check out a bike until the payment has registered successfully.'''
  elif type == 'cash':
    message = "Once you've paid and your payment has been registered, you'll be good to go!"
  elif type == "credit":
    if payment.satisfied == True:
      message = 'You\'re ready to ride!'
    else:
      message = 'Whoops! Something went wrong with your payment. We\'ve been notified and will get on this right away'
      try:
        dog = payment.id
        email_alex('payment gone wrong! %s' % str(payment.id))
      except:
        email_alex('payment gone HORRIBLY wrong! (could not email you what the payment id was!) student is %s' % student)
  else:
    message = 'Something went wrong with your payment. Please email us at messenger@penncycle.org.'
  return render_to_response('thanks.html', {'message':message, 'pages':pages()})

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

def pay(request, type, penncard, plan):
  if request.method == 'POST':
    type = str(request.POST.get('type')).lower()
    print type
    print penncard
    print plan
    student = get_object_or_404(Student, penncard=penncard) # verify form is filled out well!
    print student
    last_two = request.POST.get('last_two')
    print last_two
    student.last_two = last_two
    #student.payment_type = type
    student.save()
    plan = get_object_or_404(Plan, id=plan)
    payment = Payment(
      amount=plan.cost,
      plan=plan,
      student=student,
      date=datetime.datetime.today(),
      satisfied=False,
      payment_type=type,
      )
    payment.save()
    print 'saved'
    message = '''
      Name: %s \n
      PennCard: %s \n
      Last Two Digits: %s \n
      Type: %s \n
      Plan: %s \n
      
      bill them and remember to check 'paid'! 
      Thanks d00d >.<
    ''' % (student.name, student.penncard, student.last_two, type, plan)
    send_mail('Student Registered w/ %s' % (type), message, 
      'messenger@penncycle.org', ['messenger@penncycle.org'], fail_silently=False)
    # addPerson(student.name, student.penncard, student.last_two, type) # adds to the google spreadsheet
    return HttpResponseRedirect('/thankyou/%s/?type=%s' % (penncard, type))
  else: 
    print type
    student = get_object_or_404(Student, penncard=penncard)
    student.payment_type = type
    student.save()
    context = {
      'type': type,
      'penncard': penncard,
      'student': student,
    }
    context.update({'pages':pages()})
    return render_to_response('pay.html', RequestContext(request, context))

@login_required
def stats(request):
  return render_to_response('stats.html', {'pages':pages()})

def selectpayment(request):
  plans = Plan.objects.filter(end_date__gte = datetime.date.today())
  print plans
  day_plan = Plan.objects.filter(end_date=datetime.date.today(), name__contains='Day Plan')
  if len(day_plan) < 1:
    print 'about to create a new day plan'
    day_plan = Plan(
      name = 'Day Plan %s' % str(datetime.date.today()),
      cost = 10,
      start_date = datetime.date.today(),
      end_date = datetime.date.today(),
      description = 'A great way to try out PennCycle. Or, use this to check out a bike for a friend or family member! Add more day plans to your account to check out more bikes. Day plans can only be purchased day-of.',
      )
    day_plan.save()
  elif len(day_plan) == 1:
    print 'there already was a day plan! how convenient.'
  print day_plan
  return render_to_response('selectpayment.html', {'plans': plans, 'pages':pages()})

def addpayment(request):
  print "in addpayment view"
  print request.POST
  pennid = unicode(request.POST.get('pennid'))
  print "pennid = " + str(pennid)
  associated_student = Student.objects.get(penncard=pennid)
  print associated_student
  plan_num = int(request.POST.get('plan'))
  print "plan num = " + str(plan_num)
  associated_plan = Plan.objects.get(pk=plan_num)
  print associated_plan
  new_payment = Payment(amount=associated_plan.cost, plan=associated_plan, student=associated_student)
  print new_payment
  new_payment.save()
  print "payment saved"

  return HttpResponse(json.dumps({'message': 'success', 'payment_id':str(new_payment.id)}), content_type="application/json")

def plans(request):
  print "hit plans view"
  # list of dicts
  plans = [] 
  for p in Plan.objects.exclude(end_date__lte=datetime.date.today()).order_by('start_date', 'cost'):
    plans.append({'name': str(p), 'description': p.description, 'start_date': p.start_date, 'end_date': p.end_date,})

  context = {
      'plans': plans,
      'pages': pages(),
  }
  print plans
  return render_to_response('plans.html', context)

def email_alex(message):
  send_mail('an important email from the PennCycle App', str(message), 'messenger@penncycle.org', ['rattray.alex@gmail.com'], fail_silently=True)
