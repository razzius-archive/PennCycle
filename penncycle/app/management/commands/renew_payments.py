from django.core.management.base import NoArgsCommand
from django.utils import timezone
from app.models import Payment
from util.util import email_razzi, renewal_email

class Command(NoArgsCommand):
	"""To be run nightly"""
	def handle_noargs(self, **options):
		today = timezone.now().date()
		one_month_from_now = today + timezone.timedelta(days=30)
		payments = Payment.objects.filter(end_date=today, renew=True)
		for p in payments:
			payment.end_date = one_month_from_now
			payment.save
			email_management(
