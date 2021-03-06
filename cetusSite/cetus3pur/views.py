from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import forms
from django.views.decorators.csrf import csrf_exempt
from .models import ThirdPartyUser
from .models import ThirdParty
from .models import EAB_Request
from .models import EAB_DataStoreSystem
from .models import EAB_DataStoreSystemArea
from .models import EAB_Approval
from .models import EAB_IT_Action
from django.contrib.auth.models import User as authUser
import datetime
import dateutil.parser as parser
import re
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from datetime import date
from pprint import pprint
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView
from .tables import EAB_RecordsTable, EAB__IT_Actions_Table
from .filters import EAB_RecordFilter, EAB_IT_Actions_Filter
from .forms import EAB_Request_Form, EAB_Approve_Form, EAB_IT_Action_Form
from django.contrib.auth.models import Permission
from collections import OrderedDict


# front page - third parties by default
def index(request):
    return render(request, 'cetus3pur/index.html', )




# let user see details about their CETUS user account
def userprofile(request):
    
    ####################################################
    # get a sorted list of all possible permissions
    permissions = set()
    tmp_superuser = get_user_model()(
      is_active=True,
      is_superuser=True
    )

        # We go over each AUTHENTICATION_BACKEND and try to fetch a list of permissions
    for backend in auth.get_backends():
      if hasattr(backend, "get_all_permissions"):
        permissions.update(backend.get_all_permissions(tmp_superuser))

        # Make an unique list of permissions sorted by permission name.
    sorted_list_of_permissions = sorted(list(permissions))

    ####################################################
    # get a sorted list of __curremt__ user permissions
    user = request.user
    userpermies = set()
    userpermies = user.user_permissions.all() | Permission.objects.filter(group__user=user)

    list_uperms = []
    for uperm in userpermies:
        list_uperms.append(str(uperm))
        
        # sorted, no duplicates
    sorted_list_uperms = list(OrderedDict.fromkeys(list_uperms))



    context = {  'permies' : sorted_list_of_permissions,  'userpermies' : sorted_list_uperms }
    
    return render(request, 'cetus3pur/CetusUser_Profile.html', context)




# login
@csrf_exempt
class CETUSUserLogin(LoginView):
    template_name = 'LoginView_form.html'



# logout
@csrf_exempt
def CETUSUser_Logout(request):
    if request.method == 'GET':
        logout(request) 

        return render(request, 'cetus3pur/CETUSUser_Logout.html', )
    else:
        return render(request, 'cetus3pur/CETUSUser_Logout.html', )



# view 3rd party businesses
def ThirdPartiesView(request):
    latest_3rdparty_list = ThirdParty.objects.order_by('legal_entity_name')
    dict3p = {}
    for tp in latest_3rdparty_list:        
        dict3p[tp.legal_entity_name] = str(len(ThirdPartyUser.objects.filter(employer = tp)))


    context = {'latest_3p_list': latest_3rdparty_list, 'dict3p':dict3p}
    return render(request, 'cetus3pur/ThirdPartiesView.html', context)





# view all users for a 3rd party
def ThirdPartyUsersTableView(request, thirdparty_id):
    user_employer = ThirdParty.objects.get(pk = thirdparty_id)

    userlist = []
    for user in ThirdPartyUser.objects.filter(employer = user_employer).values():
        user.pop('employer_id')
        userlist.append(user)

    context = {'userlist': userlist, 'useremp' : user_employer, 'thirdparty_id' : thirdparty_id }
    return render(request, 'cetus3pur/ThirdPartyUsersTableView.html', context)




# the edit page for one 3rd party user
@csrf_exempt
def ThirdPartyUserViewEdit(request, user_id):

    if request.method == 'POST':
        # get form data
        form_firstname = request.POST.get('user_firstname')
        form_familyname = request.POST.get('user_familyname')
        form_employee_id = request.POST.get('user_employee_id')
        form_userac_name = request.POST.get('user_acname')
        form_userac_expiry = request.POST.get('user_acexpiry')

        ## todo - clean/validate data

        # store in model and save
        user = ThirdPartyUser.objects.get(pk = user_id)
        user.firstname = form_firstname
        user.familyname = form_familyname
        user.employee_id = form_employee_id
        user.userac_name = form_userac_name
        date_time_obj =datetime.datetime.strptime(form_userac_expiry, '%Y-%m-%d')     # convert text back to a datetime object from bulma datefield string
        user.userac_expirydate = date_time_obj
        user.save()

        bulma_friendly_date = user.userac_expirydate.strftime("%Y-%m-%d") 

        return render(request, 'cetus3pur/userviewedit.html', {'tp_user': user, 'bulma_date': bulma_friendly_date}  )

    else:
        user = ThirdPartyUser.objects.get(pk = user_id)
        
        # bulma datefields seem to need this exact format
        bulma_friendly_date = user.userac_expirydate.strftime("%Y-%m-%d") 

        return render(request, 'cetus3pur/userviewedit.html', {'tp_user': user, 'bulma_date': bulma_friendly_date} )




