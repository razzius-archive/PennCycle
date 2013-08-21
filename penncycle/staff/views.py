from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect

from braces.views import LoginRequiredMixin

from app.models import Bike, Student

from util.util import email_razzi
from util.lend import make_ride, checkin_ride

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "staff/index.html"

    def get_context_data(self):
        context = super(Dashboard, self).get_context_data()
        user = self.request.user
        try:
            station = user.groups.exclude(name='Associate')[0]
            station_name = station.name
        except IndexError:
            station = None
            station_name = "No Station"

        available_bikes = Bike.objects.filter(status="available")
        if user.is_superuser:
            bikes_for_checkout = available_bikes
        else:
            bikes_for_checkout = available_bikes.filter(location=station)

        for bike in bikes_for_checkout:
            ride = bike.rides.latest("checkout_time")
            bike.rider = ride.rider.name
            bike.return_date = ride.checkin_time

        bikes_for_checkin = [b for b in Bike.objects.all() if b.status == 'out']
        for bike in bikes_for_checkin:
            ride = bike.rides.latest("checkout_time")
            bike.rider = ride.rider.name
            bike.rider_id = ride.rider.pk
            bike.return_date = ride.checkin_time

        eligible = [s for s in Student.objects.all() if s.can_ride]
        context['eligible'] = eligible
        context['location'] = station_name
        context['bikes_for_checkout'] = bikes_for_checkout
        context['bikes_for_checkin'] = bikes_for_checkin
        return context


def login_required_ajax(function=None, redirect_field_name=None):
    """
    Make sure the user is authenticated to access a certain ajax view

    Otherwise return a HttpResponse 401 - authentication required
    instead of the 302 redirect of the original Django decorator
    """
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(status=401)
        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


@login_required_ajax
def checkout(request):
    try:
        student = request.POST.get("student")
        student = Student.objects.get(name=student)
        bike = request.POST.get("bike")
        bike = Bike.objects.get(name=bike)
        make_ride(student, bike)
        return HttpResponse("success")
    except Exception as error:
        email_razzi("Admin crashed. Locals: {}. Error: {}".format(locals(), error))
        print("Admin: {}".format(locals()))
        return HttpResponse("failure")


@login_required_ajax
def checkin(request):
    try:
        location = request.user.groups.exclude(name='Associate')[0].name
        student_id = request.POST.get("student_id")
        student = Student.objects.get(id=student_id)
        ride = student.ride_set.latest("checkout_time")
        checkin_ride(ride, location)
        return HttpResponse("success")
    except Exception as error:
        email_razzi("Admin crashed. Locals: {}. Error: {}".format(locals(), error))
        print("Admin: {}".format(locals()))
        return HttpResponse("failure")


def end_session(request):
    logout(request)
    return redirect("/")
