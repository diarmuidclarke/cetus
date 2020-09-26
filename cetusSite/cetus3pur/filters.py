import django_filters

from .models import EAB_Approval, EAB_Request


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

