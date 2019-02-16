#!/usr/bin/python
import xmlrpclib,  argparse

MANAGER_URL = "http://bjsuma.bo2go.home/rpc/api"
MANAGER_LOGIN = 'bjin'
MANAGER_PASSWORD = 'suse1234'
session_client = xmlrpclib.Server(MANAGER_URL, verbose=0)
session_key = session_client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

parser = argparse.ArgumentParser()
parser.add_argument("-base", "--current_base_channel", help="Enter the current base channel label. e.g. sles12-sp3-pool-x86_64 ",  required=True)
parser.add_argument("-newbase", "--new_base_channel", help="Enter the new base channel label. e.g. sles12-sp4-pool-x86_64 ",  required=True)
args = parser.parse_args()


def checkChannels(channelname):
    
    migrate_f_channel = session_client.channel.software.getDetails(session_key, args.current_base_channel)
    for key,value in migrate_f_channel.items():
        if type(value) is dict:
            yield from migrate_f_channel(value)
        else:
            yield (key, value)
    print(key, value)

