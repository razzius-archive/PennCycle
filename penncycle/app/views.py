import datetime
import json

from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bootstrap.forms import BootstrapModelForm
from models import *
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class SignupForm(BootstrapModelForm):
    class Meta:
        model = Student
        exclude = (
            'join_date',
            'status',
            'waiver_signed',
            'paid',
            'last_two',
            'payment_type',
            'staff',
            'plan',
            'major',
        )


pages = [
    {'name': 'Home', 'url': '/'},
    {'name': 'Plans', 'url': '/plans/'},
    {'name': 'Sign Up', 'url': '/signup/'},
    {'name': 'Safety', 'url': '/safety/'},
    {'name': 'Team', 'url': '/team/'},
    {'name': 'Partners', 'url': '/partners/'},
    {'name': 'Locations', 'url': '/locations/'},
    {'name': 'FAQ', 'url': '/faq/'},
]


def lookup(request):
    penncard = request.GET.get("penncard")
    context = {
        'pages': pages
    }
    try:
        student = Student.objects.get(penncard=penncard)
        context['student'] = student
        return render_to_response("welcome.html", RequestContext(request, context))
    except Student.DoesNotExist:
        messages.add_message(request, 20, "Fill out the form below to sign up!")
        return HttpResponseRedirect("/signup?penncard={}".format(penncard), RequestContext(request, context))


def welcome(request, student):
    return render_to_response("welcome.html", RequestContext(request, context))


def index(request):
    available = Bike.objects.filter(status='available')
    stoufferCount = sum((1 for bike in available if bike.location.name == "Stouffer"))
    psaCount = sum((1 for bike in available if bike.location.name == "PSA"))
    houstonCount = sum((1 for bike in available if bike.location.name == "Houston"))
    rodinCount = sum((1 for bike in available if bike.location.name == "Rodin"))
    wareCount = sum((1 for bike in available if bike.location.name == "Ware"))
    fisherCount = sum((1 for bike in available if bike.location.name == "Fisher"))
    context = {
        'available': available,
        'stoufferCount': stoufferCount,
        'rodinCount': rodinCount,
        'psaCount': psaCount,
        'wareCount': wareCount,
        'fisherCount': fisherCount,
        'houstonCount': houstonCount,
        'pages': pages
    }
    return render_to_response('index.html', RequestContext(request, context))


def faq(request):
    context = {
        'pages': pages
    }
    return render_to_response('faq.html', RequestContext(request, context))


def safety(request):
    context = {
        'pages': pages
    }
    return render_to_response('safety.html', RequestContext(request, context))


def team(request):
    context = {
        'pages': pages
    }
    return render_to_response('team.html', RequestContext(request, context))


def partners(request):
    context = {
        'pages': pages
    }
    return render_to_response('partners.html', RequestContext(request, context))


def locations(request):
    context = {
        'pages': pages,
        'stations': Station.objects.filter(capacity__gt=0).order_by("id")
    }
    return render_to_response('locations.html', RequestContext(request, context))


def plans(request):
    plans = Plan.objects.filter(end_date__gte=datetime.date.today(), cost__gt=0).order_by('start_date', 'cost')
    context = {
        'plans': plans,
        'pages': pages,
    }
    return render_to_response('plans.html', RequestContext(request, context))


