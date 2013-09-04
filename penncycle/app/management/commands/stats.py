from django.core.management.base import NoArgsCommand
from django.utils import timezone

from app.models import *

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        today = timezone.now()
        day = today.day
        week_ago_day = 1 if day < 7 else day - 7
        week_ago = timezone.datetime.replace(today, day=week_ago_day)
        students = Student.objects.filter(join_date__gt=week_ago).count()
        print("Recent stats:")
        if week_ago_day == 0:
            print("Signups since the start of the month: {}".format(students))
        else:
            print("Signups since a week ago: {}".format(students))

        start_of_semester = timezone.datetime(2013, 8, 1, tzinfo=timezone.utc)
        students = Student.objects.filter(join_date__gt=start_of_semester)
        print("Signups this semester: {}".format(students.count()))

        ridden_this_semester = 0
        for s in Student.objects.all():
            if s.ride_set.count() > 0:
                if s.ride_set.all()[0].checkout_time > start_of_semester:
                    ridden_this_semester += 1

        print("Unique riders this semester: {}".format(ridden_this_semester))

        revenue = 0
        for p in Payment.objects.filter(payment_date__gte=start_of_semester):
            revenue += float(p.amount)
        print("Revenue for this semester is {}".format(revenue))

        revenue = 0
        for p in Plan.objects.all():
            for i in p.payment_set.all():
                if not i.student.staff and i.satisfied:
                    if not (p.name == "Spring Basic 2013" and i.student.living_location in ["Fisher", "Ware"]):
                        revenue += i.amount

        print("Total revenue up to date: {}".format(revenue))

        participants = len([s for s in Student.objects.all() if s.ride_set.count() > 0])
        print("Totals:")
        print("Total number of students that have ridden is {}".format(participants))

        signups_since_fall = Student.objects.filter(
            join_date__gte=timezone.datetime(2013, 8, 1, tzinfo=timezone.utc),
            join_date__lte=timezone.datetime(2014, 1, 1, tzinfo=timezone.utc)
        )

        print("Signed up in fall: {}".format(len(signups_since_fall)))
        can_ride_since_fall = [s for s in signups_since_fall if s.can_ride]
        print("Can ride since fall: {}".format(len(can_ride_since_fall)))



#Most frequent riders
#Average bike load?
#Signup followthrough rate
