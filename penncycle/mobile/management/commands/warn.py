from django.core.management.base import NoArgsCommand
from penncycle.app.models import Ride

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        active_rides = Ride.objects.filter(checkin_time=None)
        print(active_rides)