# the add new users page
@csrf_exempt
def ThirdPartyUsersAdd(request, thirdparty_id):
    if request.method == 'POST':
        error_text = ""

        line = request.POST.get('new_user_specs')
        line_num = 0
        lines_processed_ok = 0

        line_list = line.split('\r\n')

        for line in line_list:
            line_num += 1            
            list_tokens = line.split(',')

            # trim leading/trailing whitespace
            new_list_tokens = []
            for token in list_tokens:
                new_list_tokens.append(token.strip())
            list_tokens = new_list_tokens

            # right number of tokens?
            if(len(list_tokens) != 5 and len(list_tokens) != 2):
                error_text += "line " + str(line_num) + " has wrong number of tokens --> " + line + "\r\n"
                continue

            # new user
            if(len(list_tokens) == 5):
                # check for duplicates (this vs db) by employee ID number
                users  = ThirdPartyUser.objects.filter(employee_id = list_tokens[2])
                if(len(users)>0):
                    error_text += "line " + str(line_num) + " is duplicate of entry in database for employee ID " + list_tokens[2] + " --> " + line + "\r\n"
                    continue

                # create the new user in the model and save to Database
                date_obj = parser.parse(list_tokens[4], dayfirst = True)
                tpu = ThirdPartyUser.create(list_tokens[0], list_tokens[1], list_tokens[2], list_tokens[3] , date_obj, thirdparty_id)
                tpu.save()

                # update status
                lines_processed_ok += 1
                error_text += "line " + str(line_num) + " OK\r\n"
            

            # update expiry date
            if(len(list_tokens) == 2):
                # check for duplicates (this vs db) by employee ID number
                users  = ThirdPartyUser.objects.filter(userac_name = list_tokens[0])
                if(len(users)!=1):
                    error_text += "line " + str(line_num) + " for update of " + list_tokens[0] + "'s expiry date, no record found of this user --> " + line + "\r\n"
                    continue

                # create the new user in the model and save to Database
                user = users[0]
                date_obj = parser.parse(list_tokens[1], dayfirst = True) # parse text that might be one of many possible representations of a date
                date_as_yyyy_mm_dd = str(date_obj).split(' ')[0]
                date_time_obj = datetime.datetime.strptime(date_as_yyyy_mm_dd, '%Y-%m-%d')     # convert text back to a datetime object from bulma datefield string
                user.userac_expirydate = date_time_obj
                user.save()

                # update status
                lines_processed_ok += 1
                error_text += "line " + str(line_num) + " OK -- user " + list_tokens[0] + " expiry date updated to " + str(date_obj) + "\r\n"


        error_text += "Lines Processed Succesfully : " + str(lines_processed_ok) + "\n"
        error_text += "Done."

        # display status
        user_employer = ThirdParty.objects.get(pk = thirdparty_id)
        return render(request, 'cetus3pur/AddNewUsers.html', {'thirdparty_id': thirdparty_id, 'employer': user_employer, 'error_text': error_text} )

    else:
        error_text =""
        user_employer = ThirdParty.objects.get(pk = thirdparty_id)
        return render(request, 'cetus3pur/AddNewUsers.html', {'thirdparty_id': thirdparty_id, 'employer': user_employer, 'error_text' : error_text} )


def datastoresystems_cbv(request):
    
    report = []
    for dss in EAB_DataStoreSystem.objects.all():
        report.append(dss.name + ' -- ' + dss.datastoresystem_approved)

        dssa_list = EAB_DataStoreSystemArea.objects.filter(dss__id=dss.id)
        if(len(dssa_list) == 0):
            report.append('')

        for dssa in dssa_list:
            report.append('    > ' + dssa.name)
            report.append('        classifications' )
            if(dssa.export_classification_PL9009c):
                report.append('        PL9009.c')
            if(dssa.export_classification_EU_dualuse):
                report.append('        EU dual use')
            if(dssa.export_classification_US_NLR):
                report.append('        US NLR.c')
            report.append('')

    context = { 'report' : report }
    return render(request, 'cetus3pur/datastoresystems.html', context)


# RR  managers
def RRRManagersView(request):
    rrm = authUser.objects.filter(groups__name='GROUP_RR_RESP_MGR')
    rrukm = authUser.objects.filter(groups__name='GROUP_RR_UK_MGR')
    
    context = {'rrm': rrm , 'rrukm' : rrukm }
    return render(request, 'cetus3pur/rrrmanager.html', context)




