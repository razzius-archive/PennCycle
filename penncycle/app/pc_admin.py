from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from penncycle.app.models import Manufacturer, Student, Bike, Ride, Station
import datetime

class pcRidesAdmin(admin.ModelAdmin):
  list_display = (
      'rider', 'status', 'checkout_station', 'checkin_station',
  )
  list_filter = (
      'bike__status', 'bike', 'checkout_time', 'checkin_time', 'checkin_station',
  )
  fieldsets = (
    (None, {'fields':(('rider','bike','checkout_station'),),
            'classes':('main_options',)}),
    ('Edit Check-In Time and Station', {'classes':('collapse','extrapretty'),
                'fields':('checkin_time','checkin_station')
                }),
    )
  date_hierarchy = 'checkin_time'
  ordering = ('-checkout_time',)
  actions = ['check_in']
  search_fields = ['rider__name','rider__penncard','bike__bike_name']
  save_on_top = True
  print 'hello!'
##  change_form_template = 'c:/djcode/penncycle/templates/admin/app/change_form.html'

  # make this only work for bikes not already checked in
  def check_in(self, request, queryset):
    station_name = request.user.groups.exclude(name='Associate')[0].name or ''
    station = Station.objects.get(name=station_name)
    print station
    rides_updated = queryset.update(
      checkin_time=datetime.datetime.now(), 
      checkin_station=station)

    for item in queryset:
      item.bike.status='available'
      item.rider.status = 'available'
      item.rider.save()
      item.bike.save()
    if rides_updated == 1:
      message_bit = '1 bike was'
    else:
      message_bit = '%s bikes were' % rides_updated
    self.message_user(request, '%s successfully checked in to %s (if this not correct, please modify it!' % (message_bit, station_name))
  check_in.short_description = "Check in the selected rides"

  def add_view(self, request, extra_context=None):
    extra_context = extra_context or {}
    station = request.user.groups.exclude(name='Associate')[0].name or ''
    print station
    extra_context['station'] = station
    return super(pcRidesAdmin, self).add_view(request,
      extra_context=extra_context)

pcAdminSite = AdminSite(name='pcadmin')
pcAdminSite.register(Ride, pcRidesAdmin)
