from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.views.decorators.csrf import csrf_exempt
from .models import ThirdPartyUser
from .models import ThirdParty
from .models import RRResponsibleManager
from .models import EAB_Request
from .models import EAB_Approval
import datetime
import dateutil.parser as parser
import re
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from datetime import date
from pprint import pprint


# front page - third parties by default
def index(request):
    return render(request, 'cetus3pur/index.html', )




# let user see details about their CETUS user account
def userprofile(request):
    permissions = set()
    tmp_superuser = get_user_model()(
      is_active=True,
      is_superuser=True
    )

    # We go over each AUTHENTICATION_BACKEND and try to fetch
    # a list of permissions
    for backend in auth.get_backends():
      if hasattr(backend, "get_all_permissions"):
        permissions.update(backend.get_all_permissions(tmp_superuser))

    # Make an unique list of permissions sorted by permission name.
    sorted_list_of_permissions = sorted(list(permissions))
    perm_as_str = ""
    for perm in sorted_list_of_permissions:
        perm_as_str += (perm + "<br>")

    return render(request, 'cetus3pur/CetusUser_Profile.html', { 'permies' : sorted_list_of_permissions} )




# login
@csrf_exempt
class CETUSUserLogin(LoginView):
    template_name = 'LoginView_form.html'



# logout
@csrf_exempt
def CETUSUser_Logout(request):
    if request.method == 'GET':
        logout(request) 
        if request.user.is_authenticated:
            print('+++++++still logged in')
        else:
            print('+++++now logged out')


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




# RR  managers
def RRRManagersView(request):
    rrm = RRResponsibleManager.objects.values()
    context = {'rrm': rrm }
    return render(request, 'cetus3pur/rrrmanager.html', context)


# EAB Request Creation
def EAB_RequestCreate(request):
    if request.method == 'POST':
        # get form data
        datereq = request.POST.get('eabreq_date')
        reqstr_user_id = request.POST.get('eabreq_user_id')
        tpsel = request.POST.get('eabreq_tp_selector')
        datastore = request.POST.get('eabreq_datastore')
        dataowner_user_id = request.POST.get('eabreq_dataowner_user_id')
        export_claim = request.POST.get('eabreq_datastore_exportclaim')
        ipecr = request.POST.get('eabreq_ipecr')

        # make a request
        date_obj = parser.parse(datereq, dayfirst = True)
        tpid =   int(re.search(r"\[([A-Za-z0-9_]+)\]", tpsel).group(1))
        req = EAB_Request.create(date_obj, reqstr_user_id, tpid, datastore,dataowner_user_id, export_claim, ipecr)
        req.save()
        
        # make a blank approval for the request
        appr_blank = EAB_Approval.create(nreq=req.id, ndate=date_obj, napprover='todo', ndecision='NYR', necm_comment='not yet reviewed', 
        nipm_comment='not yet reviewed', nIT_comment='not yet reviewed')
        appr_blank.request = req
        appr_blank.save()
        


        # context = { 'req_id' : req.id }
        # return render(request, 'cetus3pur/EAB_RequestSubmitted.html', context)

        reqlist = EAB_Request.objects.filter().values()
        context = { 'reqlist': reqlist}
        return render(request, 'cetus3pur/EAB_ReviewSelect.html', context)

    else:
        #date
        datetoday = date.today()
        bulma_friendly_date = datetoday.strftime("%Y-%m-%d") 

        # third party list
        tplist = ThirdParty.objects.filter().values()
        
        context = { 'bulma_date_now' : bulma_friendly_date, 'user_id_requester' : request.user, 'tplist' : tplist}
        return render(request, 'cetus3pur/EAB_RequestCreate.html', context)



