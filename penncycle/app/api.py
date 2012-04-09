import random, json, hashlib, hmac, gviz_api, operator
from collections import Counter
from django.http import HttpResponseRedirect, HttpResponse
from app.models import *

def get_stats(request):
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
    #('',('','')),
    ] 
  # data = []
  # n = 0
  # for s in students:
    # n+=1
    # if s.join_date in data:
      # data.append([s.join_date, n])
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
