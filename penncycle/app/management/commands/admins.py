from django.core.management.base import NoArgsCommand
from app.models import *
from django.contrib.auth import admin

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		print("These people are in PSA / Houston:")
		admins = admin.User.objects.all()
		for a in admins:
			try:
				location = a.groups.all()[1]
				if location.name == "PSA / Houston":
					print(a)
			except:
				pass
