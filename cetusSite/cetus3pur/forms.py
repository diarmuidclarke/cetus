from django import forms
from django.forms.models import inlineformset_factory, formset_factory
from django.forms import ModelChoiceField
from cetusSite import settings
from pprint import pprint
from rest_framework.mixins import UpdateModelMixin
from .models import (
    EAB_Request,
    EAB_Approval,
    EAB_DataStoreSystem,
    EAB_DataStoreSystemArea,
)


class EAB_Approve_Form(forms.ModelForm):

    date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(format="%d/%m/%Y"),
        help_text="Date of EAB approval",
    )

    class Meta:
        model = EAB_Approval
        exclude = ()
        fields = "__all__"

    # if creating, set request field of approval object
    def __init__(self, *args, **kwargs):
        if "reqid" in kwargs:
            reqid = kwargs.pop("reqid", None)
            initial = kwargs.get("initial", {})
            initial["request"] = EAB_Request.objects.get(pk=reqid)
        super(EAB_Approve_Form, self).__init__(*args, **kwargs)
        self.fields["request"].disabled = True



class EAB_Request_Form(UpdateModelMixin, forms.ModelForm):

    date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(format="%d/%m/%Y"),
        help_text="Date of EAB request",
    )

    data_store_system = forms.ModelChoiceField(
        queryset=EAB_DataStoreSystem.objects.all(),
        widget=forms.Select(attrs={"onchange": "this.form.submit()"}),        
    )


    class Meta:
        model = EAB_Request
        exclude = ()
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        pprint(kwargs)
        super(EAB_Request_Form, self).__init__(*args,**kwargs)
        databit = kwargs.pop('data', None)
        if databit:
            dss_pk = databit['data_store_system']
            pprint('DSS PK:' + str(dss_pk))
            self.fields['data_store_system_area'].queryset = EAB_DataStoreSystemArea.objects.filter(dss__pk = dss_pk)


    def partial_update(*args, **kwargs):
        pprint(kwargs)
