import random, json, hashlib, hmac, gviz_api, operator, math
from collections import Counter
from django.http import HttpResponseRedirect, HttpResponse
from app.models import *
from django.contrib.auth.decorators import login_required

def signups(request):
  print 'in get_stats'
  students = Student.objects.all()#.order_by(join_date)
  # description = {
    # "signup": ("date", "Signup Date"),
    ##"name": ("string", "Name"),
    # "cum": ("number", "Cumulative"),
		# }
  # data = []
  # n = 0
  # for s in students:
    # n += 1
    # dicti = {"signup":s.join_date, "name":str(s.name), "cum":int(n)}
    # data.append(dicti)
  description = [
    ('date', 'date','Signup Date'), 
    ('signups','number','Signups'),
    ('cum','number','Cumulative'),
    ] 
  data = Counter([s.join_date for s in students]).items()
  data = sorted(data, key=operator.itemgetter(0), reverse=False)
  print data
  n=0
  longdata = []
  for d in data:
    n+=d[1]
    longdata.append(d+(n,))
  print longdata
  # Loading it into gviz_api.DataTable
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(longdata)
  json = data_table.ToJSon(columns_order=("date", "signups", "cum"), order_by="date")

  return HttpResponse(json, content_type="application/json")

def schools(request):
  students = Student.objects.all()
  description = [
    ('school','string','School'),
    ('count','number','Count'),
    ] 
  columns_order = ('school', 'count')
  order_by = columns_order[1]
  data = Counter([s.school for s in students]).items()
  #data = sorted(data, key=operator.itemgetter(0), reverse=True)
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")
  
def majors(request):
  students = Student.objects.all()
  description = [
    ('major','string','Major'),
    ('count','number','Count'),
    ] 
  columns_order = ('major', 'count')
  order_by = columns_order[1]
  data = Counter([s.major for s in students]).items()
  #data = sorted(data, key=operator.itemgetter(0), reverse=True)
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")
  
def numrides(request):
  students = Student.objects.all()
  description = [
    ('numrides','string','Number of Rides'),
    ('frequency','number','Frequency'),
    ] 
  columns_order = ('numrides', 'frequency')
  order_by = columns_order[0]
  def num_rides(student):
    return len(student.ride_set.all())
  data = Counter([num_rides(s) for s in students]).items()
  #data = sorted(data, key=operator.itemgetter(0), reverse=True)
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")
  
def numrides(request):
  students = Student.objects.all()
  description = [
    ('numrides','string','Number of Rides'),
    ('frequency','number','Frequency'),
    ] 
  columns_order = ('numrides', 'frequency')
  order_by = columns_order[0]
  
  def num_rides(student):
    return len(student.ride_set.all())
    
  data = Counter([num_rides(s) for s in students]).items()
  
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")
  
@login_required
def emails(request):
  students = Student.objects.all()
  string = ', '.join([s.email for s in students])
  return HttpResponse(string)

def duration(request):
  print 'in duration function'
  rides = Ride.objects.all()
  print 'got rides'
  description = [
    ('duration','string','Duration of Rides'),
    ('count','number','Count'),
    ] 
  columns_order = ('duration', 'count')
  order_by = columns_order[0]
  # here i basically make my own map because a dict is immutable. better way to do this?
  keyList = [float(t)/2 for t in range(0, 21, 1)]
  keyList.append('more')
  valList = [0 for i in range(0, 22, 1)]
  for r in rides:
    if r.checkin_time != None:
      rideDuration = r.checkin_time - r.checkout_time
      hours = math.floor((float(rideDuration.seconds) / 3600) * 2) / 2
      if hours > 10.0:
        hours = 'more'
      index = keyList.index(hours)
   
      valList[index] = valList[index] + 1
      print valList[index]

  # put all that shit back into a dict
  print 'making data'
  #data = {{float(t)/2: valList[valList.index(float(t)/2)]} for t in range(0, 21, 1)} 
  data = []
  for i in range(len(keyList)):
    tempTuple = (keyList[i], valList[i])
    data.append(tempTuple)

  #data = Counter([num_rides(r) for r in rides]).items()
  
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")