from django.urls import path
from . import views

urlpatterns = [
        # ex: /cetus3pur/
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

        # ex: /cetus3pur/userprofile/
    path('userprofile/', views.userprofile, name='CetusUser_Profile'),

        # view all 3rd parties
        # ex: /cetus3pur/tpv
    path('tpv/', views.ThirdPartiesView, name='ThirdPartiesView'),

        # view users for a specific 3rd party business
        # ex: /cetus3pur/tpvu
    path('tpvu/<int:thirdparty_id>/', views.ThirdPartyUsersTableView, name='ThirdPartyUsersTableView'),

        # view specific user
        # ex: /cetus3pur/user/1
    path('user/<int:user_id>/', views.ThirdPartyUserViewEdit, name='userviewedit'),

        # add new third party users
        # ex: /cetus3pur/AddNewUsers/1
    path('addusers/<int:thirdparty_id>', views.ThirdPartyUsersAdd, name='AddNewUsers'),

        # view RR managers
        # ex: /cetus3pur/rrm
    path('rrm/', views.RRRManagersView, name='RRRManagersView'),

    path('eabreq/',views.EAB_RequestCreate, name='EAB_RequestCreate'),

    path('eabreq_for_approval/',views.EAB_ReviewSelect, name='EAB_ReviewSelect'),

    path('eabreviewapprove/<int:approval_id>',views.EAB_ReviewApprove, name='EAB_ReviewApprove'),
    path('eabreviewapprove/',views.EAB_ReviewApprove, name='EAB_ReviewApprove'),

    path('eabrecords/',views.EAB_Records, name='EAB_Records'),
    path('audit/',views.Audit, name='Audit'),
]
