import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from crispy_forms.utils import render_crispy_form

from app.models import Student
from penncycle.util.util import welcome_email, send_pin_to_student
from .forms import SignupForm


@csrf_exempt
def check_for_student(request):
    penncard = request.POST.get("penncard")
    try:
        student = Student.objects.get(penncard=penncard)
        reply = {"success": True, 'student': student.name}
    except Student.DoesNotExist:
        signup_form = SignupForm(initial={"penncard": penncard})
        reply = {
            "success": False,
            "signup_form": render_crispy_form(signup_form)
        }
    return HttpResponse(json.dumps(reply), content_type="application/json")


@csrf_exempt
def signup(request):
    form = SignupForm(request.POST)
    __import__("pdb").set_trace()
    if form.is_valid():
        student = form.save()
        reply = {
            'success': True,
            'pin': student.pin
        }
        send_pin_to_student(student)
        welcome_email(student)
    else:
        reply = {
            'success': False,
            'signup_form': render_crispy_form(form)
        }
    return HttpResponse(json.dumps(reply), content_type="application/json")

@csrf_exempt
def verify(request):
    data = request.POST
    penncard = data.get("penncard")
    pin = data.get("pin")
    try:
        student = Student.objects.get(penncard=penncard)
        reply = {"exists": True, "valid": student.pin == pin}
    except Student.DoesNotExist:
        reply = {"exists": False}
    return HttpResponse(json.dumps(reply), content_type="application/json")
