
from django import forms
from django.utils.translation import ugettext_lazy as _


class Searcher(forms.Form):
    search_string = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput)

    search_type = forms.ChoiceField(
        required=True,
        label=_('Search'),
        choices=(
            ('full', _('Basic search')),
            ('isbn', _('ISBN')),
            ('title', _('Title')),
            ('person_id', _('Author')),
            ('publisher_id', _('Publisher')),
            ('subject_id', _('Subject')),
            ),
        widget=forms.Select)
