import datetime
import pytz
from django.test import TestCase
from django.utils import timezone
from django.utils.timesince import timesince
from penncycle.app.models import(
    Bike, Student, Plan, Payment, Station, Manufacturer, Ride
)
from penncycle.util.lend import make_ride
from management.commands.warn import test_warn
from views import(
    handle_checkout, handle_checkin, handle_stations, handle_help, handle_bikes
)

class TwilioTest(TestCase):
    def setUp(self):
        student = Student(
            name="Test Student",
            email="test@test.com",
            phone="3195943124",
            penncard="00000000",
            gender="M",
            grad_year="2015",
            living_location="Ware",
            waiver_signed=True,
        )
        student.save()
        other_student = Student(
            name="Other Student",
            email="test@test.com",
            phone="3195943125",
            penncard="00000001",
            gender="M",
            grad_year="2015",
            living_location="Ware",
            waiver_signed=True
        )
        other_student.save()
        student3 = Student(
            name="Test Student3",
            email="test@test.com",
            phone="3195943126",
            penncard="00000002",
            gender="M",
            grad_year="2015",
            living_location="Ware",
            waiver_signed=True,
        )
        student3.save()

        plan = Plan(
            name="Basic Plan",
            cost=0,
        )
        plan.save()

        payment = Payment(
            amount="0",
            plan=plan,
            student=student,
            satisfied=True,
        )
        payment.save()
        other_payment = Payment(
            amount="0",
            plan=plan,
            student=other_student,
            satisfied=True,
        )
        other_payment.save()
        payment3 = Payment(
            amount="0",
            plan=plan,
            student=student,
            satisfied=True,
        )
        payment3.save()
        station = Station(
            name="Rodin"
        )
        station.save()
        

        hill_station = Station(
            name="Hill"
        )
        hill_station.save()

        manufacturer = Manufacturer(
            name="Biria"
        )
        manufacturer.save()
        bike = Bike(
            name="1",
            manufacturer=manufacturer,
            purchase_date=timezone.now(),
            combo_update=timezone.now(),
            location=station
        )
        bike.save()
        busy_bike = Bike(
            name="2",
            manufacturer=manufacturer,
            purchase_date=timezone.now(),
            combo_update=timezone.now(),
            location=station,
            status="out for repairs"
        )

        bike3 = Bike(
            name="3",
            manufacturer=manufacturer,
            purchase_date=timezone.now(),
            combo_update=timezone.now(),
            location=hill_station
        )
        bike3.save()

        bike4 = Bike(
            name="4",
            manufacturer=manufacturer,
            purchase_date=timezone.now(),
            combo_update=timezone.now(),
            location=hill_station
        )
        bike4.save()

        bike5 = Bike(
            name="5",
            manufacturer=manufacturer,
            purchase_date=timezone.now(),
            combo_update=timezone.now(),
            location=hill_station
        )
        bike5.save()

        bike6 = Bike(
            name="6",
            manufacturer=manufacturer,
            purchase_date=timezone.now(),
            combo_update=timezone.now(),
            location=hill_station
        )
        bike6.save()

        bike7 = Bike(
            name="7",
            manufacturer=manufacturer,
            purchase_date=timezone.now(),
            combo_update=timezone.now(),
            location=hill_station
        )
        bike7.save()

        bike8 = Bike(
            name="8",
            manufacturer=manufacturer,
            purchase_date=timezone.now(),
            combo_update=timezone.now(),
            location=hill_station
        )
        bike8.save()

        time_almost_late = timezone.now() + timezone.timedelta(hours=-18, minutes=-30)
        ride_almost_late = Ride(
            rider=student3,
            bike=bike3,
            checkout_station = bike3.location
        #    checkout_time=timezone.now() + timezone.timedelta(hours=-18, minutes=-30)
        )
        
        #ride_almost_late.checkout_time = ride_almost_late.checkout_time + timezone.timedelta(hours=-18, minutes=-30)
        ride_almost_late.save() 
        

        time_almost_late = timezone.now() + timezone.timedelta(hours=-18, minutes=-30)
        ride_almost_late = Ride(
            rider=student3,
            bike=bike3,
            checkout_station = bike3.location
        #    checkout_time=timezone.now() + timezone.timedelta(hours=-18, minutes=-30)
        )
        
        #ride_almost_late.checkout_time = ride_almost_late.checkout_time + timezone.timedelta(hours=-18, minutes=-30)
        ride_almost_late.save() 
    
        busy_bike.save()
        self.student = student
        self.bike = bike
        self.late_ride = ride_almost_late
        self.student3 = student3

    def test_checkout_success(self):
        body = "checkout 1"
        expected = "You have successfully checked out"
        response = handle_checkout(self.student, body)
        print(response)
        self.assertTrue(expected in response)
        self.assertLess(len(response), 161)

    def test_checkout_fail_choice(self):
        body = "checkout garbage"
        expected = "not understood"
        response = handle_checkout(self.student, body)
        print(response)
        self.assertTrue(expected in response)
        self.assertLess(len(response), 161)

    def test_checkout_fail_busy(self):
        other_student = Student.objects.get(name="Other Student")
        make_ride(other_student, self.bike)
        timenow_string = timezone.localtime(datetime.datetime.now(pytz.utc)).strftime("%H:%M on %D")
        body = "checkout 1"
        expected1 = "still in use"
        expected2 = "checked out at "+timenow_string
        response = handle_checkout(self.student, body)
        print "PRINT TIME_NOW: " + timenow_string
        print(response)
        self.assertTrue(expected1 in response)
        self.assertTrue(expected2 in response)
        self.assertLess(len(response), 161)


    def test_checkout_fail_status(self):
        body = "checkout 2"
        expected = "not in service"
        response = handle_checkout(self.student, body)
        print(response)
        self.assertTrue(expected in response)
        self.assertLess(len(response), 161)

    def test_checkin_success(self):
        bike = Bike.objects.get(name="1")
        make_ride(self.student, bike)

        body = "checkin rodin"
        expected = "You have successfully returned"
        response = handle_checkin(self.student, body)
        print(response)
        self.assertTrue(expected in response)
        self.assertLess(len(response), 161)

    def test_checkin_fail_choice(self):
        bike = Bike.objects.get(name="1")
        make_ride(self.student, bike)

        body = "checkin PSA"
        expected = "Station not found"
        response = handle_checkin(self.student, body)
        print(expected, response)
        self.assertTrue(expected in response)
        self.assertLess(len(response), 161)

    def test_bikes(self):
        expected = "At Rodin: 1, 2."
        response = handle_bikes()
        print(response)
        self.assertTrue(expected in response)
        self.assertLess(len(response), 161)

    def test_bikes_many(self):
        expected = "At Hill: 3, 4, 5, 6."
        response = handle_bikes()
        print(response)
        self.assertTrue(expected in response)
        self.assertLess(len(response), 161)

    def test_bikes_few(self):
        expected = "At Rodin: 1, 2."
        response = handle_bikes()
        print(response)
        self.assertTrue(expected in response)
        self.assertLess(len(response), 161)

    def test_stations(self):
        expected = "Rodin"
        response = handle_stations()
        print(response)
        self.assertTrue(expected in response)
        self.assertLess(len(response), 161)

    def test_help(self):
        body = "help"
        expected = "Checkout: Checkout (number)"
        response = handle_help(self.student, body)
        print(response)
        self.assertTrue(expected in response)
        self.assertLess(len(response), 161)

    def test_warn(self):
        rides=Ride.objects.all().filter(rider=self.student3)
        body = test_warn(rides)
        display_time_now = timezone.localtime(datetime.datetime.now(pytz.utc)) 
        display_checkout_time = display_time_now + timezone.timedelta(hours=-18, minutes=-30)
        display_checkin_time = display_checkout_time + timezone.timedelta(hours=24)
        expected1 = "out {}".format(timesince(display_checkout_time))
        expected2 = "At {}:{} there'll be a $5 late fee".format(display_checkin_time.hour, display_checkin_time.minute)
        print(body)
        self.assertTrue(expected1 in body)
        self.assertTrue(expected2 in body)
