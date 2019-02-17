#!/usr/bin/python

class verifyChannels:
    def __init__(self):
        return
        
    def Channels(self,  client,  key,  channelname):
        migrate_f_channel = client.channel.software.getDetails(key, channelname)
        for key,value in migrate_f_channel.iteritems():
            if type(value) is dict:
                verifyChannels.Channels(value)
                #print(value)
            else:
                #print ("{0}: {1}".format(key, value))
                if key == 'label' and value == channelname:
                    #print('match gefunden')
                    return value

