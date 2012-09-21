from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from penncycle.app.models import Manufacturer, Student, Bike, Ride, Station, Payment, Comment
import datetime
from penncycle.app.admin_stuff import PaymentAdmin, RidesAdmin, StudentAdmin, Bike
# from penncycle.app.admin_stuff.RidesAdmin import check_in as admin_check_in

class pcRidesAdmin(RidesAdmin):
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
  # def check_in(self, request, queryset):
  #   return RidesAdmin.check_in(self, request, queryset)
  # check_in = admin_check_in

  def add_view(self, request, extra_context=None):
    extra_context = extra_context or {}
    station = request.user.groups.exclude(name='Associate')[0].name or ''
    print station
    extra_context['station'] = station
    return super(pcRidesAdmin, self).add_view(request,
      extra_context=extra_context)

pcAdminSite = AdminSite(name='pcadmin')
pcAdminSite.register(Ride, pcRidesAdmin)
pcAdminSite.register(Payment, PaymentAdmin)
pcAdminSite.register(Bike, BikeAdmin)
pcAdminSite.register(Student, StudentAdmin)
pcAdminSite.register(Comment)
# pcAdminSite.register(Station)