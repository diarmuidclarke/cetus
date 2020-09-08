from django.urls import path
from . import views

urlpatterns = [
        # ex: /cetus3pur/
    path('', views.index, name='index'),

        # ex: /cetus3pur/tpv
    path('tpv/', views.ThirdPartiesView, name='ThirdPartiesView'),

        # ex: /cetus3pur/rrm
    path('rrm/', views.RRRManagersView, name='RRRManagersView'),

        # ex: /cetus3pur/
    path('user/<int:thirdparty_id>/', views.ThirdPartyUsersTableView, name='ThirdPartyUsersTableView'),

]
