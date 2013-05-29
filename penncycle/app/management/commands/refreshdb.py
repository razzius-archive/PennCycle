from django.core.management.base import NoArgsCommand
from app.models import *
import os


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        os.system("heroku pgbackups:capture --expire")
        os.system("curl -o latest.dump `heroku pgbackups:url`")
        os.system("pg_restore --verbose --clean --no-acl --no-owner -U razzi -d pcpg latest.dump")
        os.system("mv latest.dump /home/razzi/Desktop/pchk/penncycle/data/")
