from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.views.decorators.csrf import csrf_exempt
from .models import ThirdPartyUser
from .models import ThirdParty
from .models import RRResponsibleManager
import datetime


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

    context = {'userlist': userlist, 'useremp' : user_employer }
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
        test_string = "Billy Alby, BE5001, bill999, 10/01/2021\nBilly Bender, BE5002, bill901, 20/1/2022"
        test_date = "10/1/2021"
        #django.core.exceptions.ValidationError: ['“20/3/2023” value has an invalid date format. It must be in YYYY-MM-DD format.']
        date_time_obj = datetime.datetime.strptime(test_date, '%b %d %Y %I:%M%p')

        tpu = ThirdPartyUser(firstname="Billy", familyname="Testme", employee_id="BE5005", userac_name="bill9009", userac_expirydate="20/3/2023" )
        tpu.save()
        tpu = ThirdPartyUser(firstname="Billy", familyname="Testme2", employee_id="BE5006", userac_name="bill9010", userac_expirydate="20/3/2024" )
        tpu.save()
        return render(request, 'cetus3pur/ThirdPartyUsersTableView.html', {'thirdparty_id': thirdparty_id} )
    else:
        return render(request, 'cetus3pur/AddNewUsers.html', {'thirdparty_id': thirdparty_id} )




# RR  managers
def RRRManagersView(request):
    rrm = RRResponsibleManager.objects.values()
    context = {'rrm': rrm }
    return render(request, 'cetus3pur/rrrmanager.html', context)

