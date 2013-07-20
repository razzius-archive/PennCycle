import datetime
import json

from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from django import forms

from braces.views import LoginRequiredMixin

from crispy_forms.layout import Layout, Fieldset, Submit, Div, Field
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineRadios, FormActions

from models import *

from pdb import set_trace

class SignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div(
                    Field(
                        'penncard',
                        placeholder="8 digits",
                    ),
                    'name',
                    'phone',
                    'email', css_class="span5 offset1"
                ), Div(
                    Field(
                        'last_two',
                        placeholder="Usually 00"
                    ),
                    'grad_year',
                    'living_location',
                    InlineRadios('gender'), css_class="span6"
                ), css_class="row-fluid"
            )
        )
        self.helper.form_action = '/signup/'
        self.helper.add_input(Submit('submit', "Submit"))
        self.helper.form_method = 'post'
        self.fields['last_two'].label = "Last two digits of PennCard"
        self.fields['penncard'].label = "PennCard Number"

    class Meta:
        model = Student
        fields = [
            'penncard',
            'name',
            'phone',
            'email',
            'last_two',
            'grad_year',
            'living_location',
            'gender',
        ]

    gender = forms.TypedChoiceField(
        choices=(("M", "Male"), ("F", "Female")),
    )


def lookup(request):
    penncard = request.GET.get("penncard")
    context = {}
    try:
        student = Student.objects.get(penncard=penncard)
        messages.info(request, "Enter your PIN to add plans.")
        return HttpResponseRedirect('/signin/?penncard={}'.format(penncard))
    except Student.DoesNotExist:
        messages.info(request, "Fill out the form below to sign up!")
        return HttpResponseRedirect("/signup/?penncard={}".format(penncard))

def verify_pin(request):
    data = request.POST
    penncard = request.POST.get('penncard')
    pin = request.POST.get('pin')
    context = {}
    try:
        student = Student.objects.get(penncard=penncard)
    except Student.DoesNotExist:
        messages.info(
            request,
            "No student with Penncard {} found. Sign up or email"
            "messenger@penncycle.org if you have already signed up.".format(penncard)
        )
        return HttpResponseRedirect('/signup?penncard={}'.format(penncard))
    if student.pin != pin:
        messages.error(
            request,
            "Your pin did not match. <a href='/send_pin/?penncard={}'>Click here</a> "
            "to resend it to {}.".format(penncard, student.phone)
        )
        return render_to_response("signin.html", RequestContext(request, context))
    else:
        request.session['penncard'] = penncard
        return HttpResponseRedirect('/welcome/')


def welcome(request):
    penncard = request.session.get('penncard')
    try:
        student = Student.objects.get(penncard=penncard)
    except Student.DoesNotExist:
        email_razzi("Strangely, a student dne on welcome. {}".format(student))
        return HttpResponseRedirect("/signin/")
    context = {
        "student": student
    }
    return render_to_response("welcome.html", RequestContext(request, context))


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        psa = Station.objects.get(name="PSA")
        count = Bike.objects.filter(location=psa).filter(status="available").count()
        context = {
            'psa_count': count
        }
        return context


class Faq(TemplateView):
    template_name = 'faq.html'


class Safety(TemplateView):
    template_name = 'safety.html'


class Team(TemplateView):
    template_name = 'team.html'


# def signin(request):
# fix me
# class SignIn(TemplateView):
#     template_name = 'signin.html'

#     def get_context_data(self, **kwargs):
#         penncard = self.request.GET.get('penncard')
#         print(penncard)
#         return {"penncard": penncard}


class Locations(TemplateView):
    template_name = 'locations.html'

    def get_context_data(self, **kwargs):
        context = {
            'stations': Station.objects.order_by("id")
        }
        return context


class Plans(TemplateView):
    template_name = 'plans.html'

    def get_context_data(self, **kwargs):
        context = super(Plans, self).get_context_data(**kwargs)
        context['plans'] = Plan.objects.filter(
            end_date__gte=datetime.date.today(),
            cost__gt=0
        ).order_by('start_date', 'cost')
        return context


class Signup(CreateView):
    model = Student
    template_name = "signup.html"
    form_class = SignupForm
    success_url = "/welcome"

    def get_initial(self):
        return {
            'penncard': self.request.GET.get('penncard')
        }

    def form_valid(self, form):
        student = form.save()
        messages.info(self.request,
            """Welcome to PennCycle, {}!
            Please review the following safety information.
            Your PIN is {}. You'll need it to log in and to
            access our <a href='http://mobile.penncycle.org'>
            mobile app</a>. You can change it on your
            <a href="/welcome/">dashboard</a>.
            """.format(student.name, student.pin)
        )
        self.request.session['penncard'] = student.penncard
        return HttpResponseRedirect('/safety/')


class Safety(TemplateView):
    template_name = "safety.html"


@require_POST
@csrf_exempt
def verify_payment(request):
    email_razzi(request.POST)
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
    context = {}
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
    context['message'] = message
    return render_to_response('thanks.html', RequestContext(request, context))


@require_POST
def verify_waiver(request):
    pennid = request.POST.get('pennid')
    student = Student.objects.get(penncard=pennid)
    student.waiver_signed = True
    student.save()
    return HttpResponse(json.dumps({'message': 'success'}), content_type="application/json")


def pay(request, payment_type, penncard, plan):
    if request.method == 'POST':
        payment_type = str(request.POST.get('payment_type')).lower()
        print("Pay view")
        try:
            student = Student.objects.get(penncard=penncard)  # verify form is filled out well!
        except:
            context = {
                'message': "No student matching that PennCard was found. Please try again, or sign up.",
                'payment_type': payment_type,
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
            }
        except:
            context = {
                'payment_type': payment_type,
                'penncard': penncard,
                'message': "No student matching that PennCard was found. <a href='/signup'>Sign up</a> here.",
            }
        return render_to_response('pay.html', RequestContext(request, context))


class Stats(LoginRequiredMixin, TemplateView):
    template_name = "stats.html"


def select_payment(request):
    plans = Plan.objects.filter(end_date__gte=datetime.date.today(), cost__gt=0)
    # day_plan = Plan.objects.filter(end_date=datetime.date.today(), name__contains='Day Plan')
    # if len(day_plan) < 1:
    #     day_plan = Plan(
    #         name='Day Plan %s' % str(datetime.date.today()),
    #         cost=5,
    #         start_date=datetime.date.today(),
    #         end_date=datetime.date.today(),
    #         description='A great way to try out PennCycle. Or, use this to check out a bike for a friend or family member! Add more day plans to your account to check out more bikes. Day plans can only be purchased day-of.',
    #     )
    #     day_plan.save()
    context = {
        'plans': plans,
    }
    return render_to_response('selectpayment.html', RequestContext(request, context))


@require_POST
def addpayment(request):
    pennid = request.POST.get('pennid')
    try:
        associated_student = Student.objects.get(penncard=pennid)
    except:
        email_razzi("addpayment failed: {}".format(pennid))
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
            'bikes': Bike.objects.all()
        }
    else:
        context = {
            'bikes': Bike.objects.all()
        }
    context_instance = RequestContext(request, context)
    return render_to_response("combo.html", context_instance)
