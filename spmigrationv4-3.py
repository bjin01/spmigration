#!/usr/bin/python
import argparse,  getpass,  textwrap
from xmlrpc.client import ServerProxy, DateTime
from mymodules import saltping
from datetime import datetime
from mymodules import checkactivesystems
from mymodules import newoptchannels
from mymodules import createGroup
from mymodules import checkChannels

class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)

parser = argparse.ArgumentParser()
#parser.add_argument("-v", "--verbosity", action="count", default=0)
parser = argparse.ArgumentParser(prog='PROG', formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
This scripts runs service pack migration for given base channel. 

Sample command:

              python spmigration.py -s bjsuma.bo2go.home -u bjin -p suse1234 -t traditional 
              -base dev-sles12-sp3-pool-x86_64 -newbase dev-sles12-sp4-pool-x86_64 -fromsp sp3 -tosp sp4 \n \

If -x is not specified the SP Migration is always a dryRun.
Check Job status of the system if dryrun was successful before run the above command with -x specified. ''')) 
parser.add_argument("-x", "--execute_migration", action="store_true")
parser.add_argument("-s", "--server", help="Enter your suse manager host address e.g. myserver.abd.domain",  default='localhost',  required=True)
parser.add_argument("-u", "--username", help="Enter your suse manager loginid e.g. admin ", default='admin',  required=True)
parser.add_argument('-p', action=Password, nargs='?', dest='password', help='Enter your password',  required=True)
parser.add_argument("-t", "--system_type", help="Enter type of your target systems, either traditional or salt, default is salt", default='salt', required=True)
parser.add_argument("-base", "--current_base_channel", help="Enter the current base channel label. e.g. sles12-sp3-pool-x86_64 ",  required=True)
parser.add_argument("-newbase", "--new_base_channel", help="Enter the new base channel label. e.g. sles12-sp4-pool-x86_64 ",  required=True)
parser.add_argument("-fromsp", "--migrate_from_servicepack", help="Enter the current service pack version e.g. sp3\n of course you can jump from sp3 to sp5 as well.",  required=True)
parser.add_argument("-tosp", "--migrate_to_servicepack", help="Enter the target service pack version e.g. sp4\n of course you can jump from sp3 to sp5 as well.",  required=True)
args = parser.parse_args()

MANAGER_URL = "http://"+ args.server+"/rpc/api"
MANAGER_LOGIN = args.username
MANAGER_PASSWORD = args.password


SUMA = "http://" + MANAGER_LOGIN + ":" + MANAGER_PASSWORD + "@" + MANAGER_URL + "/rpc/api"
with ServerProxy(SUMA) as client:
    key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

today = datetime.today()
earliest_occurrence = DateTime(today)

if args.execute_migration:
    dryRun = 0
else:
    dryRun = 1

L = []
migrationsystems = []
vChannels = checkChannels.verifyChannels()
bChannel = args.current_base_channel
nChannel = args.new_base_channel
base_channel = vChannels.Channels(client,key,bChannel)
new_base_channel = vChannels.Channels(client,key,nChannel)

previous_sp = args.migrate_from_servicepack
new_sp = args.migrate_to_servicepack

checksystems = checkactivesystems.checkInactives(client,  key,  args.username,  args.password)
activesystems = checksystems.getactive_systems()

mygroup = createGroup.myGroup(client, key)
mygroup.newGroup()

for server in activesystems:
    s = server.get('id')
    basech_name = client.system.listSubscribableBaseChannels(key, s)
    availpkgs = client.system.listLatestUpgradablePackages(key,  s)

    for a in basech_name:
       if a['current_base'] == 1:
            L.append(a['name'])
            getoptchannels = newoptchannels.getnew_optionalChannels(client, key, s)
            optionalChannels = getoptchannels.find_replace(previous_sp, new_sp)
            if a['label'] == base_channel and len(availpkgs) <=3 :
                print('%s has %d upgradable packages and is qualified for sp migration.' %( server['name'],  len(availpkgs)))

                if "salt" in args.system_type: 
                    print('\nChecking system through salt %s test.ping: \n' %(server['name']))                
                    p1 = saltping.mysalt(server['name'])
                    p1.ping()
                else:
                    p1.code == 0

                if p1.code == 0:
                    try:
                        #print('lets see key, s, new_base_channel childchannels, dryRun',  key, s, new_base_channel, optionalChannels, dryRun)
                        spjob = client.system.scheduleProductMigration(key, s,  new_base_channel,  optionalChannels,  dryRun,  earliest_occurrence)
                        print('A new job has been scheduled with id: %d' %(spjob))
                        migrationsystems.append(s)
                    except:
                        print('something went wrong with system while scheduling job with client.system.scheduleProductMigration %s'%(server['name']))
            elif a['label'] == base_channel:
                print('\033[1;31;40m%s The system need to be updated prior Product Migration. It still has upgradable pkgs: %d \033[1;32;40m'%(server['name'], len(availpkgs)))

if migrationsystems:
    mygroup.addSystemsToGroup(migrationsystems)
    print('Check systems and their scheduled jobs in web UI -> Systems -> System Groups -> ProductMigration_temp')
else:
    print('Obviously no system has been qualified for the service pack migration. This can have several reasons:\n\n')
    print('\tThe systems don\'t have the base_channel you entered.')
    print('\tThe systems are not online and or not reachable by salt test.ping')
    print('\tThe systems have more than 3 upgradable packages.')
    print('last but not least double check your target base channel and optional channels if they are available.')
client.auth.logout(key)
