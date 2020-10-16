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
        widget=forms.Select(attrs={"onchange": "document.getElementById('data_store_system_changed').value = 'Yes';this.form.submit()"}),        
    )

    Data_Store_Changed = None


    class Meta:
        model = EAB_Request
        exclude = ()
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super(EAB_Request_Form, self).__init__(*args,**kwargs)
        form_data = kwargs.pop('data', None)
        if form_data:
            if form_data['data_store_system_changed'] == "Yes":
                self.Data_Store_Changed = True
                dss_pk = form_data['data_store_system']
                self.fields['data_store_system_area'].queryset = EAB_DataStoreSystemArea.objects.filter(dss__pk = dss_pk)
    
    def clean(self):
        cleaned_data = super(EAB_Request_Form, self).clean()
        # If this change was trigged by the drop down being selected then hide errors and warnings
        if self.Data_Store_Changed:
            for error in self.errors:
                self.errors[error] = []
        return cleaned_data


