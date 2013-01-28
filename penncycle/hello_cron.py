import os
from os.path import abspath, dirname
import sys
path = '~/penncycle'
if path not in sys.path:
    sys.path.append(path)
sys.path.insert(0, path)
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from app.models import *
from app.views import email_razzi
from django.core.mail import send_mail

late_rides = Ride.objects.filter(checkin_time=None)

print 'checking for overnight rides'
for ride in late_rides:
  print ride
  stud = ride.rider
  internal_message = ''' 
  We've got an overnight ride on our hands, ladies and gentlemen!
  Ride: %s
  Checkout Time: %s
  Checkout Station: %s
  Bike: %s

  Student Name: %s
  Student Phone: %s
  Student Email: %s
  Student Penncard: %s
  ''' % (ride, ride.checkout_time, ride.checkout_station, ride.bike, stud.name, stud.phone, stud.email, stud.penncard)

  send_mail('Overnight Ride', 
    str(internal_message), 
    'messenger@penncycle.org', 
    ['messenger@penncycle.org'], 
    fail_silently=True)
  try:
    outbound_message = '''
    Hey %s, 
    
    I'm a robot working for PennCycle. Looks like you didn't check in your bike today. That's not a problem: feel free to keep it out as long as you like! 
    We do charge a $5 overnight fee every evening, which you can pay by cash, credit, check, or bursar. 
    You won't be able to check out bikes while you have fees outstanding: reply to this email to arrange payment, or with any questions.

    Thanks, 

    P-98-C22
    Robot, PennCycle
    ''' % stud.name
    print 'not sending outbound message'
    print outbound_message
    # send_mail('PennCycle Overnight ride notice',
    #   str(outbound_message),
    #   'messenger@penncycle.org',
    #   [stud.email],
    #   fail_silently=False)
  except:
    print 'tried to email about an overnight ride but couldn\'t' 
    print stud
    email_razzi('tried to email %s about an overnight ride but couldn\'t' % stud)
  print 'sent email'