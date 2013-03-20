from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from penncycle.app.models import Manufacturer, Student, Bike, Ride, Station, Payment, Comment
import datetime
from penncycle.app.views import email_razzi
from penncycle.app.admin_stuff import PaymentAdmin, RidesAdmin, StudentAdmin, BikeAdmin
from django.http import HttpResponse
# from penncycle.app.admin_stuff.RidesAdmin import check_in as admin_check_in

class pcRidesAdmin(RidesAdmin):
  list_display = (
      'rider', 'bike', 'status', 'checkout_station', 'checkin_station',
  )
  list_filter = (
      'bike__status', 'bike', 'checkout_time', 'checkin_time', 'checkin_station',
  )
  fieldsets = (
    (None, {'fields':(('rider','bike','checkout_station'),),
            'classes':('main_options',)}),)
    # ('Edit Check-In Time and Station', {'classes':('collapse','extrapretty'),
    #             'fields':('checkin_time','checkin_station')
    #             }),
#    )
  date_hierarchy = 'checkin_time'
  ordering = ('-checkout_time',)
  actions = ['check_in']
  search_fields = ['rider__name','rider__penncard','bike__bike_name']
  save_on_top = True
##  change_form_template = 'c:/djcode/penncycle/templates/admin/app/change_form.html'

  # make this only work for bikes not already checked in
  # def check_in(self, request, queryset):
  #   return RidesAdmin.check_in(self, request, queryset)
  # check_in = admin_check_in

  def add_view(self, request, extra_context={}):
    try:
      station = request.user.groups.exclude(name='Associate')[0].name
    except:
      email_razzi("{} tried to sign somebody in it would seem. They were told to check their /admin/auth/user status. They had groups {}".format(request.user.get_full_name(), request.user.groups.all()))
      return HttpResponse("You don't have any groups. Go to app.penncycle.org/admin/auth/user and make sure 'associate' and your station are checked.")
    extra_context['station'] = station
    return super(pcRidesAdmin, self).add_view(request, extra_context=extra_context)

pcAdminSite = AdminSite(name='pcadmin')
pcAdminSite.register(Ride, pcRidesAdmin)
pcAdminSite.register(Payment, PaymentAdmin)
pcAdminSite.register(Bike, BikeAdmin)
pcAdminSite.register(Student, StudentAdmin)
pcAdminSite.register(Comment)
# pcAdminSite.register(Station)