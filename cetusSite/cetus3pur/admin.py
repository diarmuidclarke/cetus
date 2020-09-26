from django.contrib import admin
from .models import RRResponsibleManager
from .models import ThirdParty
from .models import ThirdPartyUser
from .models import EAB_Approval
from .models import EAB_Request
from .models import EAB_DataStoreSystem


admin.site.register(RRResponsibleManager)
admin.site.register(ThirdParty)
admin.site.register(ThirdPartyUser)
admin.site.register(EAB_Request)
admin.site.register(EAB_Approval)
admin.site.register(EAB_DataStoreSystem)

