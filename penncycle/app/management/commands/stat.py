import datetime
from django.core.management.base import NoArgsCommand
from app.models import *


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        today = datetime.datetime.today()
        day = today.day
        week_ago_day = 0 if day < 7 else day - 7
        week_ago = datetime.datetime.replace(today, day=week_ago_day)
        students = Student.objects.filter(join_date__gt=week_ago).count()
        print("Recent stats:")
        if week_ago_day == 0:
            print("Signups since the start of the month: {}".format(students))
        else:
            print("Signups since a week ago: {}".format(students))

        start_of_semester = datetime.datetime(2013, 1, 1)
        students = Student.objects.filter(join_date__gt=start_of_semester)
        print("Signups this semester: {}".format(students).count())

        ridden_this_semester = 0
        for s in Student.objects.all():
            if s.ride_set.count() > 0:
                if s.ride_set.all()[0].checkout_time > start_of_semester:
                    ridden_this_semester += 1

        print("Unique riders this semester: {}".format(ridden_this_semester))

        #revenue
        revenue = 0
        for p in Plan.objects.all():
            for i in p.payment_set.all():
                if not i.student.staff:
                    revenue += i.amount

        print("Total revenue up to date: {}".format(revenue))

        participants = len([s for s in Student.objects.all() if s.ride_set.count() > 0])
        print("Totals:")
        print("Total number of students that have ridden is {}".format(participants))

#Total signups per semester
#Total rides
#Most frequent riders
#Total revenue from plans
#Average bike load?
#Signup followthrough rate
