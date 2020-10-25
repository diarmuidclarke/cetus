import django_filters

from .models import EAB_Approval, EAB_Request, EAB_IT_Action


class EAB_RecordFilter(django_filters.FilterSet):
    thirdparty = django_filters.CharFilter(lookup_expr='icontains')
    datastoresystem = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = EAB_Approval
        fields = [
            'request',
            'date',
            'approver_userid',
            'decision',
            'ecm_comment',
        ]



class EAB_IT_Actions_Filter(django_filters.FilterSet):
    class Meta:
        model = EAB_IT_Action
        fields = [
            'date_completed',
            'IT_executor_userid',
            'completed',
        ]