@require_POST
def info_submit(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        form.save()
        reply = {
            'success': True,
            'form_valid': True
        }
    else:
        reply = {
            'success': True,
            'form_valid': False,
            'new_form': str(form)
        }
    return HttpResponse(json.dumps(reply), content_type="application/json")


def signup(request):
    penncard = request.GET.get("penncard")
    form = SignupForm(initial={'penncard': penncard})
    context = {
        'form': form,
        'plans': Plan.objects.filter(end_date__gte=datetime.date.today(), cost__gt=0),
        'pages': pages
    }
    return render_to_response('signup.html', RequestContext(request, context))


@require_POST
@csrf_exempt
def verify_payment(request):
    print "in verify_payment"
    email_razzi(request.POST)
    # gets the student with penncard specified in POST data
    payment = Payment.objects.get(id=request.POST.get('merchantDefinedData1'))
    # source = request.META.get('HTTP_REFERER')
    email_razzi(request.META)
    # source_needed = 'https://orderpage.ic3.com/hop/orderform.jsp'
    amount = str(request.POST.get('orderAmount', 0))
    costwtax = float(payment.plan.cost)*1.08
    if float(amount) != costwtax:
        errmessage = "student didn't pay the right amount! Payment: {} \n Amount: {} Cost+tax: {}".format(payment.id, amount, costwtax)
        email_razzi(errmessage)
        return HttpResponse('eh okay.')
    else:
        # if source matches CyberSource, payment completed
        # if source == source_needed and (int(request.POST.get('reasonCode')) == (100 or 200)) and amount == .01:
        reasonCode = request.POST.get('reasonCode')
        good_reasons = [100, 200]
        if (int(reasonCode) in good_reasons):
            payment.satisfied = True
            payment.payment_type = 'credit'
            payment.save()
        return HttpResponse('Verified!')


@csrf_exempt
def thankyou(request, payment_id):
    print "in thanks view"
    try:
        payment = Payment.objects.get(id=payment_id)
        student = payment.student
    except:
        student = get_object_or_404(Student, penncard=payment_id)
    payment_type = request.GET.get('payment_type', 'credit')
    if payment_type == 'penncash' or payment_type == 'bursar':
        message = '''Please allow up to 48 hours for your payment to be registered.
        </p><p> You can start checking out bikes immediately in the meantime. Visit our <a href="/locations">locations</a> page
        to view our stations and their hours.'''
    elif payment_type == 'cash':
        message = "Once you've paid and your payment has been registered, you'll be good to go!"
    elif payment_type == "credit":
        if payment.satisfied:
            message = "You're ready to ride!"
        else:
            message = 'Something went wrong with your payment. We\'ve been notified and will get on this right away.'
            try:
                email_razzi('payment gone wrong! %s' % str(payment.id))
            except:
                email_razzi('payment gone HORRIBLY wrong! (could not email you what the payment id was!) student is %s' % student)
    else:
        message = 'Something went wrong with your payment. Please email us at messenger@penncycle.org.'
    return render_to_response('thanks.html', RequestContext(request, {'message': message, 'pages': pages}))


@require_POST
def verify_waiver(request):
    print 'in verify_waiver'
    pennid = request.POST.get('pennid')
    print(request.POST)
    student = Student.objects.get(penncard=pennid)
    student.waiver_signed = True
    student.save()
    print 'waiver signed'
    return HttpResponse(json.dumps({'message': 'success'}), content_type="application/json")


def pay(request, payment_type, penncard, plan):
    if request.method == 'POST':
        payment_type = str(request.POST.get('payment_type')).lower()
        print("Pay <view></view>")
        try:
            student = Student.objects.get(penncard=penncard)  # verify form is filled out well!
        except:
            context = {
                'message': "No student matching that PennCard was found. Please try again, or sign up.",
                'payment_type': payment_type,
                'pages': pages
            }
            return render_to_response("pay.html", RequestContext(request, context))
        last_two = request.POST.get('last_two')
        student.last_two = last_two
        student.save()
        plan = get_object_or_404(Plan, id=plan)
        payment = Payment(
            amount=plan.cost,
            plan=plan,
            student=student,
            date=datetime.datetime.today(),
            satisfied=True,
            payment_type=payment_type,
        )
        payment.save()
        message = '''
            Name: %s \n
            PennCard: %s \n
            Last Two Digits: %s \n
            Type: %s \n
            Plan: %s \n

            Chris and Razzi deciced that it would be easier for students to have the ability
            to check out bikes immediately, so that students wouldn't have
            to wait for us to bill them and in case we forget, they can still ride.

            It is still necessary to bill them, and if this has a problem, go to the admin interface and remove their
            payment, then email them with what went wrong.

            Email razzi53@gmail.com if something goes wrong.

            Thanks!
        ''' % (student.name, student.penncard, student.last_two, payment_type, plan)
        send_mail('Student Registered w/ %s' % (payment_type), message, 'messenger@penncycle.org', ['messenger@penncycle.org'])
        return HttpResponseRedirect('/thankyou/{}/?payment_type={}'.format(penncard, payment_type))
    else:
        print("pay get")
        try:
            student = Student.objects.get(penncard=penncard)
            context = {
                'payment_type': payment_type,
                'penncard': penncard,
                'student': student,
                'pages': pages,
            }
        except:
            context = {
                'payment_type': payment_type,
                'penncard': penncard,
                'pages': pages,
                'message': "No student matching that PennCard was found. <a href='/signup'>Sign up</a> here.",
            }
        return render_to_response('pay.html', RequestContext(request, context))


@login_required
def stats(request):
    return render_to_response('stats.html', RequestContext(request, {'pages': pages}))


def selectpayment(request):
    plans = Plan.objects.filter(end_date__gte=datetime.date.today(), cost__gt=0)
    day_plan = Plan.objects.filter(end_date=datetime.date.today(), name__contains='Day Plan')
    if len(day_plan) < 1:
        day_plan = Plan(
            name='Day Plan %s' % str(datetime.date.today()),
            cost=8,
            start_date=datetime.date.today(),
            end_date=datetime.date.today(),
            description='A great way to try out PennCycle. Or, use this to check out a bike for a friend or family member! Add more day plans to your account to check out more bikes. Day plans can only be purchased day-of.',
        )
        day_plan.save()
    return render_to_response('selectpayment.html', RequestContext(request, {'plans': plans, 'pages': pages}))


@require_POST
def addpayment(request):
    print "in addpayment view"
    print request.POST
    pennid = unicode(request.POST.get('pennid'))
    print "pennid = " + str(pennid)
    try:
        associated_student = Student.objects.get(penncard=pennid)
    except:
        raise LookupError
    print associated_student
    plan_num = int(request.POST.get('plan'))
    print "plan num = " + str(plan_num)
    associated_plan = Plan.objects.get(pk=plan_num)
    print associated_plan
    new_payment = Payment(amount=associated_plan.cost, plan=associated_plan, student=associated_student)
    print new_payment
    new_payment.save()
    print "payment saved"

    return HttpResponse(json.dumps({'message': 'success', 'payment_id': str(new_payment.id)}), content_type="application/json")


def email_razzi(message):
    send_mail('an important email from the PennCycle app', str(message), 'messenger@penncycle.org', ['razzi53@gmail.com'], fail_silently=True)


@login_required
def combo(request):
    if request.method == "POST":
        data = request.POST
        bike = data.get("bike")
        bike = Bike.objects.get(id=bike)
        log = Info(message="Bike {} had combo {} and is now {}".format(bike, bike.combo, data.get("combo")))
        log.save()
        bike.combo = data.get("combo")
        bike.combo_update = datetime.datetime.today()
        bike.save()
        context = {
            'pages': pages,
            'bikes': Bike.objects.all()
        }
    else:
        context = {
            'pages': pages,
            'bikes': Bike.objects.all()
        }
    context_instance = RequestContext(request, context)
    return render_to_response("combo.html", context_instance)
