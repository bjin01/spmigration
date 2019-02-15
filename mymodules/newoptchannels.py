#!/usr/bin/python

class getnew_optionalChannels:
    def __init__(self,  suma_client, suma_key, serverid):
        self.suma_client = suma_client
        self.suma_key = suma_key
        self.optionalChannels = []
        self.serverid = serverid
        childchannels = self.suma_client.system.listSubscribedChildChannels(self.suma_key,  self.serverid)
        for u in childchannels:
            self.optionalChannels.append(u['label'])
        #print('The old child channels are: %s'%(self.optionalChannels))
    
    def find_replace(self, oldsp, newsp):
        self.oldsp = oldsp
        self.newsp = newsp
        spvalue = ['-' + self.oldsp, '-' + self.newsp]
        newoptionChannels = []
        # define a functions that takes a dict and a dict for find replace values
        #print('the old value is %s and the new value is %s'%(spvalue[0],  spvalue[1]))
        for item in self.optionalChannels:
            newval = item.replace(spvalue[0], spvalue[1])
            newoptionChannels.append(newval)
        return newoptionChannels
        #print('the new child channels are: ',  newoptionChannels)
