# spmigration v0.2
### This is a commandline script for service pack migration in SUSE Manager v3.x. ###
### Based and forked from bjin01/spmigration ###


## Motivation:
__SUSE Manager is the best Patch and Configuration Management Tool for Linux Systems, mainly for SLES but also supports RHEL, CentOS, Ubuntu, OpenSUSE, Containers and more will come. The reason for me to write something for Service Pack Migration is due to the fact that Service Pack Migration for SLES systems can only be done by mouse clicks in the web UI or using spacecmd command which is quite longly if you have a maintenance window and need to run SP Migration for hundreds of SLES systems.__

_This program should give you some ideas how a such task could be automated by using SUSE Manager API._

**I would appreciate any help, bug fixing, code optimization and testing feedbacks to me.**

## Prerequisites:

**- The channel label need to consist "-sp1" "-sp2" "-sp3" "-sp4" or "-ga" etc.**

**- The script has been tested with Python 2.7.13 with SUSE Manager 3.2.6**


## Function Highlights:

* __Parameters:__ - enter your base channel label, target base channel label and group-name . See spmigration.py -h
python spmigration.py -s <SUMA-server> -u <username> -p <password> -g patch-group1 -base asp-2018-q3-sles12-sp3-pool-x86_64 -newbase asp-2019-m03-sles12-sp4-poo
l-x86_64  \n \

* __Checking system availability prior Migration start__ - Then the script will use SUSE Manager API to get a list of all systems in the named system group and then go through various checks:
* Check the base channel matches the base channel parameter
* Check the target base channel exists
* Query api to check if the systems have been marked as "inactive". Inactive systems will be pulled out from the systems list.
* __Check remaining upgradable packages__ - at the moment the script verifies each system if it has any upgradable rpm packages. If it is the case this system will be disqualified from service pack migration and dropped out from the list.
* __Checking salt minion online status__ - Then the script will take the matching list of systems and issue salt hostname test.ping to check if the system is online.
* __Avoid job creation for offline systems__ - If salt test.ping is successful then a service pack migration **job** in SUSE Manager with the given target sp version will be created, for each single node.
* For systems that are qualified for service pack migration 
* __Schedule Jobs in SUSE Manager__ - A job ID will be returned.


## Download and try it! ##

*__note:__ in order to run the python script you will need the modules in the subdirectory mymodules - do not rename this subdirectory.*


## Sample command: ##

```suma:~/myscripts # python spmigration.py -s mysuma -u myuser -p suse1234 -base dev-sles12-sp3-pool-x86_64 -newbase dev-sles12-sp4-pool-x86_64 -g patch-group```

If __`-x`__ is not specified the SP Migration is always a **dryRun**.
Check Job status of the system if dryrun was successful before run the above command with -x specified.

### See here for additional command arguments: ###

  ```
  -h, --help            show this help message and exit
  
  -x, --execute_migration __THIS parameter is the real _fire_ button__ :shipit:
  
  
  -s SERVER, --server SERVER
  
 Enter your suse manager host address e.g. myserver.abd.domain
                        
                        
  -u USERNAME, --username USERNAME
  
 Enter your suse manager loginid e.g. admin
                        
                        
  -p [PASSWORD]         Enter your password
  
  
  -base CURRENT_BASE_CHANNEL, --current_base_channel CURRENT_BASE_CHANNEL
  
  Enter the current base channel label. e.g. sles12-sp3-pool-x86_64
                        
                        
  -newbase NEW_BASE_CHANNEL, --new_base_channel NEW_BASE_CHANNEL
  
  Enter the new base channel label. e.g. sles12-sp4-pool-x86_64
                        
 ```
 ## Enhancements for future version
 * add more detailed handling of child channels
