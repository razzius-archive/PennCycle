# import re
# import datetime
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import Student # Bike, Ride  # , Station
from penncycle.util.util import email_razzi
from .forms import SignupForm


@csrf_exempt
def check_for_student(request):
    email_razzi("Got request: {}".format(request))
    penncard = request.POST.get("penncard")
    try:
        student = Student.objects.get(penncard=penncard)
        reply = {'student': student.name}
        return HttpResponse(json.dumps(reply, content_type="application/json"))
    except Student.DoesNotExist:
        reply = {'penncard': penncard}
        return HttpResponse(json.dumps(reply, content_type="application/json"))


@csrf_exempt
def mobile_signup(request):
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

@csrf_exempt
def verify(request):
    data = request.POST
    penncard = data.get("penncard")
    pin = data.get("pin")
    try:
        student = Student.objects.get(penncard=penncard)
    except Student.DoesNotExist:
        return "failure"
    if student.pin != pin:
        return "bad pin"
