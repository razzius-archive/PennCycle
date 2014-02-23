from django.core.management.base import NoArgsCommand
from app.models import *
import os


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        os.system("heroku pgbackups:capture --expire --app growing-day-8347")
        os.system("curl -o latest.dump `heroku pgbackups:url --app growing-day-8347`")
        os.system("pg_restore --clean --no-acl --no-owner -d pcpg latest.dump")
