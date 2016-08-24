import sys

import click
import urllib2
import urllib
from urlparse import urlparse
import json
import subprocess
import shlex

class Config(object):
	def __init__(self):
		pass

pass_config = click.make_pass_decorator(Config,ensure=True)

@click.group()
@click.option('--cinder_id',help='Cinder Volume ID')
@click.option('--name',help='Snapshot name')

@pass_config

def display(config,cinder_id="",name=""):
	key_file = open('cbkey.txt','r')
	url_file = open('cburl.txt','r')
	res_file = open('cbres.txt','r')
	key = key_file.read()
	key = key.strip()
	url = url_file.read()
	url = url.strip()
	res = res_file.read()
	config.name=name
	config.cinder_id = cinder_id
	config.key=key;
	config.url=url;
	config.res=res;
	libvirt_ver()
	qemu_check()
	#temp()
def parseJSON(config,data):
	json_data = json.loads(data)
	paths = []
	names = []
	snapshot1 = config.name
	snapshot1 = snapshot1.strip()
	for i in json_data["listDatasetSnapshotsResponse"]['snapshot']:
		x = str(i['name'])
		y = str(i['path'])
		names.append(x)
		paths.append(y)
	try:
		
		ix = names.index(snapshot1.strip())
 		path = paths[ix]
 		return path
	except:
		click.echo('Error!')

def mapCinderToID(config,data):
	json_data = json.loads(data)
	cinder = config.cinder_id
	cinder = cinder.replace("-","")
	id=""
	for i in json_data["listFilesystemResponse"]['filesystem']:
		x = str(i['name'])
		if x==cinder:
			id=str(i['id'])
			break
	if id=="":
		print "Cinder To ID Failed"
		return 0
	else:
		return id		
			


@display.command()
@pass_config	
def createsnapshot(config):
	"""This method creates a snapshot for provided cinder id"""
	
	if config.name is None or config.cinder_id is None:
	 	if config.name is None:
			print("\nPlease enter snapshot name.\n")
			#p = subprocess.call("cb --help",shell=True)
		if config.cinder_id is None:
			print("\nPlease enter Cinder ID\n")	
			#p = subprocess.call("cb --help",shell=True)
		p = subprocess.call("cb --help",shell=True) 	
		sys.exit(2)
	data = listFileSystem(config)
	config.id=mapCinderToID(config,data)
	if config.id==0:
		print "No UUID found for given cinder id"
		sys.exit(127)
	urlData = config.url + "apiKey=" + config.key + "&command=createStorageSnapshot"  + "&id=" + config.id  + "&name=" + config.name +"&response=" + config.res 
	click.echo(urlData)
	
	#Freezing the filesystem
	#p = subprocess.Popen("./qemu_check.sh | awk ' $2!=\"Name\" {print $2}'",stdout=subprocess.PIPE,shell=True)
	p = subprocess.Popen("./final.sh",stdout=subprocess.PIPE,shell=True)
	(out,err) = p.communicate()
	p_status = p.wait()
	op = out.split()
	instances = []
	for i in op:
            	x = i.strip('",')
            	instances.append(x)
	inst=instances[1]
	p=subprocess.call(shlex.split('./freeze.sh %s' %(inst)))
	
	##Ends
	webUrl = urllib2.urlopen(urlData)
	click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		click.echo(data)
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))
	
	#Thawing the filesystem
	p=subprocess.call(shlex.split('./thaw.sh %s' %inst))


@display.command()
#@pass_config	
def cinder_list():
	"""This method displays all the cinder id of volumes on Cloudbyte Server"""
	p = subprocess.Popen("./cinder_list.sh",stdout=subprocess.PIPE,shell=True)
	(out,err) = p.communicate()
	p_status = p.wait()
	op = out.split()
	for i in op:
            x = i.strip('')
            click.echo(x)



@display.command()
@pass_config
def viewsnapshots(config):
	"""This method displays all the snapshots for given cinder id"""
	
	
	if config.cinder_id is None:
	 	if config.cinder_id is None:
			print("\nPlease enter Cinder ID\n")	
			#p = subprocess.call("cb --help",shell=True)
		p = subprocess.call("cb --help",shell=True) 	
		sys.exit(2)

	data = listFileSystem(config)
	config.id=mapCinderToID(config,data)
	if config.id==0:
		print "No UUID found for given cinder id"
		sys.exit(127)

	urlData = config.url + "apiKey=" + config.key + "&command=listStorageSnapshots"  + "&id=" + config.id  +"&response=" + config.res 
	click.echo(urlData)
	webUrl = urllib2.urlopen(urlData)
	#click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		click.echo(data)
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))	


@display.command()
@pass_config
def deletesnapshot(config):
	"""Delete a particular snapshot"""
	
	if config.name is None or config.cinder_id is None:
	 	if config.name is None:
			print("\nPlease enter snapshot name.\n")
			#p = subprocess.call("cb --help",shell=True)
		if config.cinder_id is None:
			print("\nPlease enter Cinder ID\n")	
			#p = subprocess.call("cb --help",shell=True)
		p = subprocess.call("cb --help",shell=True) 	
		sys.exit(2)
	
 	data1 = listFileSystem(config)
	config.id=mapCinderToID(config,data1)
	if config.id==0:
		print "No UUID found for given cinder id"
		sys.exit(127)

	print 'Snapshot to be deleted:' , config.name
	data = listSnapshots(config)
	path = parseJSON(config,data)
	if path is None:
		return 'No such snapshot'
	urlData = config.url + "apiKey=" + config.key + "&command=deleteSnapshot" + "&id=" + config.id + "&path="  + path  + "&response=" + config.res 
	click.echo(urlData)
	webUrl = urllib2.urlopen(urlData)
	#click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		click.echo('Delete successful')
		click.echo(data)
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))


