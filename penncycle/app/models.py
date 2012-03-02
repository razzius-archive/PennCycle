from django.db import models
from django.db.models import Q
import datetime

# Create your models here.
day_end = datetime.time(23, 0, 0)
day_start = datetime.time(9, 0, 0)

GENDER_CHOICES = (
  ('M', 'Male'),
  ('F', 'Female'),
)

GRAD_YEAR_CHOICES = (
  ('2015', '2015'),
  ('2014', '2014'),
  ('2013', '2013'),
  ('2012', '2012'),
  ('2011', '2011'),
  ('faculty', 'faculty'),
  ('staff', 'staff'), 
  ('guest', 'guest'),
  ('grad', 'grad student'),
)

LIVING_LOCATIONS = (
  ('Hill', 'Hill'),
  ('KCECH', 'KCECH'),
  ('Quad', 'Quad'),
  ('Harrison', 'Harrison'),
  ('Harnwell', 'Harnwell'),
  ('Rodin', 'Rodin'),
  ('Stouffer', 'Stouffer'), 
  ('Du Bois', 'Du Bois'),
  ('Gregory', 'Gregory'),
  ('Off Campus', 'Off Campus'),
)

SCHOOL_CHOICES = (
  ('C', 'College'),
  ('W', 'Wharton'),
  ('E', 'SEAS'),
  ('N', 'Nursing'),
  ('ANN','Annenberg'),
  ('DEN','Dental'),
  ('DES','Design'),
  ('GSE','Education'),
  ('LAW','Law'),
  ('MED','Medicine'),
  ('SPP','Social Policy & Practice'),
  ('VET','Veterinary'),
  ('O', 'Other or N/A'),
)

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
  phone = models.CharField(max_length=16)
  penncard_number = models.CharField(verbose_name="Penncard", max_length=8, unique=True)
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  grad_year = models.CharField(max_length=5, choices=GRAD_YEAR_CHOICES)
  join_date = models.DateField(default=datetime.date.today())
  height = models.CharField(max_length=10)
  school = models.CharField(max_length=10, choices=SCHOOL_CHOICES)
  major = models.CharField(max_length=50, blank=True)
  living_location = models.CharField(max_length=100, choices=LIVING_LOCATIONS)
  quiz_completed = models.BooleanField(default=False)
  waiver_signed = models.BooleanField(default=False)
  paid = models.BooleanField(default=False)
  status = models.CharField(max_length=100, default='available')

  def __unicode__(self):
    return u'%s %s' % (self.name, self.penncard_number)

class Bike(models.Model):
  bike_name = models.CharField(max_length=100)
  manufacturer = models.ForeignKey(Manufacturer)
  purchase_date = models.DateField()
  color = models.CharField(max_length=30, blank=True)
  status = models.CharField(max_length=100, default='available')

  def __unicode__(self):
    return self.bike_name

class Ride(models.Model):
  rider = models.ForeignKey(Student, limit_choices_to = {
    'status': 'available',
    'waiver_signed':True,
    'quiz_completed':True,
    'paid':True})
  bike = models.ForeignKey('Bike', limit_choices_to = {'status': 'available'},
    related_name='rides')
  checkout_time = models.DateTimeField(auto_now_add=True)
  checkin_time = models.DateTimeField(null=True, blank=True)

  @property
  def ride_duration_days(self):
    if self.checkin_time == None:
      end = datetime.datetime.now()
    else:
      end = self.checkin_time
    duration = end - self.checkout_time
    duration_days = duration.days 
    return duration_days

  @property
  def status(self):
    if self.checkin_time == None:
      return 'out'
    else:
      return 'in'

  def save(self):
    super(Ride, self).save()
    if self.checkin_time == None:
      self.bike.status = 'out'
      self.rider.status = 'out'
    else:
      self.bike.status = 'available'
      self.rider.status = 'available'
    self.bike.save()
    self.rider.save()
   
  def __unicode__(self):
    return u'%s on %s' % (self.rider, self.checkout_time)

class Quiz(models.Model):
  question = models.CharField(max_length=100)
  answer = models.CharField(max_length=200)
  wrong1 = models.CharField(max_length=200)
  wrong2 = models.CharField(max_length=200)
  wrong3 = models.CharField(max_length=200)
  wrong4 = models.CharField(max_length=200)

  def __unicode__(self):
    return self.question
