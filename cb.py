import click
import urllib2
import urllib
from urlparse import urlparse
import json

class Config(object):
	def __init__(self):
		pass

pass_config = click.make_pass_decorator(Config,ensure=True)


@click.group()
@click.argument('cinder_id',default='77b26fc7-066e-3057-b131-e77b4f6835cc')
@click.argument('cb_command')


@pass_config

def display(config,cinder_id,cb_command):
	key_file = open('cbkey.txt','r')
	url_file = open('cburl.txt','r')
	res_file = open('cbres.txt','r')
	key = key_file.read()
	key = key.strip()
	url = url_file.read()
	url = url.strip()
	res = res_file.read()

	if(cb_command =='createStorageSnapshot'):
		name = raw_input('Enter snapshot name:\n')
		config.name = name
	elif(cb_command =='deleteSnapshot'):
		name = raw_input('Enter snapshot name to delete:\n')
		config.name = name
	elif(cb_command =='rollbackToSnapshot'):
		name = raw_input('Enter snapshot name to rollback:\n')
		config.name = name	
	else:
		name = ''
		config.name = name

	config.cinder_id = cinder_id
	config.cb_command = cb_command
	config.key=key;
	config.url=url;
	config.res=res;

@pass_config
def parseJSON(config,data):
	json_data = json.loads(data)
	paths = []
	names = []
	
	for i in json_data["listDatasetSnapshotsResponse"]['snapshot']:
		#print i['id']
		x = str(i['name'])
		y = str(i['path'])

		#x = x.upper()
		#y = y.upper()

		names.append(x)
		#print i['name']
		paths.append(y)
		#print i['path']
	click.echo(paths)
	click.echo('***************************************************')
	click.echo(names)	
	try:
		#snap_name = config.name.upper()
		#ix = names.index(snap_name)
		ix = names.index(config.name)
		click.echo('Index: ' ,ix)
		#user->SNAP1 system snap1
 		path = paths[ix]
 		click.echo('Path: %s' % path)
 		return path
	except:
		click.echo('No such snapshot')
			


@display.command()
@pass_config	
def createsnapshot(config):
	"""This method creates a snapshot for provided cinder id"""
	#https://20.10.43.1/client/api?command=createStorageSnapshot&
	#id=77b26fc7-066e-3057-b131-e77b4f6835cc&name=snap2&response=json
	urlData = config.url + "apiKey=" + config.key + "&command=" + config.cb_command + "&id=" + config.cinder_id  + "&name=" + config.name +"&response=" + config.res 
	click.echo(urlData)
	webUrl = urllib2.urlopen(urlData)
	click.echo(webUrl.getcode())
	click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		#print data
		click.echo((data))
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))

@display.command()
@pass_config
def viewsnapshots(config):
	"""This method displays all the snapshots for given cinder id"""
	#listStorageSnapshots
	urlData = config.url + "apiKey=" + config.key + "&command=" + config.cb_command + "&id=" + config.cinder_id  +"&response=" + config.res 
	#click.echo(urlData)
	webUrl = urllib2.urlopen(urlData)
	click.echo(webUrl.getcode())
	click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		#print data
		click.echo((data))
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))	


@display.command()
@pass_config
def deletesnapshot(config):
	"""Delete a particular snapshot"""

	data = listSnapshots(config)
	path = parseJSON(config,data)
	print('Path is :' ,path)
	if path is None:
		return 'No such snapshot'
	urlData = config.url + "apiKey=" + config.key + "&command=" + config.cb_command + "&id=" + config.cinder_id + "&path="  + path  + "&response=" + config.res 
	click.echo(urlData)
	webUrl = urllib2.urlopen(urlData)
	click.echo(webUrl.getcode())
	click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		#print data
		#click.echo((data))
		#parseJSON(config,data)
		click.echo('Delete successful')
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))


@display.command()
@pass_config
def rollbacktosnapshot(config):
	"""Rollback a particular snapshot"""

	data = listSnapshots(config)
	path = parseJSON(config,data)
	print('Path is :' ,path)
	
	urlData = config.url + "apiKey=" + config.key + "&command=" + config.cb_command + "&id=" + config.cinder_id + "&path="  + path  + "&response=" + config.res 
	click.echo(urlData)
	webUrl = urllib2.urlopen(urlData)
	click.echo(webUrl.getcode())
	click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		#print data
		click.echo((data))
		#parseJSON(config,data)
		click.echo('Rollback successful')
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))		
	
def listSnapshots(config):
	urlData = config.url + "apiKey=" + config.key + "&command=" + "listStorageSnapshots" + "&id=" + config.cinder_id  +"&response=" + config.res 
	#click.echo(urlData)
	webUrl = urllib2.urlopen(urlData)
	click.echo(webUrl.getcode())
	#click.echo(urlData)
	if(webUrl.getcode() == 200):
		data = webUrl.read()
		#print data
		#click.echo((data))
		#parseJSON(config,data)
		return data
	else:
		click.echo('Error while fetching data', str(webUrl.getcode()))