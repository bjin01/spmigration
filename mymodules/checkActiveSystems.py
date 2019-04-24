#!/usr/bin/python
import copy
#from mymodules import getInactiveSystems

import logging
logger = logging.getLogger(__name__)

class checkInactives:

    def __init__(self,  suma_client, suma_key):
        self.suma_client = suma_client
        self.suma_key = suma_key
        self.all_list = self.suma_client.system.listSystems(self.suma_key)
        self.new_list = copy.deepcopy(self.all_list)
       
        #self.get_inactive_systems = getInactiveSystems.getInactiveSystems(username,  password)
        self.get_inactive_systems = self.suma_client.system.listInactiveSystems(self.suma_key)
        for i in self.get_inactive_systems:
          logger.debug('List all inactive systems: %s (%s)' %(i['name'], i['id']))
        #self.get_inactive_systems.getinactives()

    def getactive_systems(self):
        self.mynum = 0
        logger.debug('List all systems: %s' %(self.all_list))
        for i in self.new_list:
            serverid = self.all_list[self.mynum]['id']
            logger.debug('Checking if system is active: %s (%s)' %(i['name'], i['id']))
            logger.debug('serverID: {0}'.format(serverid))
            #for x in self.get_inactive_systems.systemlist:
            for x in self.get_inactive_systems:
                inactiveserverid = x['id']
                logger.debug('Inactive system: %s (%s)' %(x['name'], x['id']))
                logger.debug('inactive serverID {0}'.format(inactiveserverid))
                if str(serverid) == str(inactiveserverid):
                #if str(serverid) == str(x):
                    try:
                        logger.info('Skipping system: %s (%s) Reason: inactive since %s' %(self.all_list[self.mynum]['name'], self.all_list[self.mynum]['id'], self.all_list[self.mynum]['last_checkin']))
                        del self.all_list[self.mynum]
                        self.mynum -= 1
                    except KeyError:
                        print("Key 'testing' not found")
            self.mynum += 1
        return self.all_list
