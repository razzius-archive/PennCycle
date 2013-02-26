from django.core.management.base import NoArgsCommand
from app.models import *

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		print("Hi.")