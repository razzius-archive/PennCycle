from django.test import TestCase
from django.utils import timezone

from penncycle.app.models import(
    Bike, Student, Plan, Payment, Station, Manufacturer
)
from penncycle.util.lend import make_ride

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
        station = Station(
            name="Rodin"
        )
        station.save()
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
        busy_bike.save()
        self.student = student
        self.bike = bike

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
        body = "checkout 1"
        expected = "still in use"
        response = handle_checkout(self.student, body)
        print(response)
        self.assertTrue(expected in response)
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
        expected = "1 @ Rodin"
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