# EAB Request edit
def EAB_RequestEdit(request, reqid):
    if request.method == 'POST':
        # get form data
        datereq = request.POST.get('eabreq_date')
        reqstr_user_id = request.POST.get('eabreq_user_id')
        tpsel = request.POST.get('eabreq_tp_selector')
        datastore = request.POST.get('eabreq_datastore')
        dataowner_user_id = request.POST.get('eabreq_dataowner_user_id')
        export_claim = request.POST.get('eabreq_datastore_exportclaim')
        ipecr = request.POST.get('eabreq_ipecr')

        date_obj = parser.parse(datereq, dayfirst = True)
        tpid =   int(re.search(r"\[([A-Za-z0-9_]+)\]", tpsel).group(1))
        tp = ThirdParty.objects.get(pk=tpid)

        # update the request
        req = EAB_Request.objects.get(pk=reqid)
        req.data = date_obj
        req.reqstr_userid = reqstr_user_id
        req.tp = tp
        req.datastore = datastore
        req.data_owner_userid = dataowner_user_id
        req.data_store_export_claim = export_claim
        req.ipecr = ipecr        
        req.save()
        
        reqlist = EAB_Request.objects.filter().values()
        context = { 'reqlist': reqlist}
        return render(request, 'cetus3pur/EAB_ReviewSelect.html', context)

    else:
        #date
        datetoday = date.today()
        bulma_friendly_date = datetoday.strftime("%Y-%m-%d") 

        # third party list
        tplist = ThirdParty.objects.filter().values()
        
        context = { 'bulma_date_now' : bulma_friendly_date, 'user_id_requester' : request.user, 'tplist' : tplist}
        return render(request, 'cetus3pur/EAB_RequestCreate.html', context)



# select an EAB request from a list, to approve or go back into edit
def EAB_ReviewSelect(request):

    reqlist = EAB_Request.objects.select_related('tp').all()
    approvalslist = EAB_Approval.objects.all()

    # for req in reqlist:
    #     pprint(req.tq.select_related('tq'))

    context = { 'reqlist': reqlist, 'approvalslist': approvalslist}

    return render(request, 'cetus3pur/EAB_ReviewSelect.html', context)



# EAB Approvals - do an approval
def EAB_ReviewApprove(request, approval_id):

    if request.method == 'POST':
        # get form data
        date_approval = request.POST.get('eabrev_date')
        aaprv_id = request.POST.get('eabrev_approver_user_id')
        decision = request.POST.get('eabreview_decision_selector')
        ecm_comment = request.POST.get('eabrev_ecm_comment')
        ipm_comment = request.POST.get('eabrev_IPM_comment')
        IT_comment = request.POST.get('eabrev_IT_comment')

        date_obj = parser.parse(date_approval, dayfirst = True)

        apprv = EAB_Approval.objects.get(pk=approval_id)
        apprv.date = date_obj
        apprv.approver_userid = aaprv_id
        apprv.decision = 'APP'
        apprv.ecm_comment = ecm_comment
        apprv.ipm_comment = ipm_comment
        apprv.IT_comment = IT_comment
        apprv.save()
        # review = EAB_Approval.create(reqid, date_obj, aaprv_id, decision, ecm_comment, ipm_comment, IT_comment)
        # review.save()

        context = {}
        return render(request, 'cetus3pur/EAB_Records.html', context)

    else:
        # find any approvals in progress from previous review of a request
        approval = EAB_Approval.objects.get(pk = approval_id)

        # find the request we're trying to approve
        req = approval.request


        # datetoday = date.today()
        bulma_friendly_date = approval.date.strftime("%Y-%m-%d") 
        context = { 'reqid' : req.id,
                    'req':req,
                    'approval':approval,
                    'bulma_date':bulma_friendly_date, 
                    'user':request.user
                }

        return render(request, 'cetus3pur/EAB_ReviewApprove.html', context)






# EAB Records - show all past approval decisions
def EAB_Records(request):
    approvals = EAB_Approval.objects.select_related('request').all()
    requests = EAB_Request.objects.select_related('tp').all()

    context = { 'approvals':approvals, 'requests':requests  }
    return render(request, 'cetus3pur/EAB_Records.html', context)

# IT Action Log
def IT_ActionLog(request):
	context = {}
	return render(request, 'cetus3pur/IT_actionlog.html',context)


# Audit
def Audit(request):
    context = { }
    return render(request, 'cetus3pur/Audit.html', context)