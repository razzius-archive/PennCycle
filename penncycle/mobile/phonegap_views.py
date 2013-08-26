import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from crispy_forms.utils import render_crispy_form

from app.models import Student, Bike, Station
from penncycle.util.util import welcome_email, send_pin_to_student
from .forms import SignupForm


@csrf_exempt
def check_for_student(request):
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
            'success': True,
            'pin': student.pin,
            'waiver': render_to_string('waiver.html')
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
        if student.pin == pin:
            reply = {
                "exists": True,
                "valid": True,
                "student_data": {
                    "name": student.name,
                    "can_ride": student.can_ride,
                    "current_ride": student.current_ride.serialize() if student.current_ride else None,
                    "ride_history": [
                        r.serialize() for r in student.ride_history
                    ]
                },

            }
        else:
            reply = {"exists": True, "valid": False}
    except Student.DoesNotExist:
        reply = {"exists": False}
    return HttpResponse(json.dumps(reply), content_type="application/json")


@csrf_exempt
def send_pin(request):
    data = request.POST
    student = Student.objects.get(penncard=data["penncard"])
    send_pin_to_student(student)
    return HttpResponse(json.dumps({"success": True, "phone": student.phone}), content_type="application/json")

def bike_data(request):
    data = [
        {
            "name": bike.name,
            "status": bike.status,
            "location": bike.location.name,
            "latitude": bike.location.latitude,
            "longitude": bike.location.longitude
        } for bike in Bike.objects.all()
    ]
    return HttpResponse(json.dumps(data), content_type="application/json")

def station_data(request):
    data = [
        {
            "name": station.name,
            "latitude": station.latitude,
            "longitude": station.longitude
        } for station in Station.objects.all()
    ]
    return HttpResponse(json.dumps(data), content_type="application/json")
