# import re
# import datetime
import json

from django.core.mail import send_mail
from app.models import Student, Bike, Ride, Station

import twilio.twiml
from django.views.generic import TemplateView


def email_razzi(message):
    send_mail('an important email from the PennCycle app', str(message), 'messenger@penncycle.org', ['razzi53@gmail.com'], fail_silently=True)


class Signup(TemplateView):
    template_name = "index.html"

hsk kfej
# def info_submit(request):
#     form = SignupForm(request.POST)
#     if form.is_valid():
#         form.save()
#         reply = {
#             'success': True,
#             'form_valid': True
#         }
#     else:
#         reply = {
#             'success': True,
#             'form_valid': False,
#             'new_form': str(form)
#         }
#     return HttpResponse(json.dumps(reply), content_type="application/json")

def send_pin(phone_number):
    student = Student.objects.get(phone=phone_number)
    pin = student.pin
    return "fix mess"