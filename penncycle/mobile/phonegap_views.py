import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from crispy_forms.utils import render_crispy_form

from app.models import Student
from penncycle.util.util import email_razzi, welcome_email, send_pin_to_student
from .forms import SignupForm


@csrf_exempt
def check_for_student(request):
    email_razzi("Got request: {}".format(request))
    penncard = request.POST.get("penncard")
    try:
        student = Student.objects.get(penncard=penncard)
        reply = {"registered": True, 'student': student.name}
    except Student.DoesNotExist:
        signup_form = SignupForm(initial={"penncard": penncard})
        reply = {
            "registered": False,
            "signup_form": render_crispy_form(signup_form)
        }
    return HttpResponse(json.dumps(reply), content_type="application/json")


@csrf_exempt
def signup(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        student = form.save()
        reply = {
            'form_valid': True
        }
        send_pin_to_student(student)
        welcome_email(student)
    else:
        reply = {
            'form_valid': False,
            'new_form': str(form)
        }
    return HttpResponse(json.dumps(reply), content_type="application/json")

@csrf_exempt
def verify(request):
    email_razzi("Got request: {}".format(request))
    data = request.POST
    penncard = data.get("penncard")
    pin = data.get("pin")
    try:
        student = Student.objects.get(penncard=penncard)
        reply = {"exists": True, "valid": student.pin == pin}
    except Student.DoesNotExist:
        reply = {"exists": False}
    return HttpResponse(json.dumps(reply), content_type="application/json")
