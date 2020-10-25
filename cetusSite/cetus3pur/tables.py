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
        )

        sequence = (
            "id",
            "date_assigned",
            "approval",
            "completed",
            "IT_executor_userid",
            "date_completed",
        )

        attrs = {
            "class": "table is-bordered is-striped is-narrow is-hoverable is-fullwidth"
        }
        

    # render the ID column as links to the edit for that IT action
    def render_id(self, value):
        return format_html(
            "<a class=\"button is-link is-small\" href=\"/cetus3pur/eab_it_action/edit/{0}\">Mark Complete</a>",
            value
        )
