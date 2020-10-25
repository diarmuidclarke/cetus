from django.urls import path
from . import views

urlpatterns = [

    # root
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

    # View CETUS logged-in user's profile
    path('userprofile/', views.userprofile, name='CetusUser_Profile'),

    
    # Third Parties
        # view all 3rd parties
    path('tpv/', views.ThirdPartiesView, name='ThirdPartiesView'),
        # view users for a specific 3rd party business
    path('tpvu/<int:thirdparty_id>/', views.ThirdPartyUsersTableView, name='ThirdPartyUsersTableView'),
        # view specific user
    path('user/<int:user_id>/', views.ThirdPartyUserViewEdit, name='userviewedit'),
        # add Third party users
    path('addusers/<int:thirdparty_id>', views.ThirdPartyUsersAdd, name='AddNewUsers'),


    # R-R Managers
    path('rrm/', views.RRRManagersView, name='RRRManagersView'),


    # EAB Requests
    path('eabreq/create/',views.EAB_RequestCreate_cbv.as_view()),
    path('eabreq/edit/<int:pk>',views.EAB_RequestEdit_cbv.as_view()),
    path('eabreq/view/<int:pk>',views.EAB_RequestView_cbv.as_view()),


    # EAB Approvals
    path('eabappr/create/',views.EAB_ApproveCreate_cbv.as_view()),
    path('eabappr/create/<int:reqid>',views.EAB_ApproveCreate_cbv.as_view()),
    path('eabappr/edit/<int:pk>',views.EAB_ApproveEdit_cbv.as_view()),
    path('eabappr/view/<int:pk>',views.EAB_ApproveView_cbv.as_view()),
    path('eabreq_for_approval/',views.EAB_ReviewSelect, name='EAB_ReviewSelect'),


    # EAB "minutes" / records
    path('eabrecords_cbv/',views.EAB_Records_cbv.as_view()),


    # IT Actions
    path('eab_it_action/create/',views.EAB_IT_Action_Create_cbv.as_view()),  
    path('eab_it_action/edit/<int:appr_id>',views.EAB_IT_Action_Edit_cbv.as_view()),
    path('eab_it_action/view/<int:appr_id>',views.EAB_IT_Action_View_cbv.as_view()),
    path('eab_it_action/list', views.EAB_IT_Action_List.as_view()),
    # path('IT_actionlog/',views.IT_ActionLog, name='IT_actionlog'),


    # Data systems
    path('datastoresystems_cbv/',views.datastoresystems_cbv, name='datastoresystems_cbv'),


    # Audits    
    path('audit/',views.Audit, name='Audit'),	
    
]

