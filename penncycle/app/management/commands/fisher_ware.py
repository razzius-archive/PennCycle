import datetime
from django.core.management.base import NoArgsCommand
from app.models import *
from pprint import pprint


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        stats = {}
        start = datetime.date(2013, 1, 1)
        rides = Ride.objects.filter(checkin_time__gte=start)
        chris = Student.objects.get(name="Chris Cruz")
        z = [r for r in rides if not r.rider.staff]
        print(len(rides), len(z))
        rides_without_chris = rides.exclude(rider=chris)
        fisher = Station.objects.get(name="Fisher")
        fisher_rides = rides_without_chris.filter(checkout_station=fisher)
        fisher_returns = rides_without_chris.filter(checkin_station=fisher)
        fisher_to_fisher = fisher_rides.filter(checkin_station=fisher)
        stats['Fisher Rides Checked Out'] = fisher_rides.count()
        stats['Fisher Rides Returned'] = fisher_returns.count()
        stats['Fisher-to-Fisher rides'] = fisher_to_fisher.count()
        print("Rides starting in fisher and ending in fisher:")
        pprint(list(fisher_to_fisher))
        ware = Station.objects.get(name="Ware")
        ware_rides = rides_without_chris.filter(checkout_station=ware)
        ware_returns = rides_without_chris.filter(checkin_station=ware)
        ware_to_ware = ware_rides.filter(checkin_station=ware)
        stats['Ware Rides Checked Out'] = ware_rides.count()
        stats['Ware Rides Returned'] = ware_returns.count()
        stats['Ware-to-Ware rides'] = ware_to_ware.count()
        print("Rides starting in ware and ending in ware:")
        pprint(list(ware_to_ware))
        print("Misc stats:")
        pprint(stats)
        fisher_global_checkouts = list(rides_without_chris)
        count = 0
        for r in fisher_global_checkouts:
            if r.rider.living_location == "Fisher":
                count += 1
                print(r)
        print("7 Fisher PC users took {} rides".format(count))
        Ware_global_checkouts = list(rides_without_chris)
        count = 0
        for r in Ware_global_checkouts:
            if r.rider.living_location == "Ware":
                count += 1
                print(r)
        print("? Ware PC users took {} rides".format(count))
