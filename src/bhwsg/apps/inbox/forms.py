import uuid
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.db import transaction
from django.db import IntegrityError

from core.utils import generate_username
from models import Inbox, ForwardRule, DeleteRule


class InboxCreateForm(forms.ModelForm):
    class Meta:
        model = Inbox
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        super(InboxCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.password = uuid.uuid4()
        self.instance.owner = self.owner
        return super(InboxCreateForm, self).save(*args, **kwargs)


class ForwardRuleForm(forms.ModelForm):
    class Meta:
        model = ForwardRule

ForwardRuleFormSet = inlineformset_factory(
    Inbox, ForwardRule, extra=1, can_delete=True,
    form=ForwardRuleForm
)


class DeleteRuleForm(forms.ModelForm):
    class Meta:
        model = DeleteRule

DeleteRuleFormSet = inlineformset_factory(
    Inbox, DeleteRule, extra=1, can_delete=True,
    form=DeleteRuleForm
)


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already taken!")
        else:
            return email

    def save(self, *args, **kwargs):
        for username in generate_username(self.cleaned_data['email']):
            try:
                sid = transaction.savepoint()
                user = User.objects.create_user(
                    username, self.cleaned_data['email'], '1'
                )
            except IntegrityError:
                transaction.savepoint_rollback(sid)
            else:
                # Send mail to user here
                return user
