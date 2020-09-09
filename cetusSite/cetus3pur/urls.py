from django.urls import path
from . import views

urlpatterns = [
        # ex: /cetus3pur/
    path('', views.index, name='index'),

        # view all 3rd parties
        # ex: /cetus3pur/tpv
    path('tpv/', views.ThirdPartiesView, name='ThirdPartiesView'),

        # view users for a specific 3rd party business
        # ex: /cetus3pur/tpvu
    path('tpvu/<int:thirdparty_id>/', views.ThirdPartyUsersTableView, name='ThirdPartyUsersTableView'),

        # view specific user
        # ex: /cetus3pur/user/1
    path('user/<int:user_id>/', views.ThirdPartyUserViewEdit, name='userviewedit'),

        # view RR managers
        # ex: /cetus3pur/rrm
    path('rrm/', views.RRRManagersView, name='RRRManagersView'),


]