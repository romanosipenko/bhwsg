import email


class MailParser(object):
    def __init__(self, mail):
        self._parser = email.message_from_string(mail)
