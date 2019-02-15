#!/usr/bin/python
import xmlrpclib,  copy
from myping import getinactivesystems
#username = 'bjin'
#passwd = 'suse1234'
MANAGER_URL = "http://bjsuma.bo2go.home/rpc/api"
MANAGER_LOGIN = "bjin"
MANAGER_PASSWORD = "suse1234"
client = xmlrpclib.Server(MANAGER_URL, verbose=0)
key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

all_list = client.system.listSystems(key)
new_list = copy.deepcopy(all_list)
#print('the entire list is:' , new_list)
print('The original list has %d entries.' %(len(all_list)))

get_inactive_systems = getinactivesystems.getInactiveSystems()
get_inactive_systems.getinactives()

mynum = 0
z = 0
for i in new_list:
    serverid = all_list[mynum]['id']
    for x in get_inactive_systems.systemlist:
        if str(serverid) == str(x):
            y = 1
            try:
                print('\033[2;31;40mwill be deleted as the system is inactive:\n %s'% (all_list[mynum]))
                del all_list[mynum]
                mynum -= 1
            except KeyError:
                print("Key 'testing' not found")
        else:
            y = 0
    mynum += 1
       
print('\033[1;32;40mThe new all_list looks now:\n %s' %((all_list)))
print('\033[1;32;40mThe new list has %d entries.' %(len(all_list)))
