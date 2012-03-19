from django.contrib.localflavor.us.models import PhoneNumberField
from django.template.defaultfilters import slugify
from django.db import models
from django.db.models import Q
from django.core.validators import RegexValidator
import re
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
  ('grad', 'grad student'),
  ('faculty', 'faculty'),
  ('staff', 'staff'), 
  ('guest', 'guest'),
)

LIVING_LOCATIONS = (
  ('Hill', 'Hill'),
  ('KCECH', 'KCECH'),
  ('Quad', 'Quad'),
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

PAYMENT_CHOICES = (
  ('cash','cash'),
  ('penncash','penncash'),
  ('bursar','bursar '),
  ('credit','credit'),
  ('group','group'),
  ('free','free'),
  ('other','other'),
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
  status = models.CharField(max_length=100, default='available')
  payment_type = models.CharField(max_length=100, choices=PAYMENT_CHOICES, blank=True, null=True)
  at_desk = models.NullBooleanField()

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

  def __unicode__(self):
    return '%s (%s)' % (self.bike_name, self.manufacturer)

class Station(models.Model):
  name = models.CharField(max_length=100)
  latitude = models.FloatField(default=39.9529399)
  longitude = models.FloatField(default=-75.1905607)
  address = models.CharField(max_length=300, blank=True)
  notes = models.TextField(max_length=100, blank=True)
  picture = models.ImageField(upload_to='img/stations', blank=True)
  capacity = models.IntegerField()

  def __unicode__(self):
    return self.name

class Ride(models.Model):
  rider = models.ForeignKey(Student, limit_choices_to = {
    'status': 'available',
    'waiver_signed':True,
    'paid':True})
  bike = models.ForeignKey('Bike', limit_choices_to = {'status': 'available'},
    related_name='rides')
  checkout_time = models.DateTimeField(auto_now_add=True)
  checkin_time = models.DateTimeField(null=True, blank=True)
  checkout_station = models.ForeignKey(Station, default=1, related_name='checkouts')
  checkin_station = models.ForeignKey(Station, blank=True, null=True, related_name='checkins')
  num_users = models.IntegerField()
  
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
    if not self.num_users:
      self.num_users = len(Student.objects.all())
      'set the num users'
    'should pass to normal save func now'
    super(Ride, self).save()
    'super saved!'
    if self.checkin_time == None:
      'bikes should become out now'
      self.bike.status = 'out'
      self.rider.status = 'out'
    else:
      print 'in save else'
      self.checkin_station = 1
      'did checkin station'
      self.bike.status = 'available' #change to be 'at %s' % station
      self.rider.status = 'available'
      'should have changed to available'
    self.bike.save()
    self.rider.save()
   
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
