from django.core.management.base import BaseCommand
from core.smtp import BHWSGSMTPServer

from django.conf import settings
import asyncore
import sys


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        BHWSGSMTPServer((settings.BHWSG_SMTP_SERVER, settings.BHWSG_SMTP_PORT), None)
        print "Server start @ %s:%s" % (settings.BHWSG_SMTP_SERVER, settings.BHWSG_SMTP_PORT)
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            sys.exit(0)
        except BaseException:
            sys.exit(1)
