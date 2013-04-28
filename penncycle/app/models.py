from django.core.mail import send_mail
from django.contrib.localflavor.us.models import PhoneNumberField
from django.template.defaultfilters import slugify
from django.db import models
from django.core.validators import RegexValidator
import datetime

day_end = datetime.time(23, 0, 0)
day_start = datetime.time(9, 0, 0)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

GRAD_YEAR_CHOICES = (
    ('2016', '2016'),
    ('2015', '2015'),
    ('2014', '2014'),
    ('2013', '2013'),
    ('2012', '2012'),
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
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    plan = models.ForeignKey(
        Plan, default=1, limit_choices_to={
            'end_date__gte': datetime.date.today(),
        }
    )
    student = models.ForeignKey('Student', related_name="payments")
    date = models.DateField(auto_now_add=True)
    satisfied = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=100, default='available')

    def save(self):
        super(Payment, self).save()
        self.student.paid = self.student.paid_now

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
    paid = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_CHOICES, blank=True, null=True)
    staff = models.BooleanField(default=False)
    plan = models.ManyToManyField('Plan', blank=True, null=True)

    @property
    def paid_now(self):
        payments = self.current_payments
        if len(payments) > 0:
            return True
        else:
            return False

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
        if len(self.current_payments.filter(status='available')) > 0 and self.waiver_signed:
            return True
        else:
            return False

    def __unicode__(self):
        return u'%s %s' % (self.name, self.penncard)


class Bike(models.Model):
    bike_name = models.CharField(max_length=100, unique=True)
    manufacturer = models.ForeignKey(Manufacturer)
    purchase_date = models.DateField()
    color = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=100, default='available')
    serial_number = models.CharField(max_length=100, blank=True)
    tag_id = models.CharField(max_length=100, blank=True)
    key_serial_number = models.CharField(max_length=100, blank=True)
    combo = models.CharField(max_length=4, blank=True)
    combo_update = models.DateField()

    @property
    def knowsCombo(self):
        rides = self.rides.filter(checkout_time__gt=self.combo_update)
        return list(set([ride.rider for ride in rides]))

    @property
    def location(self):
        last_ride = self.rides.filter(checkin_station__isnull=False).order_by('-checkin_time')
        try:
            last_ride = last_ride[0]
            location = last_ride.checkin_station
        except:
            location = Station.objects.get(name__contains="PSA")
        return location

    def __unicode__(self):
        return '#%s. Location: %s' % (self.bike_name, self.location.name)

days = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

strings = dict([v, k] for k, v in days.items())


def decimal(time):
    if len(time) <= 2:
        return int(time)
    else:
        hours, minutes = time.split(":")
        return int(hours) + float(minutes) / 60


def hour(time):
    return decimal(time[0]) if (time[1] == "am" or time[0] == "12") else decimal(time[0])+12


def enter_hours(interval, info, day):
    # print(info)
    start_time = hour(info[0:2])
    end_time = hour(info[3:5])
    if day in interval:
        interval[day].append((start_time, end_time))
    else:
        interval[day] = [(start_time, end_time)]


def get_hours(description):
    intervals = {}
    day = 0
    if not description:  # empty station
        return {}
    for line in description.split("\n"):  # assumes to be in order
        if line.split()[1] == "-":  # there is a range of days
            # print("range of days")
            start = days[line.split()[0]]
            end = days[line.split()[2][:-1]]
            for i in range(end-start+1):
                that_day = strings[day]
                if "and" in line:  # multiple ranges
                    enter_hours(intervals, line.split()[3:8], that_day)
                    enter_hours(intervals, line.split()[9:14], that_day)
                else:
                    enter_hours(intervals, line.split()[3:8], that_day)
                day += 1
        elif line.split()[0][-1] == ":":
            # print("matched :")
            that_day = strings[day]
            if "and" in line:  # multiple ranges
                enter_hours(intervals, line.split()[1:6], that_day)
                enter_hours(intervals, line.split()[7:12], that_day)
            else:
                enter_hours(intervals, line.split()[1:6], that_day)
                day += 1
        else:  # 7 days a week.
            for day in range(7):
                enter_hours(intervals, line.split()[2:7], strings[day])
    return intervals


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
        ranges = get_hours(self.hours)
        today = datetime.datetime.today().weekday()
        this_hour = datetime.datetime.today().hour
        if strings[today] in ranges:
            hours = ranges[strings[today]]
            for opening in hours:
                if this_hour > opening[0] and this_hour < opening[1]:
                    return True
        return False

    @property
    def comma_name(self):
        return ", ".join(self.hours.split("\n"))


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
    checkin_time = models.DateTimeField(null=True, blank=True)
    checkout_station = models.ForeignKey(Station, default=1, related_name='checkouts')
    checkin_station = models.ForeignKey(Station, blank=True, null=True, related_name='checkins')
    num_users = models.IntegerField()

    @property
    def ride_duration_days(self):
        if self.checkin_time is None:
            end = datetime.datetime.now()
        else:
            end = self.checkin_time
        duration = end - self.checkout_time
        duration_days = duration.days
        return duration_days

    @property
    def status(self):
        if self.checkin_time is None:
            return 'out'
        else:
            return 'in'

    def save(self):
        print 'in Ride save method'
        if not self.num_users:
            self.num_users = len(Student.objects.all())
        super(Ride, self).save()
        print 'super saved!'
        if self.checkin_time is None:
            self.bike.status = 'out'
            payment = self.rider.current_payments.filter(status='available')[0]
            payment.status = 'out'
        else:
            self.bike.status = 'available'
            payment = self.rider.current_payments.filter(status='out')[0]
            payment.status = 'available'
        self.bike.save()
        payment.save()

    def __unicode__(self):
        return u'%s on %s' % (self.rider, self.checkout_time)


class Page(models.Model):
    content = models.TextField()
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def save(self):
        self.slug = slugify(self.name)
        super(Page, self).save()

    def __unicode__(self):
        return self.name


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
