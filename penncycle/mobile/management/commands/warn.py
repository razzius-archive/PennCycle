from django.core.management.base import NoArgsCommand
from django.utils import timezone
from django.utils.timesince import timesince
from django_twilio.client import twilio_client
from penncycle.app.models import Ride
from penncycle.util.util import email_razzi

def warn_message(ride):
    bike = ride.bike.name
    checkout_display_time = timezone.localtime(ride.checkout_time)
    time = timesince(checkout_display_time)
    latest = checkout_display_time + timezone.timedelta(hours=24)
    latest_format = "{}:{}".format(latest.hour, latest.minute)
    message="You've had bike {} out {}. At {} there'll be a $5 late fee. Return the bike or consider an unlimited plan to remove the 24 hour limit.".format(bike, time, latest_format)
    return message

def warn(ride):
    phone = ride.rider.twilio_phone
    twilio_client.sms.messages.create(
        to=phone,
        body= warn_message(ride),
        from_="+12156885468"
    )
#only used for  testing in mobile/test.py
def test_warn(ride):
        nineteen_hours_ago = timezone.localtime(timezone.now()) + timezone.timedelta(hours=-19)
        eighteen_hours_ago = timezone.localtime(timezone.now()) + timezone.timedelta(hours=-18)
       
        active_rides = Ride.objects.filter(
            checkin_time=None,
            checkout_time__gte=nineteen_hours_ago,
            checkout_time__lte=eighteen_hours_ago
        )

        ride = active_rides[0] 
        if "Unlimited" not in ride.rider.payments.get(status="out").plan.name:
            return warn_message(ride)
        else: 
            return ""

class Command(NoArgsCommand):
    """To be run every 2 hours."""
    def handle_noargs(self, **options):
        nineteen_hours_ago = timezone.localtime(timezone.now()) + timezone.timedelta(hours=-19)
        eighteen_hours_ago = timezone.localtime(timezone.now()) + timezone.timedelta(hours=-18)
        active_rides = Ride.objects.filter(
            checkin_time=None,
            checkout_time__gte=nineteen_hours_ago,
            checkout_time__lte=eighteen_hours_ago
        )
        for ride in active_rides:
            if "Unlimited" not in ride.rider.payments.get(status="out").plan.name:
                warn(ride)
