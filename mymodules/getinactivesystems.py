import shlex,  subprocess

class getInactiveSystems:
    def __init__(self,  username,  password):
        self.systemlist = []
        cmdx = "awk 'NR>2{print $1;}' "
        args1 = shlex.split(cmdx)
        f = open('output1.txt', 'wb')
        cmd1 = subprocess.Popen(['spacecmd', '-u', username, '-p', password, '-q', 'report_inactivesystems'], stdout=subprocess.PIPE)
        #print(cmd1)
        cmd2 = subprocess.Popen(args1, stdin=cmd1.stdout, stdout=subprocess.PIPE)
        cmd1.stdout.close()
        output = cmd2.communicate()[0]
        cmd2.stdout.close()
        f.write(output)
        f.close()
        
    def getinactives (self):
          
            self.filepath = "output1.txt"
            with open(self.filepath) as fp:  
                cnt = 0
                newfile = fp.read().splitlines()
                for i in  newfile:
                   #print("Line {}: {}".format(cnt, i.strip()))
                   cnt += 1
                   self.systemlist.append(i)
                   #print('und weitere zeilen sind: ',  i)
            #self.subp.kill ()
            #print('the list is: ',  self.systemlist)
