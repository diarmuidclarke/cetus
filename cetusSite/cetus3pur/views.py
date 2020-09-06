from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import ThirdPartyUser
from .models import ThirdParty
from .models import RRResponsibleManager



def index(request):
    latest_3rdparty_list = ThirdParty.objects.order_by('legal_entity_name')
    context = {'latest_3p_list': latest_3rdparty_list}
    return render(request, 'cetus3pur/index.html', context)



def ThirdPartyUsersTableView(request, thirdparty_id):
    userlist = []
    user_employer = ThirdParty.objects.get(pk = thirdparty_id)

    for user in ThirdPartyUser.objects.filter(employer = user_employer).values():
        userlist.append(user)

    context = {'userlist': userlist}
    return render(request, 'cetus3pur/ThirdPartyUsersTableView.html', context)






#
# def index(request):
#    return HttpResponse("Hello, world. Cetus 3rd Party User Register")


def ThirdPartiesTableView(request, question_id):
    response = "3rd party table"
    return HttpResponse(response % question_id)


