#!/usr/bin/env python
################################################################
# This python3 script requires Ubuntu 14.04 or later.          #
# Earlier versions do not appear to offer the required,        #
# up-to-date sleekxmpp library.                                #
#                                                              #
# In addition, it must be noted that the version of            #
# sleekxmpp included in Ubuntu 14.04 (python3-sleekxmpp)       #
# is not sufficient (as of 8/2015), because it is not kept      #
# up to date with important changes.                           #
#                                                              #
# Follow these steps to install the latest sleekxmpp:          #
#                                                              #
#    1) sudo apt-get update                                    #
#    2) sudo apt-get install python3-pip  # also adds many     #
#                                         # dependencies       #
#    3) sudo pip3 install sleekxmpp                            #
#                                                              #
# Other Ubuntu dependencies: fortune-mod,                      #
#                                                              #
################################################################

import sleekxmpp
import sys
import os
import random
import sched, time
from time import strftime

class ChatAgent(sleekxmpp.ClientXMPP):
    '''Class defining semi-autonomous XMPP chat agents'''
    # These variables are used to pace the activity
    # rate of the agents and the probability that
    # they'll send a message when their turn comes up
    delay_min = 30 # seconds
    delay_max = 60 # seconds
    send_prob = 0.1

    def __init__(self, jid, password):
        'Create a chat agent'
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        # Using these seetings, we don't need to handle
        # subscription requests
        self.auto_authorize = True
        self.auto_subscribe = True
        # Save the account name for printing
        # in various messages
        self.__whoami = jid
        self.__sched = sched.scheduler(time.time, time.sleep)
        self.add_event_handler('session_start', self._start)
        self.add_event_handler('presence_probe', self._handle_probe)
        # Probably don't need the subscribe handler with
        # options for auto_authorize and auto_subscribe set above
        #self.add_event_handler('presence_subscribe', self._subscribe)
        self.add_event_handler('message', self._message)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0199')
        self._run()

    def _run(self):
        if self.connect():
            self.process(block=False)
        else:
            print(self.__whoami, 'unable to connect...')
            sys.exit(1)
        while True:
            try:
                self._sched_msg()
            except KeyboardInterrupt:
                self.disconnect()
                print(strftime("%H:%M:%S") + ' This is ' + self.__whoami + ' signing off!')
                sys.exit()
                        
    def _start(self, event):
        self.send_presence()
        self.get_roster()
        
    def _handle_probe(self, event):
        self.sendPresence(pto = event["from"])
    
    def _handle_subscribe(self, presence):
        sender = presence['from']
        # Reply with confirmation
        self.sendPresence(pto=sender, ptype="subscribed")
        self.sendPresence(pto=sender, ptype="subscribe")

    def _message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(strftime("%H:%M:%S") + ' ' + self.__whoami + ' received a message from', str(msg['from']).split('/')[0])
                
    def _sched_msg(self):
        'Schedule a message to be sent after a random delay, but only if we have an empty queue'
        if self.__sched.empty():
            # Scheduling a message is based on the
            # probability defined as a class variable
            r = random.randint(1,101)
            p = int(1 / ChatAgent.send_prob)
            if r % p == 0:                                
                delay = random.randint(ChatAgent.delay_min, ChatAgent.delay_max)
                self.__sched.enter(delay, 1, self.send_msg, ())
                self.__sched.run()
                self._loaded = True

    def send_msg(self, msg=None, to=None):
        'Send an XMPP message'
        if not msg:
            f = os.popen('fortune')
            msg = f.read().strip()
            f.close()
        if not to:
            while True:
                # Pick a random jid from our roster, but first
                # check whether the roster actually contains any
                # chat buddies at this point...
                if len(list(self.client_roster.keys())) < 1:
                    print(self.__whoami, 'has NO friends!')
                    print(strftime("%H:%M:%S") + ' ' + self.__whoami, 'has NO friends!')
                    return
                to = random.choice(list(self.client_roster.keys()))
                me = self.__whoami
                # Let's not send messages to myself, so we'll loop
                # until the randomly-selected addressee isn't me. This
                # was an issue with the Python 2 version of xmpp, but
                # may not be with sleekxmpp. Still, it doesn't hurt
                # to check.
                if to != me:
                    break
        print(strftime("%H:%M:%S") + ' ' + self.__whoami + ': sending message to:', to)
        self.send_message(to, msg)

#    This is the old, Python 2 version, replaced by a simpler version that
#    simply prints the fact of a message's receipt
#    def _message(self, sess, mess):
#        'Method to handle receipt of XMPP messages'
#        mess_text = mess.getBody()
#        mess_from = mess.getFrom().getStripped()
#        print(strftime("%H:%M:%S") + ' ' + self.__whoami, 'received message from: ', mess_from)
#        # Sending a reply is based on the probability
#        # of doing so, defined as a class variable
#        r = random.randint(1,101)
#        p = int(1 / ChatAgent.send_prob)
#        if r % p == 0:
#            f = os.popen('fortune')
#            reply = 'Thanks for checking in!\n' +  f.read().strip()
#            f.close()
#            mess_reply = mess.buildReply(reply)
#            self.send_msg(mess_reply, mess_from)

