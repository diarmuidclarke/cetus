from django import forms
from django.forms.models import inlineformset_factory, formset_factory
from django.forms import ModelChoiceField
from cetusSite import settings
from pprint import pprint
from rest_framework.mixins import UpdateModelMixin
from django_select2.forms import ModelSelect2Widget, Select2Widget
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


