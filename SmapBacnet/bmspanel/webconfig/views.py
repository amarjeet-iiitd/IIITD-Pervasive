#Author Romil Bhardwaj 
#romil11092@iiitd.ac.in
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from SmapBacnetUtils import BacnetPoint, configread, configreadpoint, configaddpoint, configdeletepoint, configeditpoint, ReadProperty

import ConfigParser

from webconfig.models import BacnetPointModel
from webconfig.forms import PointForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

filepath='/home/pi/smap/iiitd_bms.conf'

def loginpage(request):
    if request.method == 'GET':
    	return render(request, 'webconfig/login.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/config')
        else:
            return HttpResponseRedirect('/config/login')
    else:
        return HttpResponseRedirect('/config/login')

def debug(request):
    if request.method == 'GET':
    	return render(request, 'webconfig/debug.html')
    obj_type = request.POST['obj_type']
    inst_id = request.POST['inst_id']
    prop_id = request.POST['prop_id']
    addr = request.POST['address']
    print addr
    ReadResult = ReadProperty(str(obj_type), str(inst_id), str(prop_id), str(addr))
    #ReadResult = addr + obj_type + inst_id
    context = {'ReadResult': ReadResult}
    return render(request, 'webconfig/debug.html', context)

def scanlist(request):
    return render(request, 'webconfig/static_pointslist.htm')

@login_required
def logoutpage(request):
    logout(request)

@login_required
def reboot(request):
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
    return render(request, 'webconfig/reboot.html')
    
@login_required
def index(request):
    PointsList=configread(filepath)
    context = {'PointsList': PointsList}
    return render(request, 'webconfig/index.html', context)

@login_required
def deletepoint(request, config_id):
    configdeletepoint(filepath, int(config_id))
    return HttpResponseRedirect('/config')

@login_required
def addpoint(request):
	if request.method == 'GET':
		form=PointForm()
		context = { 'form' : form }
		return render(request, 'webconfig/addpoint.html', context)
	elif request.method == 'POST':
		form=PointForm(request.POST)
		if form.is_valid():
			print (form.cleaned_data)
			bacpoint = BacnetPoint(form.cleaned_data['ip'], form.cleaned_data['obj_type'], str(form.cleaned_data['inst_id']), form.cleaned_data['prop_type'], form.cleaned_data['value_type'], form.cleaned_data['value_unit'], str(form.cleaned_data['rate']), form.cleaned_data['wing'], form.cleaned_data['point_parent'], form.cleaned_data['point_name'], str(form.cleaned_data['point_floor']), form.cleaned_data['point_building'], form.cleaned_data['point_source'])#Add any new Metadata to be added here
			configaddpoint(filepath, bacpoint)
		return HttpResponseRedirect('/config')

@login_required
def editpoint(request, config_id):
	point=configreadpoint(filepath, int(config_id))
	if request.method == 'GET':
		form=PointForm(point.__dict__)
		context = { 'form' : form, 'id' : config_id }
		return render(request, 'webconfig/edit.html', context)
	elif request.method == 'POST':
		form=PointForm(request.POST)
		if form.is_valid():
			print (form.cleaned_data)
			bacpoint = BacnetPoint(form.cleaned_data['ip'], form.cleaned_data['obj_type'], str(form.cleaned_data['inst_id']), form.cleaned_data['prop_type'], form.cleaned_data['value_type'], form.cleaned_data['value_unit'], str(form.cleaned_data['rate']), form.cleaned_data['wing'], form.cleaned_data['point_parent'], form.cleaned_data['point_name'], str(form.cleaned_data['point_floor']), form.cleaned_data['point_building'], form.cleaned_data['point_source'])#Add any new Metadata to be added here
			configeditpoint(filepath, int(config_id), bacpoint)
		return HttpResponseRedirect('/config')
