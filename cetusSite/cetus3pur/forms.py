from django import forms
from django.forms.models import inlineformset_factory, formset_factory
from cetusSite import settings
from .models import EAB_Request


class EAB_Request_Form(forms.ModelForm):

    date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y'),
    )


    class Meta:
        model = EAB_Request
        exclude = ()
        localized_fields = ('date',)


    def __init__(self, *args, **kwargs):
        print('todo')