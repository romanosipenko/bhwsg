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
            # log.info("<<< v.%s stoped." % __version__)
            sys.exit(0)
        except BaseException:
            # log.critical("<<< v. %s interrupted: %s" % (s, __version__))
            sys.exit(1)