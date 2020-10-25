from django import forms
from django.forms.models import inlineformset_factory, formset_factory
from django.forms import ModelChoiceField
from cetusSite import settings
from pprint import pprint
import datetime
from rest_framework.mixins import UpdateModelMixin
from django_select2.forms import ModelSelect2Widget, Select2Widget
from .models import (
    EAB_Request,
    EAB_Approval,
    EAB_DataStoreSystem,
    EAB_DataStoreSystemArea,
    EAB_IT_Action,
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
        initial = kwargs.get("initial", {})
        if "reqid" in kwargs:
            reqid = kwargs.pop("reqid", None)
            initial["request"] = EAB_Request.objects.get(pk=reqid)

        initial['approver_userid'] =  kwargs.pop("user", None)
        dt = datetime.datetime.now()
        dts = dt.strftime('%d/%m/%Y')
        initial['date'] = dts
        super(EAB_Approve_Form, self).__init__(*args, **kwargs)
        
        self.fields['date'].disabled = True
        self.fields['request'].disabled = True
        self.fields['approver_userid'].disabled = True






class EAB_Request_Form(UpdateModelMixin, forms.ModelForm):

    date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(format="%d/%m/%Y"),
        help_text="Date of EAB request",
    )

    data_store_system = forms.ModelChoiceField(
        queryset=EAB_DataStoreSystem.objects.all(),
        widget=Select2Widget(
            attrs={
                "data-width": "20em",
            }
        )
    )

    data_store_system_area = forms.ModelChoiceField(
        queryset=EAB_DataStoreSystemArea.objects.all(),
        widget=ModelSelect2Widget(
            model=EAB_DataStoreSystemArea,
            search_fields=["name__icontains"],
            attrs={
                "data-width": "20em",
                'data-minimum-input-length': 0,
            },
            dependent_fields={"data_store_system": "dss"},
        ),
    )

    class Meta:
        model = EAB_Request
        exclude = ()
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial", {})
        initial['reqstr_userid'] =  kwargs.pop("user", None)
        dt = datetime.datetime.now()
        dts = dt.strftime('%d/%m/%Y')
        initial['date'] = dts
        super(EAB_Request_Form, self).__init__(*args, **kwargs)
        
        self.fields['date'].disabled = True
        self.fields['reqstr_userid'].disabled = True




class EAB_IT_Action_Form(forms.ModelForm):

    date_assigned = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(format="%d/%m/%Y"),
        help_text="when action assigned",
    )

    date_completed = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(format="%d/%m/%Y"),
        help_text="when action completed",
    )


    class Meta:
        model = EAB_IT_Action
        exclude = ()
        fields = "__all__"


    # if creating, set request field of approval object
    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial", {})
        if "appr_id" in kwargs:
            appr_id = kwargs.pop("appr_id", None)
            initial["approval"] = EAB_Approval.objects.get(pk=appr_id)

        initial['IT_executor_userid'] =  kwargs.pop("user", None)

        dt = datetime.datetime.now()
        dts = dt.strftime('%d/%m/%Y')
        initial['date_completed'] = dts

        super(EAB_IT_Action_Form, self).__init__(*args, **kwargs)
        


        self.fields['date_assigned'].disabled = True
        self.fields['date_completed'].disabled = True
        self.fields['approval'].disabled = True
        self.fields['IT_executor_userid'].disabled = True
