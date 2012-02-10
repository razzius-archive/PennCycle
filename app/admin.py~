from django.contrib import admin
from penncycle.app.models import Manufacturer, Student, Bike, Ride, Quiz
import datetime

def check_in(modeladmin, request, queryset):
  queryset.update(checkin_time=datetime.datetime.now())
  for item in queryset:
    item.bike.status='available'
    item.bike.save()

check_in.short_description = "Check in the selected rides"

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
        #'rider', 'list_of_bikes', 'checkout_time', 'checkin_time',
        #'ride_duration_days',
    )
    list_filter = (
        'rider', 'bike', 'checkout_time', 'checkin_time', 
    ) 
    readonly_fields = ('ride_duration_days',)
    date_hierarchy = 'checkin_time'
    ordering = ('checkin_time',)
    actions = [check_in]

#class QuizAdmin(admin.ModelAdmin):
#  list_display = (
#      'question', 'answer',
#  )


admin.site.register(Manufacturer)
admin.site.register(Student, StudentAdmin)
admin.site.register(Bike, BikeAdmin)
admin.site.register(Ride, RidesAdmin)
admin.site.register(Quiz)
