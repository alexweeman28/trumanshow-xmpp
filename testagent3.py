#!/usr/bin/python

import multiprocessing as mp
import time, sys, pickle
from chatagent3 import ChatAgent
from time import strftime

# The list of XMPP agents is created by a script in
# the accounts directory, named xmpp_accounts.py. This
# script then stores a Python dictionary of agent JIDs
# and their associated passwords in a Python pickle
# file: accounts/xmpp_accounts.p.
agentList = pickle.load(open('accounts/xmpp_accounts.p', 'rb'))

# This delay is required to keep the newly-hatching agents
# from overwhelming the ClientXMPP class/XMPP server with
# the admin traffic associated with logging in. The current
# setting of 5 seconds is arbitrary and could probably be
# reduced somewhat, if necessary.
slow_start = 5 #seconds

for agent in agentList:
    try:
        print(strftime('%H:%M:%S') + ' Spawning child process for ' + agent + '...', end = '')
        agent = mp.Process(target=ChatAgent, args=(agent,agentList[agent]),)
        agent.start()
        print('success!')
        time.sleep(slow_start)
    except Exception as e:
        print('\nError: unable to start thread for ' + agent, e)
    except KeyboardInterrupt:
        sys.exit()
                    
while True:
    try:
        time.sleep(30)
    # Exit the script by pressing Ctrl-c
    except KeyboardInterrupt:
        # This driver script only needs to take care of itself
        #  here. The child processes will all see the signal 
        # and ChatBot class  includes code to allow agents to 
        # gracefully exit on their own. We're all adults here.
        print('Bye!')
        sys.exit()
