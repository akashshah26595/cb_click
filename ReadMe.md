#CloudByte Click CLI

##Prerequisites:
* Python 2.7
* python-pip for python 2


##How to Install this CLI on Linux OR on Windows?
* Clone or Download the files from https://github.com/akashshah26595/cb_click

* Extract the files 

* Change the directory in terminal to click_test1
   ```
   $ cd click_test1
   ```

* Execute this command in the terminal(or Command Prompt)
   ```
    $ pip install --editable .
    ```

##Note:
	
	CINDER_ID is the cinder volume id, with hyphens(-). 
	Example: 77b26fc7-066e-3057-b131-e77b4f6835cc
	This is the **default** cinder_id.

##How to use this CLI
* To display help page, syntax or available commands.
 ```
  $ cb 
  $ cb --help
 ```  

* View all the snapshots of this volume
   ```
   $ cb 77b26fc7-066e-3057-b131-e77b4f6835cc viewsnapshots
   ```

* Create a new snapshot
   ```
      $ cb 77b26fc7-066e-3057-b131-e77b4f6835cc createsnapshot	   	 
   	 Enter snapshot name:
   	 snap2
   ```

* Delete a particular snapshot
   ```
   $ cb 77b26fc7-066e-3057-b131-e77b4f6835cc deletesnapshot
     Enter snapshot name to delete:
     snap1
   ```

* Rollback to a particular snapshot
   ```
   $ cb 77b26fc7-066e-3057-b131-e77b4f6835cc rollbacktosnapshot
     Enter a snapshot name to rollback:
     snap2
   ```


