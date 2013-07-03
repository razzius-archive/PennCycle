import datetime
import pytz

from django.core.mail import send_mail
from django_localflavor_us.models import PhoneNumberField
from django.db import models
from django.core.validators import RegexValidator

from south.modelsinspector import add_introspection_rules

import hour_util

# Necessary because South hasn't been updated since localflavors was broken up.
add_introspection_rules([], ['django_localflavor_us\.models\.PhoneNumberField'])

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

GRAD_YEAR_CHOICES = (
    ("2017", "2017"),
    ('2016', '2016'),
    ('2015', '2015'),
    ('2014', '2014'),
    ('grad', 'grad student'),
    ('faculty', 'faculty'),
    ('staff', 'staff'),
    ('guest', 'guest'),
)

LIVING_LOCATIONS = (
    ('Hill', 'Hill'),
    ('KCECH', 'KCECH'),
    ('Riepe', 'Riepe'),
    ('Fisher', 'Fisher'),
    ('Ware', 'Ware'),
    ('Harrison', 'Harrison'),
    ('Harnwell', 'Harnwell'),
    ('Rodin', 'Rodin'),
    ('Stouffer', 'Stouffer'),
    ('Mayer', 'Mayer'),
    ('Du Bois', 'Du Bois'),
    ('Gregory', 'Gregory'),
    ('Sansom', 'Sansom'),
    ('Off Campus', 'Off Campus'),
)

SCHOOL_CHOICES = (
    ('C', 'College'),
    ('W', 'Wharton'),
    ('E', 'SEAS'),
    ('N', 'Nursing'),
    ('ANN', 'Annenberg'),
    ('DEN', 'Dental'),
    ('DES', 'Design'),
    ('GSE', 'Education'),
    ('LAW', 'Law'),
    ('MED', 'Medicine'),
    ('SPP', 'Social Policy & Practice'),
    ('VET', 'Veterinary'),
    ('O', 'Other or N/A'),
)

PAYMENT_CHOICES = (
    ('cash', 'cash'),
    ('penncash', 'penncash'),
    ('bursar', 'bursar'),
    ('credit', 'credit'),
    ('group', 'group'),
    ('stouffer', 'stouffer'),
    ('free', 'free'),
    ('other', 'other'),
    ('fisher', 'fisher')
)


class Plan(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(max_length=150, default="Details coming soon!")
    banner = models.CharField(max_length=50, default="")

    def __unicode__(self):
        return self.name + ': $' + str(self.cost)


class Payment(models.Model):
    class Meta:
        get_latest_by = 'date'

    amount = models.DecimalField(decimal_places=2, max_digits=6)
    plan = models.ForeignKey(
        Plan, limit_choices_to={
            'end_date__gte': datetime.date.today(),
        }
    )
    student = models.ForeignKey('Student', related_name="payments")
    date = models.DateField(auto_now_add=True)
    satisfied = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_CHOICES, null=True)
    status = models.CharField(max_length=100, default='available')

    def __unicode__(self):
        return str(self.student) + ' for ' + str(self.plan)


