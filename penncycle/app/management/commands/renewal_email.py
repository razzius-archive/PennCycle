from django.core.management.base import NoArgsCommand
from django.utils import timezone
from app.models import Payment
from util.util import email_razzi, renewal_email

class Command(NoArgsCommand):
	"""To be run nightly"""
	def handle_noargs(self, **options):
		now = timezone.now().date()
		five_days_from_now = now + timezone.timedelta(days=5)
		payments = Payment.objects.filter(end_date=five_days_from_now, renew=False)
		for p in payments:
			renewal_email(p.student, p)
