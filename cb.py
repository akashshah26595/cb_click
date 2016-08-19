import click
import urllib2
import urllib
from urlparse import urlparse
import json
import subprocess

class Config(object):
	def __init__(self):
		pass

pass_config = click.make_pass_decorator(Config,ensure=True)

@click.group()
#@click.option('cinder_id',default='77b26fc7-066e-3057-b131-e77b4f6835cc')

@pass_config

def display(config,cinder_id):
	key_file = open('cbkey.txt','r')
	url_file = open('cburl.txt','r')
	res_file = open('cbres.txt','r')
	key = key_file.read()
	key = key.strip()
	url = url_file.read()
	url = url.strip()
	res = res_file.read()

	config.cinder_id = cinder_id
	config.key=key;
	config.url=url;
	config.res=res;
	checkLibvirtVersion()
	
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
			


@display.command()
@pass_config	
def createsnapshot(config):
	"""This method creates a snapshot for provided cinder id"""
	
	name = raw_input('Enter a snapshot name:\n')
	config.name = name

	urlData = config.url + "apiKey=" + config.key + "&command=createStorageSnapshot"  + "&id=" + config.cinder_id  + "&name=" + config.name +"&response=" + config.res 
	click.echo(urlData)
	webUrl = urllib2.urlopen(urlData)
	click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		click.echo((data))
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))

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

	urlData = config.url + "apiKey=" + config.key + "&command=listStorageSnapshots"  + "&id=" + config.cinder_id  +"&response=" + config.res 
	webUrl = urllib2.urlopen(urlData)
	click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		click.echo((data))
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))	


@display.command()
@pass_config
def deletesnapshot(config):
	"""Delete a particular snapshot"""

	name = raw_input('Enter snapshot name to delete:\n')
	config.name = name
	print 'Snapshot to be deleted:' , config.name
	data = listSnapshots(config)
	path = parseJSON(config,data)
	if path is None:
		return 'No such snapshot'
	urlData = config.url + "apiKey=" + config.key + "&command=deleteSnapshot" + "&id=" + config.cinder_id + "&path="  + path  + "&response=" + config.res 
	webUrl = urllib2.urlopen(urlData)
	click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		click.echo('Delete successful')
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))


@display.command()
@pass_config
def rollbacktosnapshot(config):
	"""Rollback a particular snapshot"""

	name = raw_input('Enter a snapshot name to rollback:\n')
	config.name = name
	data = listSnapshots(config)
	path = parseJSON(config,data)
	if path is None:
		return 'No such snapshot'
	
	urlData = config.url + "apiKey=" + config.key + "&command=rollbackToSnapshot"  + "&id=" + config.cinder_id + "&path="  + path  + "&response=" + config.res 
	webUrl = urllib2.urlopen(urlData)
	click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		click.echo((data))
		click.echo('Rollback successful')
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))		
	
def listSnapshots(config):
	urlData = config.url + "apiKey=" + config.key + "&command=" + "listStorageSnapshots" + "&id=" + config.cinder_id  +"&response=" + config.res 
	webUrl = urllib2.urlopen(urlData)
	click.echo(webUrl.getcode())
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		return data
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))


def checkLibvirtVersion():
	p = subprocess.Popen("./libvirt_version.sh",stdout=subprocess.PIPE,shell=True)
	(out,err) = p.communicate()
	p_status = p.wait()
	op = out.split()
	if op!="1.2.11":
		click.echo('Incorrect libvirt version detected. Please update it to v1.2.11');
	