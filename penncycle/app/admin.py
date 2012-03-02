from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from penncycle.app.models import Manufacturer, Student, Bike, Ride, Quiz
import datetime

class StudentAdmin(admin.ModelAdmin):
  list_display = (
      'name', 'grad_year', 'penncard_number',
      'gender', 'school',)
  search_fields = ('name', 'penncard_number',)
  list_filter = ('school', 'gender', 'grad_year')
  date_hierarchy = 'join_date'
    
class BikeAdmin(admin.ModelAdmin):
  list_display = ('bike_name', 'status', 'manufacturer', 'purchase_date')
  list_filter = ('purchase_date','manufacturer',)
  date_hierarchy = 'purchase_date'

class RidesAdmin(admin.ModelAdmin):
  list_display = (
      'rider', 'bike', 'checkout_time', 'checkin_time', 'ride_duration_days',
  )
  list_filter = (
      'rider', 'bike', 'checkout_time', 'checkin_time', 
  ) 
  readonly_fields = ('ride_duration_days',)
  date_hierarchy = 'checkin_time'
  ordering = ('checkin_time',)
  actions = ['check_in']

  # make this only work for bikes not already checked in
  def check_in(self, request, queryset):
    rides_updated = queryset.update(checkin_time=datetime.datetime.now())
    for item in queryset:
      item.bike.status='available'
      item.bike.save()
    if rides_updated == 1:
      message_bit = '1 bike was'
    else:
      message_bit = '%s bikes were' % rides_updated
    self.message_user(request, '%s successfully checked in' % message_bit)
  check_in.short_description = "Check in the selected rides"

class QuizAdmin(admin.ModelAdmin):
  list_display = (
      'question', 'answer', 'wrong1', 'wrong2', 'wrong3', 'wrong4',
  )

admin.site.register(Manufacturer)
admin.site.register(Student, StudentAdmin)
admin.site.register(Bike, BikeAdmin)
admin.site.register(Ride, RidesAdmin)
admin.site.register(Quiz, QuizAdmin)
