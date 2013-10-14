from django.core.management.base import NoArgsCommand
from django.utils import timezone
from app.models import Payment
from util.util import email_razzi, renewed_email, email_management

class Command(NoArgsCommand):
	"""To be run nightly. Renews plans and tells students."""
	def handle_noargs(self, **options):
		today = timezone.now().date()
		one_month_from_now = today + timezone.timedelta(days=30)
		payments = Payment.objects.filter(end_date=today, renew=True)
		for payment in payments:
			old_end_date = payment.end_date
			payment.end_date = one_month_from_now
			payment.save()
			email_management("Charge {student} {cost} by bursar for a renewal".format(student=payment.student, cost=payment.plan.cost), "The plan has been renewed, but they have not been charged as of yet.")
			renewed_email(payment, old_end_date)
			email_razzi("renewed {} and emailed them and management".format(payment))
