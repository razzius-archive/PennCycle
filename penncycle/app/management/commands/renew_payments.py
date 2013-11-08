from django.core.management.base import NoArgsCommand
from django.utils import timezone
from app.models import Payment
from util.util import email_razzi, renewed_email, email_managers

class Command(NoArgsCommand):
	"""To be run nightly. Renews plans and tells students."""
	def handle_noargs(self, **options):
		today = timezone.now().date()
		one_month_from_now = today + timezone.timedelta(days=30)
		payments = Payment.objects.filter(end_date=today, renew=True)
		message = "The following have had their plans renewed, but have not been charged: \n"
		for payment in payments:
			old_end_date = payment.end_date
			payment.end_date = one_month_from_now
			payment.save()
			renewed_email(payment, old_end_date)
			message += "{student} with last two {last_two}: {plan}\n".format(
				student=payment.student, last_two=payment.student.last_two,
				plan=payment.plan
			)
		if payments:
			 email_managers(
				"{} renewals: {} total".format(today, len(payments)),
				message
			)

