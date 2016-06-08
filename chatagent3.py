#!/usr/bin/env python3
################################################################
# This python3 script requires Ubuntu 14.04 or later.          #
# Earlier versions do not appear to offer the required,        #
# up-to-date sleekxmpp library.                                #
#                                                              #
# In addition, it must be noted that the version of            #
# sleekxmpp included in Ubuntu 14.04 (python3-sleekxmpp)       #
# is not sufficient (as of 8/2015), because it is not kept     #
# up to date with important changes.                           #
#                                                              #
# Follow these steps to install the latest sleekxmpp:          #
#                                                              #
#    1) sudo apt-get update                                    #
#    2) sudo apt-get install python3-pip  # also adds many     #
#                                         # dependencies       #
#    3) sudo pip3 install sleekxmpp                            #
#                                                              #
# Other Ubuntu dependencies: fortune-mod...                    #
#                                                              #
#    sudo apt-get install fortune-mod                          #
#                                                              #
################################################################

import sleekxmpp
import sys
import os
import random
import sched, time
from time import strftime
from configparser import ConfigParser

class ChatAgent(sleekxmpp.ClientXMPP):
    '''Class defining semi-autonomous XMPP chat agents'''
    # Read configuration values from settings.ini in the
    # present working directory.
    # These variables are used to pace the activity rate
    # of the agents and the probability that they'll actually
    # send a message when their scheduled turn comes up.
    # On error, use these defaults.
    defaults = {"send_prob": 0.1, "delay_min": 30, "delay_max": 60}
    try:
        parser = ConfigParser()
        parser.read('settings.ini')
        options = parser['settings']
        send_prob = options.getfloat('send_prob', defaults['send_prob'])
        delay_min = options.getint('delay_min', defaults['delay_min'])
        delay_max = options.getint('delay_max', defaults['delay_max'])
    except Exception as e:
        print('ChatAgent unable to read configuration from settings.ini: {}. Configuration set using hard-coded defaults.'.format(repr(e)))
        send_prob = defaults['send_prob']
        delay_min = defaults['delay_min']
        delay_max = defaults['delay_max']
    
    def __init__(self, jid, password):
        'Create a chat agent'
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        # Using these settings, we don't need to set
        # event handlers for subscription requests
        self.auto_authorize = True
        self.auto_subscribe = True
        # Save the account name for printing
        # in various console messages
        self.__whoami = jid
        # Create a scheduler for agent activity
        self.__sched = sched.scheduler(time.time, time.sleep)
        # The session_start handler is required. See not
        # with the handler
        self.add_event_handler('session_start', self._start)
        # The presence_probe handler is nice to have.
        self.add_event_handler('presence_probe', self._handle_probe)
        # Don't need the subscribe handler when options for
        # auto_authorize and auto_subscribe are set, as above
        #self.add_event_handler('presence_subscribe', self._subscribe)
        # The 'message' handler prints a console message when
        # a chat message is received--mostly for debugging now,
        # but could be used for auto-reply messages later.
        self.add_event_handler('message', self._message)
        # Various plugins, from the example code. Some may
        # not actually be necessary.
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
                # Sending of messages is scheduled
                self._sched_msg()
            except KeyboardInterrupt:
                # Chat agents all receive the Ctrl-c signal, even
                # when running as child processes. So, they can
                # (and should) exit gracefully on their own.
                self.disconnect()
                print(strftime("%H:%M:%S") + ' This is ' + self.__whoami + ' signing off!')
                sys.exit()
                        
    def _start(self, event):
        # If users don't report in to the server,
        # they don't get their rosters. Without
        # a roster, agents don't know who they
        # can communicate with.
        self.send_presence()
        self.get_roster()

    # A nice-to-have feature for finding
    # out (in other code) who's on line    
    def _handle_probe(self, event):
        self.sendPresence(pto = event["from"])

    # This method isn't currently used, but
    # may come in handy later...
    def _handle_subscribe(self, presence):
        sender = presence['from']
        # Reply with confirmation and start the
        # reverse subscription process.
        self.sendPresence(pto=sender, ptype="subscribed")
        self.sendPresence(pto=sender, ptype="subscribe")
        
    # This method is mostly here for debugging purposes.
    # It could be removed later to reduce console message
    # traffic, and/or be used to send automatic replies.
    def _message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(strftime("%H:%M:%S") + ' ' + self.__whoami + ' received a message from', str(msg['from']).split('/')[0])
                
    def _sched_msg(self):
        '''Schedule a message to be sent after a random delay, but *only* if the agent's send queue is empty'''
        if self.__sched.empty():
            # Scheduling a message is based on the
            # probability defined as a class variable above
            r = random.randint(1,101)
            p = int(1 / ChatAgent.send_prob)
            if r % p == 0:
                delay = random.randint(ChatAgent.delay_min, ChatAgent.delay_max)
                self.__sched.enter(delay, 1, self.send_msg, ())
                self.__sched.run()
                self._loaded = True

    def send_msg(self, msg=None, to=None):
        '''Send an XMPP message. For debugging or other purposes,
        messages and recipients can optionally be provided. Otherwise,
        agents send randomly selected "fortunes" from the fortune-mod
        package.'''
        if not msg:
            f = os.popen('fortune')
            msg = f.read().strip()
            f.close()
        if not to:
            while True:
                # Pick a random jid from our roster, but first
                # check whether the roster actually contains any
                # chat buddies at this point... Rarely a problem,
                # but an empty list raises an exception.
                if len(list(self.client_roster.keys())) < 1:
                    print(strftime("%H:%M:%S") + ' ' + self.__whoami, 'has NO friends!')
                    return
                to = random.choice(list(self.client_roster.keys()))
                me = self.__whoami
                # Let's not send messages to ourselves! So we'll loop
                # until the randomly-selected addressee isn't me. This
                # was an issue with the Python 2 version of xmpp, but
                # may not be with sleekxmpp. Still, it doesn't hurt
                # to check.
                # Update (8/10/2015): This check could be eliminated if
                # the send/receive status of the subscriber is checked
                # instead, and we only send to subscribers with the
                # appropriate status. Sending to subscribers for whom
                # 'to' is False or still pending doesn't cause problems; 
                # the messages are silently rejected by the server.
                if to != me:
                    break
        print(strftime("%H:%M:%S") + ' ' + self.__whoami + ': sending message to:', to)
        self.send_message(to, msg)
