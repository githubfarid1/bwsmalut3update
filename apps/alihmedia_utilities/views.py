from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from subprocess import Popen, check_call
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@user_passes_test(lambda user: Group.objects.get(name='arsip') in user.groups.all())
@csrf_exempt
def inactive(request):
    comlist = [settings.PYTHON_UTILITY]
    if request.method == 'POST':
        function = request.POST.get("process")
        if function == "gencover":
            comlist.append(settings.GENCOVER_SCRIPT)
            comlist.append("-r")
            isreplace = request.POST.get("isreplace")
            if isreplace == "yes":
                comlist.append("yes")
            else:
                comlist.append("no")
        if function == "movepdf":
            comlist.append(settings.MOVEPDF_SCRIPT)
        
        Popen(comlist, shell=False)
        messages.info(request, "Proses dijalankan dibackground..")
    return render(request, 'alihmedia_utilities/inactive.html')