class Manufacturer(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=60, blank=True)
    country = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)

    def __unicode__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField()
    penncard = models.CharField(max_length=8, validators=[RegexValidator('\d{8}')], unique=True)
    last_two = models.CharField(max_length=2, validators=[RegexValidator('\d{2}')], blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    grad_year = models.CharField(max_length=50, choices=GRAD_YEAR_CHOICES)
    join_date = models.DateField(default=datetime.date.today())
    school = models.CharField(max_length=100, choices=SCHOOL_CHOICES)
    major = models.CharField(max_length=50, blank=True)
    living_location = models.CharField(max_length=100, choices=LIVING_LOCATIONS)
    waiver_signed = models.BooleanField(default=False)
    staff = models.NullBooleanField(default=False)
    plan = models.ManyToManyField('Plan', blank=True, null=True)

    @property
    def paid_now(self):
        return len(self.current_payments) > 0

    @property
    def current_payments(self):
        today = datetime.date.today()
        return self.payments.filter(
            satisfied=True,
            plan__start_date__lte=today,
            plan__end_date__gte=today,
        )

    @property
    def can_ride(self):
        return len(self.current_payments.filter(status='available')) > 0 and self.waiver_signed

    def __unicode__(self):
        return u'%s %s' % (self.name, self.penncard)


class Station(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(default=39.9529399)
    longitude = models.FloatField(default=-75.1905607)
    address = models.CharField(max_length=300, blank=True)
    notes = models.TextField(max_length=100, blank=True)
    hours = models.TextField(max_length=100, blank=True)
    picture = models.ImageField(upload_to='img/stations', blank=True)
    capacity = models.IntegerField(default=15)
    full_name = models.CharField(max_length=100, default="")

    def __unicode__(self):
        return self.name

    @property
    def is_open(self):
        return hour_util.is_open(self.hours)

    @property
    def comma_name(self):
        return ", ".join(self.hours.split("\n"))


class Bike(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manufacturer = models.ForeignKey(Manufacturer)
    purchase_date = models.DateField()
    color = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=100, default='available')
    serial_number = models.CharField(max_length=100, blank=True)
    tag_id = models.CharField(max_length=100, blank=True)
    key_serial_number = models.CharField(max_length=100, blank=True)
    combo = models.CharField(max_length=4, blank=True)
    combo_update = models.DateField()
    location = models.ForeignKey(Station, default=2)

    @property
    def knows_combo(self):
        rides = self.rides.filter(checkout_time__gt=self.combo_update)
        return list(set([ride.rider for ride in rides]))

    @property
    def set_location(self):
        last_ride = self.rides.filter(checkin_station__isnull=False).order_by('-checkin_time')
        try:
            last_ride = last_ride[0]
            location = last_ride.checkin_station
        except:
            location = Station.objects.get(name__contains="PSA")
        self.location = location
        self.save()

    def __unicode__(self):
        return '#%s. Location: %s' % (self.name, self.location.name)


class Ride(models.Model):
    rider = models.ForeignKey(
        Student, limit_choices_to={
            'payments__status': 'available',
            'waiver_signed': True,
            'payments__satisfied': True,
            'payments__plan__end_date__gte': datetime.date.today(),
            'payments__plan__start_date__lte': datetime.date.today(),
        },
    )
    bike = models.ForeignKey('Bike', limit_choices_to={'status': 'available'}, related_name='rides')
    checkout_time = models.DateTimeField(auto_now_add=True)
    checkin_time = models.DateTimeField(null=True)
    checkout_station = models.ForeignKey(Station, default=2, related_name='checkouts')
    checkin_station = models.ForeignKey(Station, null=True, related_name='checkins')

    @property
    def ride_duration_days(self):
        if self.checkin_time is None:
            end = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        else:
            end = self.checkin_time
        duration = end - self.checkout_time
        return duration.days

    @property
    def status(self):
        if self.checkin_time is None:
            return 'out'
        else:
            return 'in'

    def save(self):
        print 'in Ride save method'
        super(Ride, self).save()
        if self.checkin_time is None:
            self.bike.status = 'out'
            payment = self.rider.payments.latest()
            payment.status = 'out'
        else:
            self.bike.status = 'available'
            payment = self.rider.payments.latest()
            payment.status = 'available'
        self.bike.save()
        payment.save()

    def __unicode__(self):
        return u'%s on %s' % (self.rider, self.checkout_time)


class Comment(models.Model):
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, blank=True, null=True)
    ride = models.ForeignKey(Ride, blank=True, null=True)
    is_problem = models.BooleanField(default=False)

    def save(self):
        super(Comment, self).save()
        message = '''
            Comment: \n %s \n \n
            Time: \n %s \n \n
            Student: \n %s \n \n
            Ride: \n %s \n \n
            Marked as problem? \n %s \n \n
        ''' % (self.comment, self.time, self.student, self.ride, self.is_problem)
        send_mail('PennCycle: Comment Submitted', message, 'messenger@penncycle.org', ['messenger@penncycle.org'])

    def __unicode__(self):
        return self.comment[:30]


class Info(models.Model):
    message = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.message + " on " + self.date.isoformat()
