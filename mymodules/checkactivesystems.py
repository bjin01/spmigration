#!/usr/bin/python
import copy
from mymodules import getinactivesystems

class checkInactives:
    def __init__(self,  suma_client, suma_key,  username,  password):
        self.suma_client = suma_client
        self.suma_key = suma_key
        self.all_list = self.suma_client.system.listSystems(self.suma_key)
        self.new_list = copy.deepcopy(self.all_list)
       
        self.get_inactive_systems = getinactivesystems.getInactiveSystems(username,  password)
        self.get_inactive_systems.getinactives()

    def getactive_systems(self):
        self.mynum = 0
        #print('self.all_list in function: %s' %(self.all_list))
        for i in self.new_list:
            serverid = self.all_list[self.mynum]['id']
            for x in self.get_inactive_systems.systemlist:
                if str(serverid) == str(x):
                    try:
                        #print('\033[2;31;40mwill be deleted as the system is inactive:\n %s'% (self.all_list[self.mynum]))
                        del self.all_list[self.mynum]
                        self.mynum -= 1
                    except KeyError:
                        print("Key 'testing' not found")
            self.mynum += 1
        return self.all_list
