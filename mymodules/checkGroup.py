#!/usr/bin/python
import xmlrpclib

import logging
logger = logging.getLogger(__name__)

class verifyGroup:
    
    def __init__(self,  session_client, session_key):
        self.session_client = session_client
        self.session_key = session_key
    
    def groupNotEmpty(self, group):
        logger.debug('Checking if System group "{0}" exists ...'.format(group))
        try:
           groupDetails = self.session_client.systemgroup.getDetails(self.session_key, group)
           logger.debug('Systemgroup "%s" exists' %(groupDetails))
        except:
           logger.debug('Systemgroup "%s" does not exist' %(group))
           return False
        if groupDetails['system_count'] > 0:
           logger.info('Systemgroup "%s" exists and contains %d systems' %(group, groupDetails['system_count']))
           return True
        else:
           logger.debug('Systemgroup "%s" is empty %d ' %(groupDetails,  groupDetails['system_count']))
           return False


    def getActiveSystemIDs(self, group):
        logger.debug('Checking which systems in group "%s" are active ...' %(group))
        activeSystems = self.session_client.systemgroup.listActiveSystemsInGroup(self.session_key, group)
        logger.info('Number of active systems in group "%s" is %d' %(group, len(activeSystems)))
        for i in activeSystems:
          logger.debug('Active system in group "%s": (%d)' %(group, i))
        return activeSystems