@display.command()
@pass_config
def rollbacktosnapshot(config):
	"""Rollback a particular snapshot"""
	
	if config.name is None or config.cinder_id is None:
	 	if config.name is None:
			print("\nPlease enter snapshot name.\n")
			#p = subprocess.call("cb --help",shell=True)
		if config.cinder_id is None:
			print("\nPlease enter Cinder ID\n")	
			#p = subprocess.call("cb --help",shell=True)
		p = subprocess.call("cb --help",shell=True) 	
		sys.exit(2)

	
 	data1 = listFileSystem(config)
	config.id=mapCinderToID(config,data1)
	if config.id==0:
		print "No UUID found for given cinder id"
		sys.exit(127)

	data = listSnapshots(config)
	path = parseJSON(config,data)
	if path is None:
		return 'No such snapshot'
	
	#Freezing the filesystem
	p = subprocess.Popen("./final.sh",stdout=subprocess.PIPE,shell=True)
	(out,err) = p.communicate()
	p_status = p.wait()
	op = out.split()
	instances = []
	for i in op:
            	x = i.strip('",')
            	instances.append(x)
	inst=instances[1]
	p=subprocess.call(shlex.split('./freeze.sh %s' %(inst)))
	
	##Ends
	urlData = config.url + "apiKey=" + config.key + "&command=rollbackToSnapshot"  + "&id=" + config.id + "&path="  + path  + "&response=" + config.res 
	click.echo(urlData)
	webUrl = urllib2.urlopen(urlData)
	#click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		click.echo((data))
		click.echo('Rollback successful')
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))		
	
	#Thawing the filesystem
	p=subprocess.call(shlex.split('./thaw.sh %s' %inst))

def listSnapshots(config):
	urlData = config.url + "apiKey=" + config.key + "&command=" + "listStorageSnapshots" + "&id=" + config.id  +"&response=" + config.res 
	webUrl = urllib2.urlopen(urlData)
	click.echo(webUrl)
	click.echo(webUrl.getcode())
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		return data
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))

def listFileSystem(config):
	urlData = config.url + "apiKey=" + config.key + "&command=" + "listFileSystem" +"&response=" + config.res 
	webUrl = urllib2.urlopen(urlData)
	#click.echo(webUrl)
	click.echo(webUrl.getcode())
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		return data
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))		

#@display.command()
def libvirt_ver():
	p = subprocess.Popen("./libvirt_version.sh",stdout=subprocess.PIPE,shell=True)
	(out,err) = p.communicate()
	p_status = p.wait()
	op = str(out).strip()
#	op = "1.2.12"
	click.echo('Libvirt Version: %s' %op)
	if op == "1.2.11":
		click.echo('Correct libvirt version');
	else:
		click.echo('Please update your libvirt version to 1.2.11')
	        sys.exit(2)

def qemu_check():
	try:
		p = subprocess.Popen("./qemu_check.sh",stdout=subprocess.PIPE,shell=True)
		(out,err) = p.communicate()
		p_statusNot  = p.wait()
		#out = out.strip()
		#print out
	#op = str(out).strip()
#	op = "1.2.12"
	#click.echo('Libvirt Version: %s' %op)
		click.echo('KVM QEMU Enabled on VM');
	except:
		
		click.echo('KVM QEMU Not Enabled on VM. Exiting..')
	        sys.exit(2)
# def temp():
# 	click.echo('Hello World!')

@display.command()
@pass_config
def cinder_status(config):
	"""This method displays status of cinder services"""	
	p = subprocess.Popen("./cinder_services.sh",stdout=subprocess.PIPE,shell=True)
	(out,err) = p.communicate()
	p_statusNot  = p.wait()
	op = str(out).strip()
	print op
	#click.echo('Libvirt Version: %s' %op)
	#k=0
	#for i in op:
#		if k==2:
#			print "\n"
#			k=0
#	    	print i,"\t",
#	    	k=k+1
#	print


@display.command()
@pass_config
def glance_check(config):
	
	"""This method checks whether the bootable cinder volume has glance image stored on CB Storage"""	
	#p = subprocess.Popen("./check glance.sh",stdout=subprocess.PIPE,shell=True)

	if config.cinder_id is None:
	 	if config.cinder_id is None:
			print("\nPlease enter Cinder ID\n")	
			#p = subprocess.call("cb --help",shell=True)
		p = subprocess.call("cb --help",shell=True) 	
		sys.exit(2)
	cinder = config.cinder_id
	p = subprocess.Popen(('./check_glance.sh %s' %(cinder)),stdout=subprocess.PIPE,shell=True)
	(out,err) = p.communicate()
	p_statusNot  = p.wait()
	op = str(out).strip()
	if op is None or op=="":
		click.echo("Volume not Bootable or Glance Image Not Hosted On Cloudbyte")
	else:
		print op
		click.echo("Glance image is hosted on Cloudbyte")
	#click.echo('Libvirt Version: %s' %op)
	#k=0
	#for i in op:
#		if k==2:
#			print "\n"
#			k=0
#	    	print i,"\t",
#	    	k=k+1
#	print

#p = subprocess.Popen(('./check_glance.sh %s' %(cinder)),stdout=subprocess.PIPE,shell=True)
#(out,err) = p.communicate()
#print "OP:",out
#p_statusNot  = p.wait()
#op = str(out).strip()
#print "Output:%s" %op
#if op is None:
#	print("Volume not Bootable or Glance Image Not Hosted On Cloudbyte")
#else:
#	print op
#        print("Glance image is hosted on Cloudbyte")

