CloudByte Click CLI

Prerequisites:
1) Python 2.7
2) python-pip for python 2


How to Install this CLI on Linux OR on Windows?
1) Clone or Download the files from https://github.com/akashshah26595/cb_click

2) Extract the files 

3) Change the directory in terminal to click_test1
   $ cd click_test1

4) Execute this command in the terminal(or Command Prompt)
   $ pip install --editable .

Note:
	
	CINDER_ID is the cinder volume id, with hyphens(-). 
	Example: 77b26fc7-066e-3057-b131-e77b4f6835cc
	This is the default cinder_id.

How to use this CLI
1) $ cb or cb --help
   Displays help page, syntax and commands.

2) View all the snapshots of this volume
   $ cb 77b26fc7-066e-3057-b131-e77b4f6835cc viewsnapshots

3) Create a new snapshot
   $ cb 77b26fc7-066e-3057-b131-e77b4f6835cc createsnapshot	   	 
   	 Enter snapshot name:
   	 snap2

4) Delete a particular snapshot
   $ cb 77b26fc7-066e-3057-b131-e77b4f6835cc deletesnapshot
   Enter snapshot name to delete:
   snap1

5) Rollback to a particular snapshot
   $ cb 77b26fc7-066e-3057-b131-e77b4f6835cc rollbacktosnapshot
   Enter a snapshot name to rollback:
   snap2



