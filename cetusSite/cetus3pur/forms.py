from django import forms
from django.forms.models import inlineformset_factory, formset_factory
from cetusSite import settings
from .models import EAB_Request


class EAB_Request_Form(forms.ModelForm):

    date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text = 'Date of EAB request',
    )


    class Meta:
        model = EAB_Request
        exclude = ()
        fields = '__all__'
        # localized_fields = ('date',)

    """
    # If a toolId is set then set that field by default on the new form
    def __init__(self, *args, **kwargs):
        if 'requestID' in kwargs:
            requestID = kwargs.pop('requestID', None)
            initial = kwargs.get('initial', {})
            initial['request'] = requestID
        super(EAB_Request_Form, self).__init__(*args, **kwargs)
        # Make the Tool field read-only
        self.fields['request'].disabled = True
    """
