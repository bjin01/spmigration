#!/usr/bin/python
import logging
import sys

logger = logging.getLogger(__name__)

class verifyChannels:

    def __init__(self, suma_client, suma_key):
        self.suma_client = suma_client
        self.suma_key = suma_key
        self.all_channels = self.suma_client.channel.listAllChannels(self.suma_key)
       
        for c in self.all_channels:
          logger.debug('List all available channels: %s (%s)' %(c['name'], c['label']))
        return
        
    def Channels(self,  client,  suma_key,  channel2verify):
        logger.debug('Checking if Base Channel "{0}" exists ...'.format(channel2verify))
        
        logger.debug('List all channels: %s' %(self.all_channels))
        retVal = None

        for i in self.all_channels:
            channelLabel = i['label']
            logger.debug('Searching for channel "%s" in available channels: "%s"' %(channel2verify, channelLabel))
            if str(channelLabel) == str(channel2verify):
               logger.debug('Channel "{0}" exists'.format(channel2verify))
               migrate_f_channel = client.channel.software.getDetails(suma_key, channel2verify)
               if (type(migrate_f_channel) is dict) and (migrate_f_channel['parent_channel_label'] == ""):
                  logger.info('Channel "%s" exists and is a valid base channel' %(channel2verify))
                  retVal = channel2verify
                  break
               else:
                  logger.debug("Channel: %s is NOT a base channel" %(channel2verify))
        return retVal




