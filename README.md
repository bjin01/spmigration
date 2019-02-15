# spmigration
### This scripts runs service pack migration for given base channel. 

Which scenarios are covered by the scripts:
* enter your base channel label, target base channel label, the current sp version and target sp version. See spmigration.py -h
*Then the script will use SUSE Manager API to get a list of all systems matching the base channel and query api to check if the systems have been marked as "inactive". Inactive systems will be pulled out from the systems list.
*Then the script will take the matching list of systems and issue salt hostname test.ping to check if the system is only.
*If salt test.ping is successful then a service pack migration **job** in SUSE Manager with the given target sp version will be created, for each single node.
*A job ID will be returned.

**Sample command:**

*python spmigration.py -s bjsuma.bo2go.home -u bjin -p suse1234 -base dev-sles12-sp3-pool-x86_64 -newbase dev-sles12-sp4-pool-x86_64 -fromsp sp3 -tosp sp4*

If __-x__ is not specified the SP Migration is always a **dryRun**.
Check Job status of the system if dryrun was successful before run the above command with -x specified.
