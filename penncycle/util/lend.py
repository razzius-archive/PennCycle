import datetime
import pytz

from app.models import Student, Bike, Ride, Station

def make_ride(student, bike):
    student = Student.objects.get(name=student)
    bike = Bike.objects.get(name=bike)
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

def checkin_ride(ride, location):
    station = Station.objects.get(name=location)
    ride.checkin_time = datetime.datetime.now(pytz.utc)
    ride.checkin_station = station
    ride.bike.status = "available"
    payment = ride.rider.payments.latest()
    payment.status = "available"
    payment.save()
    ride.bike.save()
    ride.save()
