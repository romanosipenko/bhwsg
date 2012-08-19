import email
from core.utils import memoize_method

TEXT_PLAIN_CONTENT_TYPE = "text/plain"
TEXT_HTML_CONTENT_TYPE = "text/html"

class MailParser(object):
    contenttype_scoredict = {TEXT_PLAIN_CONTENT_TYPE: 1.0, TEXT_HTML_CONTENT_TYPE: 0.5}
    
    def __init__(self, mail):
        self._mail = email.message_from_string(mail.encode('utf-8'))
    
    def get_content_types(self):
        return list(set(item.get_content_type() for item in self._mail.walk()))
    
    def get_attachments(self):
        for item in self._mail.walk():
            name = item.get_filename()
            if name:
                yield (name, item.get_payload(decode=True))         
    
    def get_subject(self):
        return self._mail['Subject']
    
    def get_content_type(self):
        return self._mail['Content-Type']
    
    def get_from(self):
        return self._mail['From']
    
    def get_to(self):
        return self._mail['To'].strip().split(',')
    
    def get_bcc(self):
        return self._mail['BCC'] or self._mail['Bcc'] 
    
    def get_cc(self):
        return self._mail['CC'] or self._mail['Cc']
    
    def get_text(self):
        text_msgs = self._get_text_parts() or None
        
        if text_msgs:
            best_msg = max(text_msgs, key=lambda x:x[0])[1]
            msg_text = best_msg.get_payload(decode=True)
        
        return msg_text
    
    def get_html(self):
        html_msg = filter(lambda x: x[2] == TEXT_HTML_CONTENT_TYPE, self._get_text_parts())
        html_msg = html_msg[0][1] if html_msg else None
        if html_msg:
            html_msg = html_msg.get_payload(decode=True)
        return html_msg
    
    def _get_texts_and_scores_from_message(self, msg):
        scorelist = []
        for item in self._mail.walk():
            if not item.is_multipart():
                contenttype = item.get_content_type().lower()
                if contenttype.startswith("text"):
                    contenttype_score = self.contenttype_scoredict.get(contenttype, 0.0)
                    scorelist.append((contenttype_score, item, contenttype))
                     
        return scorelist
    
    @memoize_method
    def _get_text_parts(self):
        text_parts = self._get_texts_and_scores_from_message(self._mail)
        return text_parts
        
    
