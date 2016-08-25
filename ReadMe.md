#CloudByte Click CLI

##Prerequisites:
* Python 2.7
* python-pip for python 2


##How to Install this CLI on Linux OR on Windows?
* Clone or Download the files from https://github.com/akashshah26595/cb_click

* Extract the files 

* Change the directory in terminal to cb_click-master/
   ```
	$ cd cb_click-master/
   ```

* Execute this command in the terminal(or Command Prompt). This will install CLI.
   ```
	$ pip install --editable .
    ```

##Note:
	
	CINDER_ID is the cinder volume id, with hyphens(-). 
	Example: 77b26fc7-066e-3057-b131-e77b4f6835cc

##How to use this CLI

* ####To display help page, syntax or available commands.
 
 ```
  $ cb 
  $ cb --help

  Usage: cb [OPTIONS] COMMAND [ARGS]...

Options:
  --cinder_id TEXT  Cinder Volume ID
  --name TEXT       Snapshot name
  --help            Show this message and exit.

Commands:
  cinder_list         Displays cinder id's of volumes on Cloudbyte...
  cinder_status       This method displays status of cinder...
  createsnapshot      Creates a snapshot for given cinder id
  deletesnapshot      Delete a snapshot
  glance_check        This method checks whether the bootable...
  rollbacktosnapshot  Rollback to a snapshot
  viewsnapshots       Displays all the snapshots for given cinder...

 ```  
* ####View all the snapshots of this volume.
 
 ```
  $ cb --cinder_id bee98fc2-7298-4d35-8ff0-5a8f3651f9fd viewsnapshots 
 
  { "listDatasetSnapshotsResponse" : { "count":2 ,"snapshot" : [  {
  "name": "T2",
  "path": "POOL2/OPENSTACK_ACCOPENSTACK_VSM/bee98fc272984d358ff05a8f3651f9fd@T2",
  "availMem": "-",
  "usedMem": "4.73M",
  "refer": "8.05G",
  "mountpoint": "-",
  "timestamp": "Thu Aug 25 2016 10:55",
  "clones": 0,
  "poolTakeOver": "noTakeOver",
  "managedstate": "Available",
  "type": "instant"
  }, {
  "name": "T5",
  "path": "POOL2/OPENSTACK_ACCOPENSTACK_VSM/bee98fc272984d358ff05a8f3651f9fd@T5",
  "availMem": "-",
  "usedMem": "308K",
  "refer": "8.05G",
  "mountpoint": "-",
  "timestamp": "Thu Aug 25 2016 17:05",
  "clones": 0,
  "poolTakeOver": "noTakeOver",
  "managedstate": "Available",
  "type": "instant"
  } ] } }

 ```  

* ####Create a new snapshot.
 
 ```
  $ cb --cinder_id bee98fc2-7298-4d35-8ff0-5a8f3651f9fd --name Snap1 createsnapshot 
 
  Froze 1 filesystem(s)

  { "createStorageSnapshotResponse" :  { "StorageSnapshot" : {
  "id": "27f3ef0d-9637-3cba-95c7-1fdac9588424",
  "name": "Snap1",
  "usn": "27f3ef0d96373cba95c71fdac9588424",
  "lunusn": "3b7834aadd3730799404c8886dc747af",
  "lunid": "3b7834aa-dd37-3079-9404-c8886dc747af",
  "scsiEnabled": false
  } }  }

  Thawed 1 filesystem(s)

 ```  

* ####Delete a particular snapshot.
 
 ```
  $ cb --cinder_id bee98fc2-7298-4d35-8ff0-5a8f3651f9fd --name Snap1 deletesnapshot
	  
  { "deleteSnapshotResponse" :  { "DeleteSnapshot" : {
  "status": "success"
  } }  }
  Delete Successful

 ```  

* ####Rollback to a particular snapshot.
 
 ```
  $ cb --cinder_id bee98fc2-7298-4d35-8ff0-5a8f3651f9fd --name Snap1 rollbacktosnapshot 
	  
  Froze 1 filesystem(s)

  { "rollbacktoshotresponse" :  { "Rollback" : {} }  }
  Rollback successful

  Thawed 1 filesystem(s)
    
 ```  

* ####Check whether glance image is stored on CloudByte Storage.
 
 ```
  $ cb --cinder_id bee98fc2-7298-4d35-8ff0-5a8f3651f9fd glance_check
  Glance image is hosted on Cloudbyte

 ```  

* ####View Cinder Service Status.
 
 ```
	  $ cb cinder_status

	----+------------------+-------------------+------+---------+-------+----------------------------+-----------------+
	|      Binary      |        Host       | Zone |  Status | State |         Updated_at         | Disabled Reason |
	+------------------+-------------------+------+---------+-------+----------------------------+-----------------+
	| cinder-scheduler |       cbnew       | nova | enabled |   up  | 2016-08-25T12:18:40.000000 |        -        |
	|  cinder-volume   |  cbnew@cloudbyte  | nova | enabled |   up  | 2016-08-25T12:18:43.000000 |        -        |
	|  cinder-volume   | cbnew@lvmdriver-1 | nova | enabled |  down | 2016-07-27T11:05:07.000000 |        -        |
	+------------------+-------------------+------+---------+-------+----------------------------+-----------------+
  

 ```  

* ####Find all the Cinder Volume ID's of Cloudbyte Storage.
 
 ``` 
  $ cb cinder_list 
  7569df37-30cc-4316-8e21-4cff774ccee5
  bee98fc2-7298-4d35-8ff0-5a8f3651f9fd
 ```  
