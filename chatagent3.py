#!/usr/bin/env python
import sleekxmpp
import sys
import os
import random
import sched, time
from time import strftime

class ChatAgent(sleekxmpp.ClientXMPP):
    '''Class defining semi-autonomous XMPP chat agents'''
    delay_min = 30 # seconds
    delay_max = 60 # seconds
    send_prob = 0.1
    # A list to which agents that crash will be added
    # so that they can later be respawned by the driver script
    ###crashed = []
    def __init__(self, jid, password):
        'Create a chat agent'
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.auto_authorize = True
        self.auto_subscribe = True
        self.__whoami = jid
        self.__sched = sched.scheduler(time.time, time.sleep)
        self.add_event_handler('session_start', self._start)
        self.add_event_handler('presence_probe', self._handle_probe)
        self.add_event_handler('presence_subscribe', self._handle_subscribe)
        self.add_event_handler('message', self._message)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0199')
        try:
            self._run()
        except Exception as e:
            print('******************* KABOOM!!!! *******************')
            print(self.__whoami + ' JUST LEFT THE BUILDING!!!!')
            print('Here\'s the issue:', e)
            # Add this crashed agent to the class's list so
            # that a new thread can be spawned for it
            #ChatAgent.crashed.append(self.__whoami)

    def _run(self):
        if self.connect():
            self.process(block=False)
        else:
            print(self.__whoami, 'unable to connect...')
            sys.exit(1)
        while True:
            self._sched_msg()
                        
    def _start(self, event):
        self.send_presence()
        self.get_roster()
        
    def _handle_probe(self, presence):
        sender = presence['from']
        self.sendPresence(pto=sender, pstatus="Let's chat!", pshow="available")
    
    def _handle_subscribe(self, presence):
        sender = presence['from']
        # Reply with confirmation
        self.sendPresence(pto=sender, ptype="subscribed")
        self.sendPresence(pto=sender, ptype="subscribe")

    def _message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(strftime("%H:%M:%S") + ' ' + self.__whoami + 'received a message from', msg['from'])
                
    def _sched_msg(self):
        'Schedule a message to be sent after a random delay'
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
                # Pick a random jid from our roster
                if len(list(self.client_roster.keys())) < 1:
                    print(self.__whoami, 'has NO friends!')
                    print(strftime("%H:%M:%S") + ' ' + self.__whoami, 'has NO friends!')
                    return
                to = random.choice(list(self.client_roster.keys()))
                # Get my (stripped) jid
                #me = self.__my_jid.getNode() + '@' + self.__my_jid.getDomain()
                me = self.__whoami
                # Let's not try to send messages to myself
                if to != me:
                    break
        # Is the recipient online?
        #if self._roster.getShow(to) != None:
        print(strftime("%H:%M:%S") + ' ' + self.__whoami + ': sending message to:', to)
            #message = xmpp.Message(to, msg)
            #message.setAttr('type', 'chat')
            #self.__client.send(message)
        self.send_message(to, msg)
        #else:
        #print(strftime("%H:%M:%S") + ' ' + self.__whoami + ':', to, 'is not on line')
            #self._roster.Subscribe(to)
            #self._roster.Authorize(to)

    def _message(self, sess, mess):
        'Method to handle receipt of XMPP messages'
        mess_text = mess.getBody()
        mess_from = mess.getFrom().getStripped()
        print(strftime("%H:%M:%S") + ' ' + self.__whoami, 'received message from: ', mess_from)
        # Sending a reply is based on the probability
        # of doing so, defined as a class variable
        r = random.randint(1,101)
        p = int(1 / ChatAgent.send_prob)
        if r % p == 0:
            f = os.popen('fortune')
            reply = f.read().strip()
            f.close()
            mess_reply = mess.buildReply(reply)
            self.send_msg(mess_reply, mess_from)

#    def _presence(self,conn,msg):
#        'Method to handle XMPP presence'
#        jid=xmpp.protocol.JID(msg.getFrom())
#        name=self._roster.getName(jid.getNode()+"@"+jid.getDomain())
#        if not name:
#            name=jid.getNode()+"@"+jid.getDomain()
#        if not self.__showself and name == self.__my_jid.getNode()+"@"+self.__my_jid.getDomain():
#            return
#        status = msg.getStatus()
#        show = msg.getShow()
#        if not msg.getPriority():
#            status="Signed out"
#        elif not status and show:
#            status="("+msg.getShow()+")"
#        elif show and status:
#            status="("+msg.getShow()+") " + status
#        for f in self.__callbacks:
#            f(name,status)
        
#class ConnectionException(Exception):
#    def __init__(self):
#        pass
#    def __str__(self):
#        return "Error connecting to chat server"
#
#class AuthException(Exception):
#    def __init__(self):
#        pass
#    def __str__(self):
#        print "Error authenticating to chat server"
#
#if __name__=="__main__":
#    def callback(name,status):
#        print "%s: %s" % (name,status)
#        
#    DistTwit(sys.argv[1],sys.argv[2],callbacks=[callback])
