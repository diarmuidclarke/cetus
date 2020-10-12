from django import forms
from django.forms.models import inlineformset_factory, formset_factory
from cetusSite import settings
from pprint import pprint
from .models import (
    EAB_Request,
    EAB_Approval,
    EAB_DataStoreSystem,
    EAB_DataStoreSystemArea,
)
from django.forms import ModelChoiceField


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
        # localized_fields = ('dssa',)

    # if creating, set request field of approval object
    def __init__(self, *args, **kwargs):
        if "reqid" in kwargs:
            reqid = kwargs.pop("reqid", None)
            initial = kwargs.get("initial", {})
            initial["request"] = EAB_Request.objects.get(pk=reqid)
        super(EAB_Approve_Form, self).__init__(*args, **kwargs)
        self.fields["request"].disabled = True


class EAB_Request_Form(forms.ModelForm):

    date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(format="%d/%m/%Y"),
        help_text="Date of EAB request",
    )

    data_store_system = forms.ModelChoiceField(
        queryset=EAB_DataStoreSystem.objects.all(),
        # attributes = { 'cols':80 }
        widget=forms.Select(attrs={"onchange": "this.form.submit()"}),
    )

    # dssa = forms.ModelChoiceField(
    #     queryset = EAB_DataStoreSystemArea.objects.all()
    # )

    class Meta:
        model = EAB_Request
        # widgets = { 'data_store_system':ModelChoiceField(attrs={'cols':80}) }
        exclude = ()
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        pprint(kwargs)
        databit = kwargs.pop('data', None)
        if databit:
            dss_pk = databit['data_store_system']
            pprint('DSS PK:' + str(dss_pk))
            super(EAB_Request_Form, self).__init__(*args,**kwargs)
            self.fields['data_store_system_area'].queryset = EAB_DataStoreSystemArea.objects.filter(dss__pk = dss_pk)
