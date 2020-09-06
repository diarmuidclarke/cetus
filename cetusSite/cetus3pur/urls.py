from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
        # ex: /cetus3pur/5/
    path('<int:thirdparty_id>/', views.ThirdPartyUsersTableView, name='ThirdPartyUsersTableView'),
]
