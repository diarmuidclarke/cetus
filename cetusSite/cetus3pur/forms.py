from django import forms
from django.forms.models import inlineformset_factory, formset_factory
from cetusSite import settings
from .models import EAB_Request, EAB_Approval


class EAB_Approve_Form(forms.ModelForm):

    date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text = 'Date of EAB approval',
    )


    class Meta:
        model = EAB_Approval
        exclude = ()
        fields = '__all__'
        # localized_fields = ('date',)


    # if creating, set request field of approval object
    def __init__(self, *args, **kwargs):
        if 'reqid' in kwargs:
            reqid = kwargs.pop('reqid', None)
            initial = kwargs.get('initial', {})
            initial['request'] = EAB_Request.objects.get(pk = reqid)
        super(EAB_Approve_Form, self).__init__(*args, **kwargs)
        self.fields['request'].disabled = True



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
