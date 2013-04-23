from django.contrib import admin
from penncycle.app.admin_stuff import *


admin.site.register(Comment)
admin.site.register(Station)
admin.site.register(Manufacturer)
admin.site.register(Student, StudentAdmin)
admin.site.register(Bike, BikeAdmin)
admin.site.register(Ride, RidesAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Plan)
admin.site.register(Payment, PaymentAdmin)
