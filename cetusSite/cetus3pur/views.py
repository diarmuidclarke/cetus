from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.views.decorators.csrf import csrf_exempt
from .models import ThirdPartyUser
from .models import ThirdParty
from .models import RRResponsibleManager
import datetime
import dateutil.parser as parser







# front page - third parties by default
def index(request):
    return render(request, 'cetus3pur/index.html', )



def ThirdPartiesView(request):
    latest_3rdparty_list = ThirdParty.objects.order_by('legal_entity_name')
    context = {'latest_3p_list': latest_3rdparty_list}
    return render(request, 'cetus3pur/ThirdPartiesView.html', context)




# users for a 3rd party
def ThirdPartyUsersTableView(request, thirdparty_id):
    user_employer = ThirdParty.objects.get(pk = thirdparty_id)

    userlist = []
    for user in ThirdPartyUser.objects.filter(employer = user_employer).values():
        user.pop('employer_id')
        userlist.append(user)

    context = {'userlist': userlist, 'useremp' : user_employer, 'thirdparty_id' : thirdparty_id }
    return render(request, 'cetus3pur/ThirdPartyUsersTableView.html', context)




# the edit page for one user
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

        return render(request, 'cetus3pur/userviewedit.html', {'user': user, 'bulma_date': bulma_friendly_date}  )

    else:
        user = ThirdPartyUser.objects.get(pk = user_id)
        
        # bulma datefields seem to need this exact format
        bulma_friendly_date = user.userac_expirydate.strftime("%Y-%m-%d") 

        return render(request, 'cetus3pur/userviewedit.html', {'user': user, 'bulma_date': bulma_friendly_date} )




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
            if(len(list_tokens) != 5):
                error_text += "line " + str(line_num) + " has wrong number of tokens --> " + line + "\r\n"
                continue


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
            error_text += "line " + str(line_num) + " OK\n"
            
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

