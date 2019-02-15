import salt.client
local = salt.client.LocalClient()
class mysalt:
    def __init__(self, hostname):
        self.hostname = hostname
        self.code = 3
        #print(self.hostname)
    def ping(self):
        try:
            jobreturn = local.cmd(self.hostname, 'test.ping',  timeout=5)
        except:
            print('salt test.ping failed:',  jobreturn)
        else:
            for k, v in jobreturn.items():
                if v == 1:
                    self.code = 0
                    print('salt test ping successful: %s' %(jobreturn))
                else:
                    self.code = 1
                    print('salt test ping failed. this system will be excluded from migration.: %s' %(jobreturn))
        finally:
            print('salt ping is done. %s'%(self.hostname))
        return self.code
