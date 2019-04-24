#!/usr/bin/python

import salt.client
local = salt.client.LocalClient()

import logging
logger = logging.getLogger(__name__)

class mysalt:
    def __init__(self, hostname):
        self.hostname = hostname
        self.code = 3
        logger.debug('self.hostname "%s"' %(self.hostname))
        #print(self.hostname)
    def ping(self):
        try:
            jobreturn = local.cmd(self.hostname, 'test.ping',  timeout=5)
        except:
            logger.error('Salt test.ping failed - make sure you are running this as root')
        else:
            for k, v in jobreturn.items():
                if v == 1:
                    self.code = 0
                    logger.debug('salt test ping successful: %s' %(jobreturn))
                else:
                    self.code = 1
                    logger.debug('salt test ping failed. this system will be excluded from migration.: %s' %(jobreturn))
        finally:
            logger.debug('salt ping is done. %s'%(self.hostname))
        return self.code
