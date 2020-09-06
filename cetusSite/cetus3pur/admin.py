from django.contrib import admin
from .models import RRResponsibleManager
from .models import ThirdParty
from .models import ThirdPartyUser

admin.site.register(RRResponsibleManager)
admin.site.register(ThirdParty)
admin.site.register(ThirdPartyUser)
