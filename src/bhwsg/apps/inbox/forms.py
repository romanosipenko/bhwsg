import uuid
from django import forms
from django.forms.models import inlineformset_factory

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
    Inbox, DeleteRule, extra=0, can_delete=True,
    form=DeleteRuleForm
)
