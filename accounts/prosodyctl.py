## This script uses Pickle to import a
# dictionary of xmpp accounts/passwords
# from a file named xmpp_accounts.p
# in the local directory. Using the data
# in this dictionary, the script writes
# (to stdout) a series of prosodyctl
# statements to register the included users
# on their respective xmpp servers.

import pickle
import sys

try:
    accounts = pickle.load( open( "xmpp_accounts.p", "rb" ) )
except:
    print("ERROR: Unable to load accounts dictionary from ./xmpp_accounts.p")

servers = set()
for account in accounts.keys():
    servers.add(str(account).split('@')[1])
#print(list(servers))

for server in servers:
    print('\nAccounts for ' + server + ':')
    for account in accounts.keys():
        user = str(account).split('@')[0]
        domain = str(account).split('@')[1]
        if domain == server:
           print('sudo prosodyctl register ' + user + ' ' + domain + ' ' +accounts[account])