# EAB Approve - create
class EAB_ApproveCreate_cbv(CreateView):
    model = EAB_Approval
    template_name = "cetus3pur/EAB_ApproveCreate.html"
    form_class = EAB_Approve_Form
    extra_context = {}


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return "../view/{id}".format(id=self.object.id)

    def form_valid(self, form):
        self.object = form.save()

        # create the IT Action object
        dt = datetime.datetime.now()
        ita = EAB_IT_Action.create(nappr=self.object.id, ndate_assigned = dt, ndate_completed = None , nuser = self.request.user, ncompleted= False)
        ita.save()

        return HttpResponseRedirect(self.get_success_url())


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['reqid'] = self.kwargs['reqid']
        return kwargs





# EAB Approve -- edit
class EAB_ApproveEdit_cbv(UpdateView):
    model = EAB_Approval
    template_name = "cetus3pur/EAB_ApproveCreate.html"
    form_class = EAB_Approve_Form


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return "../view/{id}".format(id=self.kwargs['pk'])




# EAB Approve -- view
class EAB_ApproveView_cbv(UpdateView):
    model = EAB_Approval
    template_name = "cetus3pur/EAB_ApproveCreate.html"
    form_class = EAB_Approve_Form




    
# EAB Records - show all past approval decisions
class EAB_Records_cbv(SingleTableMixin, FilterView):
    model = EAB_Approval
    table_class = EAB_RecordsTable
    template_name = "cetus3pur/EAB_Records_cbv.html"
    filterset_class = EAB_RecordFilter




# EAB Request - create
class EAB_RequestCreate_cbv(CreateView):
    model = EAB_Request
    template_name = "cetus3pur/EAB_RequestCreate.html"
    form_class = EAB_Request_Form
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return "../view/{id}".format(id=self.object.id)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



# EAB Request -- edit
class EAB_RequestEdit_cbv(UpdateView):
    model = EAB_Request
    template_name = "cetus3pur/EAB_RequestCreate.html"
    form_class = EAB_Request_Form


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return "../view/{id}".format(id=self.kwargs['pk'])



# EAB Request -- view
class EAB_RequestView_cbv(UpdateView):
    model = EAB_Request
    template_name = "cetus3pur/EAB_RequestCreate.html"
    form_class = EAB_Request_Form




# select an EAB request from a list, to approve or go back into edit
def EAB_ReviewSelect(request):

    reqlist = EAB_Request.objects.select_related('tp').all()
    approvalslist = EAB_Approval.objects.all()

    # dictionary that maps request IDs to approval IDs
    # e.g. dict[req_id] = appr_id
    dict_req2appr = { }
    for appr in approvalslist:
        dict_req2appr[appr.request.id] = appr.id

    list_reqs_with_no_approvals = []
    dict_req_has_apprv = {}
    for req in reqlist:
        if(req.id in dict_req2appr):
            dict_req_has_apprv[req.id] = True
        else:
            dict_req_has_apprv[req.id] = False
            list_reqs_with_no_approvals.append(req)


    # context = { 'reqlist': reqlist, 'approvalslist': approvalslist, 'dict_req2appr' : dict_req2appr, 'dict_req_has_apprv' : dict_req_has_apprv}
    context = { 'reqlist': list_reqs_with_no_approvals, 'approvalslist': approvalslist, 'dict_req2appr' : dict_req2appr, 'dict_req_has_apprv' : dict_req_has_apprv}

    return render(request, 'cetus3pur/EAB_ReviewSelect.html', context)





class EAB_IT_Action_Create_cbv(CreateView):
    model = EAB_IT_Action
    template_name = "cetus3pur/EAB_IT_Action_Create.html"
    form_class = EAB_Approve_Form
    extra_context = {}


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return "../view/{id}".format(id=self.object.id)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['appr_id'] = self.kwargs['appr_id']
        return kwargs





class EAB_IT_Action_Edit_cbv(UpdateView):
    model = EAB_IT_Action
    template_name = "cetus3pur/EAB_IT_Action_Create.html"
    form_class = EAB_IT_Action_Form
    pk_url_kwarg='appr_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return "../view/{id}".format(id=self.kwargs['appr_id'])


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        # kwargs['appr_id'] = self.kwargs['appr_id']
        return kwargs




# EAB Approve -- view
class EAB_IT_Action_View_cbv(UpdateView):
    model = EAB_IT_Action
    template_name = "cetus3pur/EAB_IT_Action_Create.html"
    form_class = EAB_IT_Action_Form
    pk_url_kwarg='appr_id'




class EAB_IT_Action_List(SingleTableMixin, FilterView):
    model = EAB_IT_Action
    table_class = EAB__IT_Actions_Table
    filterset_class = EAB_IT_Actions_Filter
    template_name = "cetus3pur/EAB_IT_Actions_List.html"




# Audit
def Audit(request):
    context = { }
    return render(request, 'cetus3pur/Audit.html', context)




