#!/usr/bin/python2
import xmlrpclib,  argparse,  getpass,  textwrap
from mymodules import saltping
from datetime  import datetime
from mymodules import checkActiveSystems
from mymodules import newoptchannels
from mymodules import checkGroup
from mymodules import checkChannels
from mymodules import myLogger
from mymodules import jsonIO
import sys

class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(prog='PROG', formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
This script runs service pack migrations for selected systems.

Sample command:

    python spmigration.py -s <SUMA-server> -u <username> -p <password> -g <system-group-name> -base asp-2018-q3-sles12-sp3-pool-x86_64 -newbase asp-2019-m03-sles12-sp4-pool-x86_64  \n \

If -x is not specified the SP Migration is always a dryRun.
Please check the results of a dryrun before running this script with -x specified. ''')) 
parser.add_argument("-v", "--verbosity", action="count", default=0)
parser.add_argument("-x", "--execute_migration", action="store_true")
parser.add_argument("-s", "--server", help="Enter your suse manager host address e.g. myserver.abd.domain",  default='localhost',  required=True)
parser.add_argument("-u", "--username", help="Enter your suse manager loginid e.g. admin ", default='admin',  required=True)
parser.add_argument('-p', action=Password, nargs='?', dest='password', help='Enter your password',  required=True)
parser.add_argument('-g', "--group", help='Enter the name of the system group holding the systems to migrate ', required=True)
parser.add_argument("-base", "--current_base_channel", help="Enter the current base channel label. e.g. sles12-sp3-pool-x86_64 ",  required=True)
parser.add_argument("-newbase", "--new_base_channel", help="Enter the new base channel label. e.g. sles12-sp4-pool-x86_64 ",  required=True)
args = parser.parse_args()

MANAGER_URL = "http://"+ args.server+"/rpc/api"
MANAGER_LOGIN = args.username
MANAGER_PASSWORD = args.password
client = xmlrpclib.Server(MANAGER_URL, verbose=0)
key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)
today = datetime.today()
earliest_occurrence = xmlrpclib.DateTime(today)
jsonFile = "/tmp/jobs.json"
migrationSystems = {}
confirm = False

logger = myLogger.setup_custom_logger(__package__, args.verbosity)
logger.debug("Setting logging verbosity set to: {0}".format(args.verbosity))

if args.execute_migration:
    dryRun = 0
else:
    dryRun = 1

# Check the Service Pack and Channel args
bChannel = args.current_base_channel
nChannel = args.new_base_channel

logger.debug("Arg: Current base channel: {0}".format(bChannel))
logger.debug("Arg: New base channel: {0}".format(nChannel))

# Check the user supplied base channels exist and are valid base channels
vChannels = checkChannels.verifyChannels(client, key)
base_channel = vChannels.Channels(client,key,bChannel)
if base_channel is None:
  logger.critical('Base Channel "{0}" does not exist - exiting '.format(bChannel))
  client.auth.logout(key)
  sys.exit()
new_base_channel = vChannels.Channels(client,key,nChannel)
if new_base_channel is None:
  logger.critical('New Base Channel "{0}" does not exist - exiting '.format(nChannel))
  client.auth.logout(key)
  sys.exit()
logger.debug("Base Channel: %s New Base Channel: %s" %(base_channel, new_base_channel))

# Check which systems were chosen
group = args.group
logger.debug('Arg: System group: %s' %(group))
vGroup = checkGroup.verifyGroup(client, key)
if (vGroup.groupNotEmpty(group)):
   activeSystemIDs=vGroup.getActiveSystemIDs(group)
else:
   logger.error('System group "%s" does not exist - exiting' %(group))
   client.auth.logout(key)
   sys.exit()

logger.debug('Checking for SP migration candidates ...')
for ID in activeSystemIDs:
   gN = client.system.getName(key, ID)
   name = gN.get('name')
   logger.debug('Checking system %s (%d) ...' %(name, ID))
   print('Checking system %s (%d) ...' %(name, ID))

# Check the system has a base channel assigned
   curBaseChannel = client.system.getSubscribedBaseChannel(key, ID)
   if not curBaseChannel:
      logger.error('Skipping system \033[1;31;40m%s (%d)\033[1;31;0m - Reason: it has no base channel' %(name, ID))
      continue

# Check the current base channel is not the target base channel
   if curBaseChannel['label'] == new_base_channel:
      logger.error('Skipping system \033[1;31;40m%s (%d)\033[1;31;0m - Reason: it already has "%s" as Base Channel' %(name, ID, new_base_channel))
      continue

# Check the current base channel matches the base channel argument
   if not curBaseChannel['label'] == base_channel:
      logger.error('Skipping system \033[1;31;40m%s (%d)\033[1;31;0m - Reason: it does not have "%s" as Base Channel' %(name, ID, base_channel))
      logger.error('Current base channel for %s (%d) is %s' %(name, ID, curBaseChannel['label']))
      continue

# Check the system has subscribable base channels
   possibleBasech = client.system.listSubscribableBaseChannels(key, ID)
   logger.debug('Subscribable Base Channels for %s (%d) are: %s' %(name, ID, possibleBasech))
   if len(possibleBasech) == 0:
      print('Skipping system: \033[1;31;40m%s (%d)\033[1;31;0m - Reason: It has no subscribable Base Channels' %(name, ID))
      continue

# Check there are no packages which need updating
   upgradeablePkgs=client.system.listLatestUpgradablePackages(key, ID)
   if upgradeablePkgs:
      logger.error('Skipping system \033[1;31;40m%s (%d)\033[1;31;0m - Reason: it has %d installable packages' %(name, ID, len(upgradeablePkgs)))
      continue

# Check the system can be pinged via salt
   logger.debug('Sending salt.ping cmd to system %s (%d) ...' %(name, ID))
   p1 = saltping.mysalt(name)
   if p1:
      p1.ping()
   if p1.code == 0:
      logger.debug('salt.ping cmd to system %s (%d) was successful' %(name, ID))
      logger.debug('System %s (%d) is a candidate for SP migration' %(name, ID))
      migrationSystems[ID] = {'name': name}
   else:
      logger.error('Skipping system \033[1;31;40m%s (%d)\033[1;31;0m - Reason: salt ping failed' %(name, ID))
      continue

# Start the migrations
if len(migrationSystems) == 0:
   print('\nNo systems are candidates for SP migration - exiting')
   print('\nFor more details re-run the command and add -v or -vv and check the debugging information')
   client.auth.logout(key)
   sys.exit()

print('\nThe following system(s) can be migrated:' )
for s_id, s_info in migrationSystems.items():
    print ('\t\t\033[1;32;40m %s (%d)\033[1;32;0m' %(s_info['name'], s_id))

while True:
   answer = str(raw_input("\nDo you want to continue? [Y/n]:"))
   if answer.startswith("Y"):
      confirm = True
      break
   elif answer.startswith("n"):
      logger.info('Exiting')
      print("Exiting")
      break

optionalChannels=[]
if confirm:
   print("")
   for s_id, s_info in migrationSystems.items():
      sys = s_id
      name = s_info['name']
      logger.debug('\nlets see: %s  (%d) new_base_channel: %s childchannels: %s, dryRun: %s' %(name, sys, new_base_channel, optionalChannels, dryRun))
      try:
         spjob = client.system.scheduleSPMigration(key, sys,  new_base_channel,  optionalChannels,  dryRun,  earliest_occurrence)
      except:
         print('something went wrong with system while scheduling job with client.system.scheduleSPMigration %s %s'%(name, spjob))
      print('\t\tA job has been scheduled for system \033[1;32;40m%s (%d)\033[1;32;0m with job_id: %d' %(name, sys, spjob))
      migrationSystems[sys]['jobid'] = spjob
      print('\nCheck the scheduled jobs in the SUMA web UI -> Systems -> System Groups -> spmigration_temp')

   print('Or check %s for the list of systems and their scheduled job_ids.\n' %(jsonFile))
   jsonIO.writeJson(migrationSystems, jsonFile)

client.auth.logout(key)

