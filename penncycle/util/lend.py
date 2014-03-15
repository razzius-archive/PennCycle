import datetime
import pytz
from penncycle.util.util import email_razzi

from app.models import Ride

def make_ride(student, bike):
    ride = Ride(rider=student, bike=bike, checkout_station=bike.location)
    payment = student.payments.filter(status="available")[0]
    payment.status = "out"
    if not payment.end_date:
        if payment.plan.name == "Day Plan":
            delta = datetime.timedelta(days=1)
        else:
            delta = datetime.timedelta(days=30)
        payment.end_date = datetime.datetime.now(pytz.utc) + delta
    bike.status = "out"
    payment.save()
    bike.save()
    ride.save()
    return ride
def checkin_ride(ride, station):
    ride.checkin_time = datetime.datetime.now(pytz.utc)
    ride.checkin_station = station
    ride.bike.status = "available"
    ride.bike.location = station
    try:
        payment = ride.rider.payments.filter(status="out").latest()
    except Exception:
        payment = ride.rider.payments.latest()
        email_razzi("Rider didn't have any payments out")
    payment.status = "available"
    payment.save()
    ride.bike.save()
    ride.save()
