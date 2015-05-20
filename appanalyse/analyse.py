import subprocess,time
import re


def InstallApk(apk):
	command="adb install "+apk
	p=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
	res=p.stdout.read().decode('utf8')
	if "success" not in res:
		return False
	return True

def RestartAdb():

	p=subprocess.Popen("adb kill-server | adb start-server",stdout=subprocess.PIPE,shell=True)
	res=p.stdout.read().decode('utf8')	
	pass

def InitPort():
	command="adb forward tcp:31415 tcp:31415"
	subprocess.call(command,shell=True)


def getPacageName(apk):
	command="aapt dump badging "+apk+" | grep package:\ name"
	p=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
	res=p.stdout.read().decode('utf8')
	if "ERROR" in res:
		return False
	name=re.findall("name='(\S+)'",res)
	if len(name)==0:
		return False
	else:
		return name[0]

	
def Init(apk,workdir):
	InstallApk(apk)
	packname=getPacageName(apk)
	InitPort()
	print packname
	
	getInfo(packname,workdir)
	getActivity(packname,workdir)
	getBroadcast(packname,workdir)
	getProvider(packname,workdir)
	getService(packname,workdir)
	



def getInfo(name,workdir):

	command="drozer console connect -c 'run app.package.info -a "+name+"' > info.txt"
	p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=workdir)

	out,error=p.communicate()
	print out
	if p.returncode==0:
		print "success"
		return True
	else:
		print error
		return False




def getActivity(name,workdir):

	command="drozer console connect -c 'run app.activity.info -a "+name+"' > activity.txt"
	p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=workdir)

	out,error=p.communicate()
	if p.returncode==0:
		print "success"
		return True
	else:
		print error
		return False



def getService(name,workdir):

	command="drozer console connect -c 'run app.service.info -a "+name+"' > service.txt"
	p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=workdir)
	out,error=p.communicate()
	if p.returncode==0:
		print "success"
		return True
	else:
		print error
		return False	

def getBroadcast(name,workdir):

	command="drozer console connect -c 'run app.broadcast.info -a "+name+"' > receiver.txt"
	p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=workdir)
	out,error=p.communicate()
	if p.returncode==0:
		print "success"
		return True
	else:
		print error
		return False



def getProvider(name,workdir):

	command="drozer console connect -c 'run app.provider.info -a "+name+"' > provider.txt"
	p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=workdir)
	out,error=p.communicate()
	if p.returncode==0:
		print "success"
		return True
	else:
		print error
		return False


