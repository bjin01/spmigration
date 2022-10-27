#!/usr/bin/python

class myGroup:
    
    def __init__(self,  session_client, session_key):
        self.session_client = session_client
        self.session_key = session_key
        self.groupname = 'spmigration_temp'
    
    def newGroup(self):
        self.mygroups = self.session_client.systemgroup.listAllGroups(self.session_key)
        self.description = 'This is a temp group created by spmigration.py script for service pack migration automation. Just for information. Feel free to delete it.'
        try:
            self.session_client.systemgroup.create(self.session_key, self.groupname, self.description)
        except:
            print('group exists already!.')
            
    def addSystemsToGroup(self,  systemlist):
        self.systemlist = systemlist           
        system_added = self.session_client.systemgroup.addOrRemoveSystems(self.session_key,  self.groupname,  self.systemlist,  True)
        return system_added
