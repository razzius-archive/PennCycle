from django_twilio.client import twilio_client


def send_pin_to_student(student):
    pin = student.pin
    twilio_client.sms.messages.create(
        to=student.twilio_phone,
        body="Your PIN for PennCycle is {}."
        " Log in the website at penncycle.org/signin.".format(pin),
        from_="+12156885468"
    )
