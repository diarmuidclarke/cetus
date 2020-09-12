from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.views.decorators.csrf import csrf_exempt
from .models import ThirdPartyUser
from .models import ThirdParty
from .models import RRResponsibleManager


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
        name = request.POST.get('user_acname')
        
        user = ThirdPartyUser.objects.get(pk = user_id)
        user.userac_name = name
        user.save()


        context = {'user_id': user_id, 'user': user }
        return render(request, 'cetus3pur/userviewedit.html', { 'user': user} )
    else:
        user = ThirdPartyUser.objects.get(pk = user_id)
        context = {'user_id': user_id, 'user': user }
        return render(request, 'cetus3pur/userviewedit.html', {'user': user} )




# RR  managers
def RRRManagersView(request):
    rrm = RRResponsibleManager.objects.values()
    context = {'rrm': rrm }
    return render(request, 'cetus3pur/rrrmanager.html', context)

