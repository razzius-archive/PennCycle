from django.core.management.base import NoArgsCommand
from django.utils import timezone
from django.utils.timesince import timesince
from django_twilio.client import twilio_client
from penncycle.app.models import Ride
from penncycle.util.util import email_razzi

def warn(ride):
    phone = ride.rider.twilio_phone
    bike = ride.bike.name
    time = timesince(ride.checkout_time)
    latest = ride.checkout_time + timezone.timedelta(hours=24)
    latest_format = "{}:{}".format(latest.hour, latest.minute)
    twilio_client.sms.messages.create(
        to=phone,
        body="You've had bike {} out {}. "
        "At {} there'll be a $5 late fee. "
        "Return the bike or consider an "
        "unlimited plan to remove the 24 hour limit."
        .format(bike, time, latest_format),
        from_="+12156885468"
    )

class Command(NoArgsCommand):
    """To be run every 2 hours."""
    def handle_noargs(self, **options):
        nineteen_hours_ago = timezone.now() + timezone.timedelta(hours=-19)
        eighteen_hours_ago = timezone.now() + timezone.timedelta(hours=-18)
        active_rides = Ride.objects.filter(
            checkin_time=None,
            checkout_time__gte=nineteen_hours_ago,
            checkout_time__lte=eighteen_hours_ago
        )
        for ride in active_rides:
            if "unlimited" not in ride.rider.payments.get(status="out").plan.name:
                warn(ride)
                email_razzi("Warned! {}".format(locals()))

