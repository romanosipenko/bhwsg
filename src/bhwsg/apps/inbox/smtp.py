import smtpd
import datetime
import base64
import logging
from uuid import uuid1
from smtpd import DEBUGSTREAM, EMPTYSTRING, NEWLINE
from asyncore import ExitNow
from core.utils import get_object_or_None

from inbox.models import Inbox

__version__ = 'BHWSGSMTP proxy version 0.1'


class BHWSGSMTPCredintailsValidator(object):
    """
        Check inbox by given credintails
    """
    def __init__(self):
        self.inbox = None
        self.password = None
        self.valid = False

    def _validate(self, username, password):
        # Get inbox, using credintails
        inbox = get_object_or_None(Inbox, slug=username, password=password)
        return True if inbox else False

    def validate(self, username, password):
        self.valid = self._validate(username, password)
        if self.valid:
            self.inbox = username
            self.password = password

        return self.valid


class BHWSGSMTPServer(smtpd.SMTPServer):
    """ SMTP Server instance. Move incoming mails to Celery """

    def __init__(self, localaddr, remoteaddr, credential_validator=BHWSGSMTPCredintailsValidator):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        self.credential_validator = BHWSGSMTPCredintailsValidator()

    def process_message(self, peer, mailfrom, rcpttos, data):
        if self.credential_validator.valid:
            mail_dict = {
                'peer': peer,
                #'from_email': mailfrom,
                #'to_email': rcpttos,
                'raw': data,
                'uuid': str(uuid1()),
                'date': datetime.datetime.now(),
                'inbox': self.credential_validator.inbox
            }
            # Save mail to db in celery task
            from inbox.tasks import handle_mail
            print handle_mail.delay(mail_dict)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            conn, addr = pair
            print >> DEBUGSTREAM, 'Incoming connection from %s' % repr(addr)
            SMTPChannel(self, conn, addr, self.credential_validator)


class SMTPChannel(smtpd.SMTPChannel):
    def __init__(self, server, conn, addr, credential_validator):
        smtpd.SMTPChannel.__init__(self, server, conn, addr)
        
        self.authenticating = False
        self.authenticated = False
        self.username = None
        self.password = None
        self.credential_validator = credential_validator

        self.debug = True
        self.logger = logging.getLogger('smtp')

    # smtp_EHLO and smtp_AUTH , found_terminator are stoled from secure-smtpd. https://github.com/bcoe/secure-smtpd
    def smtp_EHLO(self, arg):
        if not arg:
            self.push('501 Syntax: EHLO hostname')
            return
        if self.__greeting:
            self.push('503 Duplicate HELO/EHLO')
        else:
            self.push('250-%s Hello %s' % (self.__fqdn, arg))
            self.push('250-AUTH LOGIN')
            self.push('250 EHLO')

    def smtp_AUTH(self, arg):
        if 'LOGIN' in arg:
            self.authenticating = True
            split_args = arg.split(' ')

            # Some implmentations of 'LOGIN' seem to provide the username
            # along with the 'LOGIN' stanza, hence both situations are
            # handled.
            if len(split_args) == 2:
                self.username = base64.b64decode(arg.split(' ')[1])
                self.push('334 ' + base64.b64encode('Username'))
            else:
                self.push('334 ' + base64.b64encode('Username'))

        elif not self.username:
            self.username = base64.b64decode(arg)
            self.push('334 ' + base64.b64encode('Password'))
        else:
            self.authenticating = False
            self.password = base64.b64decode(arg)
            if self.credential_validator and self.credential_validator.validate(self.username, self.password):
                self.authenticated = True
                self.push('235 Authentication successful.')
            else:
                self.push('454 Temporary authentication failure.')
                raise ExitNow()

    # support for AUTH is added.
    def found_terminator(self):
        line = EMPTYSTRING.join(self.__line)

        if self.debug:
            self.logger.info('found_terminator(): data: %s' % repr(line))

        self.__line = []
        if self.__state == self.COMMAND:
            if not line:
                self.push('500 Error: bad syntax')
                return
            method = None
            i = line.find(' ')

            if self.authenticating:
                # If we are in an authenticating state, call the
                # method smtp_AUTH.
                arg = line.strip()
                command = 'AUTH'
            elif i < 0:
                command = line.upper()
                arg = None
            else:
                command = line[:i].upper()
                arg = line[i + 1:].strip()

            # White list of operations that are allowed prior to AUTH.
            if not command in ['AUTH', 'EHLO', 'HELO', 'NOOP', 'RSET', 'QUIT']:
                if not self.authenticated:
                    self.push('530 Authentication required')

            method = getattr(self, 'smtp_' + command, None)
            if not method:
                self.push('502 Error: command "%s" not implemented' % command)
                return
            method(arg)
            return
        else:
            if self.__state != self.DATA:
                self.push('451 Internal confusion')
                return
            # Remove extraneous carriage returns and de-transparency according
            # to RFC 821, Section 4.5.2.
            data = []
            for text in line.split('\r\n'):
                if text and text[0] == '.':
                    data.append(text[1:])
                else:
                    data.append(text)
            self.__data = NEWLINE.join(data)
            status = self.__server.process_message(
                self.__peer,
                self.__mailfrom,
                self.__rcpttos,
                self.__data
            )
            self.__rcpttos = []
            self.__mailfrom = None
            self.__state = self.COMMAND
            self.set_terminator('\r\n')
            if not status:
                self.push('250 Ok')
            else:
                self.push(status)
