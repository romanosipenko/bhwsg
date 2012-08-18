from django import forms
from django.forms.models import inlineformset_factory

from models import Inbox, ForwardRule, DeleteRule


class ForwardRule(forms.ModelForm):
    class Meta:
        model = ForwardRule

ForwardRuleFormSet = inlineformset_factory(
    Inbox, ForwardRule, extra=0, can_delete=True,
    form=ForwardRule
)


class DeleteRule(forms.ModelForm):
    class Meta:
        model = DeleteRule

DeleteRuleFormSet = inlineformset_factory(
    Inbox, DeleteRule, extra=0, can_delete=True,
    form=ForwardRule
)
