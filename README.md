# spmigration
### This scripts runs service pack migration for given base channel. 

**Sample command:**

*python spmigration.py -s bjsuma.bo2go.home -u bjin -p suse1234 -base dev-sles12-sp3-pool-x86_64 -newbase dev-sles12-sp4-pool-x86_64 -fromsp sp3 -tosp sp4*

If __-x__ is not specified the SP Migration is always a dryRun.
Check Job status of the system if dryrun was successful before run the above command with -x specified.
