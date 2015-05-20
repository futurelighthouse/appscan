from django.shortcuts import render,render_to_response,HttpResponse
import hashlib
import os
from django import forms
from django.conf import settings


# Create your views here.
from django import forms
from analyse import Init
theapkhash=""
theapkpath=""
theworkdir=""

class UploadFileForm(forms.Form):
    file = forms.FileField()



def upload(request):
    if request.method=="POST":
        # filename=request.POST.get("Filename")
        # some check
        
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            apkfile=request.FILES['file']
            apkfilename=apkfile.name
            save_file(apkfile,apkfilename)
            
        else:
            print "wuxiao"
    else:
        return HttpResponse("error")


def save_file(file, filename):

    if file:
        
        basedir=os.path.join(settings.BASE_DIR, 'apkfiles')
        path=os.path.join(basedir, filename)
        #calculate the md5 value of the apk
        filehash=hashlib.md5()
        fp=open(path, "wb")
        for data in file.chunks():
            fp.write(data)
            filehash.update(data)
        fp.close()
        apkhash=filehash.hexdigest()
        apkname=filename
        newpath=os.path.join(basedir, apkhash+".apk")
        os.rename(path,newpath)

        workdir=os.path.join(settings.BASE_DIR, 'results')+"/"+apkhash
        if not os.path.exists(workdir):
            print "aaaaaaaaaaa"
            os.mkdir(workdir)
        global theapkhash,theapkpath,theworkdir
        theapkhash=apkhash
        theapkpath=newpath
        theworkdir=workdir
        
        return True

    else:
        print "savefail"
        return False

def index(request):
	return render_to_response("index.html")


def show(request):

    Init(theapkpath,theworkdir)
    info,user_permission,define_permission = readInfo(theworkdir)
    activity_info=readActivity(theworkdir)
    BroadcastReceiver_info=readBroadcastReceiver(theworkdir)
    Service_info=readService(theworkdir)
    Provider_info=readContentProvider(theworkdir)
    return render_to_response("show.html",{"info":info,"user_permission":user_permission,"define_permission":define_permission,"activity_info":activity_info,"BroadcastReceiver_info":BroadcastReceiver_info,"Provider_info":Provider_info,"Service_info":Service_info})


def readInfo(theworkdir):
	info_list=[]
	info=[]
	user_permission=[]
	define_permission=[]

	f=open(theworkdir+"/info.txt",'r')
	f.readline()
	f.readline()
	line=f.readline()
	while line:
		line=line.strip("\n")
		if line=="":
			continue
		if ":" in line:
			data=line.strip("\n").split(":")
			info_list.append(data)		
		else:
			
			info_list[-1][1]+=line;			
			#info_list[key]+=line.strip("\n")
		line=f.readline()
		
	for item in info_list:
		if "Uses Permissions" in item[0]:
			user_permission=item
			#info_list.remove(item)
		if "Defines Permissions" in item[0]:
			define_permission=item
			#info_list.remove(item)
	info_list.remove(user_permission)
	info_list.remove(define_permission)
	info=info_list

	return info,user_permission[1].split("-"),define_permission[1].split("-")

def readActivity(theworkdir):
    activity_info=[]
    f=open(theworkdir+"/activity.txt",'r')
    f.readline()
    f.readline()
    line=f.readline()
    line=f.readline()
    while line:
        line=line.strip("\n")
        if "Permission" not in line:
            activity_info.append(line.strip())
        line=f.readline()
    return activity_info


def readBroadcastReceiver(theworkdir):
    BroadcastReceiver_info=[]
    f=open(theworkdir+"/receiver.txt",'r')
    f.readline()
    f.readline()
    line=f.readline()
    line=f.readline()
    while line:
        line=line.strip("\n")
        if "Permission" not in line:
            BroadcastReceiver_info.append(line.strip())
        line=f.readline()
    return BroadcastReceiver_info


def readService(theworkdir):
    Service_info=[]
    f=open(theworkdir+"/service.txt",'r')
    f.readline()
    f.readline()
    line=f.readline()
    line=f.readline()
    while line:
        line=line.strip("\n")
        if "Permission" not in line:
            Service_info.append(line.strip())
        line=f.readline()
    return Service_info


def readContentProvider(theworkdir):
    Provider_info=[]
    f=open(theworkdir+"/provider.txt",'r')
    line=f.readline()
    while line:
        if "Content Provider:" in line:
            Provider_info.append(line.split(":")[1])
        line=f.readline()
    return Provider_info



