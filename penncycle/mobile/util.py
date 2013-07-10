from app.models import Student

from django_twilio.client import twilio_client

def send_pin_to_phone(phone_number):
    student = Student.objects.get(phone=phone_number)
    pin = student.pin
    twilio_client.sms.messages.create(
        to=student.twilio_phone,
        body="Your PIN for PennCycle is {}. Don't have the mobile app? "\
        "Get it from {{url}}. Log in the website at app.penncycle.org/signin.".format(pin),
        from_="+12156885468"
    )