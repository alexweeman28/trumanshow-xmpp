##########################################################
# This script uses the dictionary of accounts built in  #
# the xmpp_accounts.py script and the rosters built in   #
# the build_rosters.py script to populate the rosters    #
# for all the ChatBots on their respective XMPP servers. #
# This script also depends on the ChatBot class defined  #
# in chatbot.py, which in turn uses the sleekxmpp module # 
# to create XMPP clients. In particular, this script     #
# depends on True settings for the auto_authorize and    #
# auto_subscribe options.
# In addition, it's important to keep in mind that the   #
# sleekxmpp.Client class uses threads. As a result, it's #
# important to limit the number of ChatBot agents that   #
# are active at any given point in time. Otherwise, it's #
# quite easy to exceed the Python interpreter's limit    #
# for active threads.                                    #
##########################################################
import pickle
import time
from time import strftime
from chatbot import ChatBot

# Load the dictionaries of accounts and rosters
# created in scripts xmpp_accounts.py and
# xmpp_rosters.py
accounts = pickle.load(open('xmpp_accounts.p', 'rb'))
rosters = pickle.load(open('xmpp_rosters.p', 'rb'))

# Loop through the chat agent accounts to set up
# their respective rosters on their individual
# chat servers
for agent in accounts:
    try:
        print(strftime('%H:%M:%S') + ' Logging ' + agent + ' into chat server...', end='')
        user = ChatBot(agent, accounts[agent])
    except Exception as e:
        print('Unable to create Chatbot:', e)
        continue
    # Loop through the contacts and send a
    # subscription request to each. We are
    # relying on the auto_authorize and
    # auto_subscribe options being set in
    # the ChatBot class to enable a two-way
    # subscription to be set up with a single
    # subscription request
    for contact in rosters[agent]:
        try:
            # Contacts also need to be logged in to
            # allow processing of the subscription request
            print('\tLogging ' + contact + ' into chat server...', end='')
            buddy = ChatBot(contact, accounts[contact])
        except Exception as e:
            print('Unable to create Chatbot:', e)
        print('\tSending subscription request to ' + contact + '...')
        user.subscribe(contact)
        # This delay allows time for the rosters to be updated
        # in both directions: to and from
        time.sleep(3)
        print('\tDisconnecting ' + contact + ' from chat server')
        # Now disconnect this buddy, so as not to exceed Python's
        # limit on running threads
        buddy.disconnect()
    # Finally, disconnect the current user, again to limit the
    # number of threads running at any given time.
    user.disconnect()
