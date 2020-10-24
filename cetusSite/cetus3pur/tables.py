import django_tables2 as tables
from django.utils.html import format_html, format_html_join
from .models import EAB_Request, EAB_Approval, EAB_IT_Action



class EAB_RecordsTable(tables.Table):

    class Meta:
        model = EAB_Approval
        exclude = (
            "id",
            "IT_comment",
        )
        sequence = (
            "date",
            "request",
            "decision",
            "ecm_comment",
            "ipm_comment",
        )
        attrs = {
            "class": "table is-bordered is-striped is-narrow is-hoverable is-fullwidth"
        }




class EAB__IT_Actions_Table(tables.Table):

    class Meta:
        model = EAB_IT_Action
        exclude = (
            "id",
        )

        sequence = (
            "date_assigned",
            "approval",
            "completed",
            "IT_executor_userid",
            "date_completed",
        )
        attrs = {
            "class": "table is-bordered is-striped is-narrow is-hoverable is-fullwidth"
        }
