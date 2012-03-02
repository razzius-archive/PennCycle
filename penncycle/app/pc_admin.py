from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from penncycle.app.models import Manufacturer, Student, Bike, Ride, Quiz
import datetime

class pcRidesAdmin(admin.ModelAdmin):
  list_display = (
      'rider', 'status', 
  )
  list_filter = (
      'bike__status', 'bike', 'checkout_time', 'checkin_time', 
  )
  fieldsets = (
    (None, {'fields':(('rider','bike'),),
            'classes':('main_options',)}),
    ('Edit Check-In Time', {'classes':('collapse','extrapretty'),
                'fields':('checkin_time',)
                }),
    )
  date_hierarchy = 'checkin_time'
  ordering = ('-checkout_time',)
  actions = ['check_in']
  search_fields = ['rider__name','rider__penncard_number','bike__bike_name']
  save_on_top = True
##  change_form_template = 'c:/djcode/penncycle/templates/admin/app/change_form.html'

  # make this only work for bikes not already checked in
  def check_in(self, request, queryset):
    rides_updated = queryset.update(checkin_time=datetime.datetime.now())
    for item in queryset:
      item.bike.status='available'
      item.rider.status = 'available'
      item.rider.save()
      item.bike.save()
    if rides_updated == 1:
      message_bit = '1 bike was'
    else:
      message_bit = '%s bikes were' % rides_updated
    self.message_user(request, '%s successfully checked in' % message_bit)
  check_in.short_description = "Check in the selected rides"

pcAdminSite = AdminSite(name='pcadmin')
pcAdminSite.register(Ride, pcRidesAdmin)
