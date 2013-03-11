import datetime
from django.core.management.base import NoArgsCommand
from app.models import *

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		today = datetime.datetime.today()
		day = today.day
		week_ago_day = 0 if day < 7 else day - 7
		if week_ago_day==0:
			print("Since the start of the month:")
		else:
			print("Since a week ago:")
		week_ago = datetime.datetime.replace(today, day=week_ago_day)
		students = Student.objects.filter(join_date__gt=week_ago).count()
		print(students)