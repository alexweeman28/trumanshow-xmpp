#!/usr/bin/env python
import xmpp
import sys
import os
import random
import sched, time
from time import strftime

class ChatAgent(object):
    '''Class defining semi-autonomous XMPP chat agents'''
    delay_min = 30 # seconds
    delay_max = 60 # seconds
    send_prob = 0.1
    # A list to which agents that crash will be added
    # so that they can later be respawned by the driver script
    crashed = []
    def __init__(self,user,pwd,callbacks=None,showself=False):
        'Create a chat agent'
        self.__whoami = user
        self.__my_jid = xmpp.protocol.JID(user + '/chatagent.py')
        self.__client = xmpp.Client(self.__my_jid.getDomain(), debug=[])
        if not callbacks:
            self.__callbacks=[]
        else:
            self.__callbacks=callbacks
        self.__sched = sched.scheduler(time.time, time.sleep)
        self.__showself=showself
        self._connect()
        self._auth(pwd)
        try:
            self._run()
        except Exception, e:
            print '******************* KABOOM!!!! *******************'
            print self.__whoami + ' JUST LEFT THE BUILDING!!!!'
            print 'Here\'s the issue:', e
            # Add this crashed agent to the class's list so
            # that a new thread can be spawned for it
            ChatAgent.crashed.append(self.__whoami)
    def _connect(self):
        'Private method to connect to XMPP server'
        #print self.__whoami + ': connecting...'
<<<<<<< HEAD
        try:
            self.__client.connect()
        except Exception, e:
            print 'ERROR: Can\'t connect to chat server:', e
            sys.exit()
            #raise ConnectionException()
=======
        if self.__client.connect() == "":
            raise ConnectionException()
>>>>>>> 0e60e4db74c746d2de9aec1c6d0c61a6c81cf76e

    def _auth(self,pwd):
        'Private method to authenticate to XMPP server'
        #print self.__whoami +': authenticating...'
<<<<<<< HEAD
        try:
            self.__client.auth(self.__my_jid.getNode(),pwd):
        except Exception, e:
            print 'ERROR: Authentication failed:', e
            #raise AuthException()
=======
        if self.__client.auth(self.__my_jid.getNode(),pwd) == None:
            raise AuthException()
>>>>>>> 0e60e4db74c746d2de9aec1c6d0c61a6c81cf76e

    def add_callback(self,func):
        'Add a callback function' # Do we need this?
        self.__callbacks.append(func)

    def _sched_msg(self):
        'Schedule a message to be sent after a random delay'
        if self.__sched.empty():
            # Scheduling a message is based on the
            # probability defined as a class variable
            r = random.randint(1,101)
            p = int(1 / ChatAgent.send_prob)
            if r % p == 0:                                
                delay = random.randint(ChatAgent.delay_min, ChatAgent.delay_max)
                self.__sched.enter(delay, 1, self._send_msg, ())
                self.__sched.run()
                self._loaded = True

    def _send_msg(self, msg=None, to=None):
        'Send an XMPP message'
        if not msg:
            f = os.popen('fortune')
            msg = f.read().strip()
            f.close()
        if not to:
            while True:
                # Pick a random jid from our roster
                to = random.choice(self._roster.getItems())
                # Get my (stripped) jid
                me = self.__my_jid.getNode() + '@' + self.__my_jid.getDomain()
                # Let's not try to send messages to myself
                if to != me:
                    break
        # Is the recipient online?
        if self._roster.getShow(to) != None:
            print strftime("%H:%M:%S") + ' ' + self.__whoami + ': sending message to:', to
            message = xmpp.Message(to, msg)
            message.setAttr('type', 'chat')
            self.__client.send(message)
        else:
            print strftime("%H:%M:%S") + ' ' + self.__whoami + ':', to, 'is not on line'
            self._roster.Subscribe(to)
            self._roster.Authorize(to)

    def _run(self):
        pres = xmpp.Presence()
        pres.setShow('online')
        pres.setStatus('let\'s chat!')
        pres.setPriority(1)
        self.__client.send(pres)
        self._roster = self.__client.getRoster()
        self.__client.RegisterHandler('presence', self._presence)
        self.__client.RegisterHandler('message', self._message)
        while True:
            try:
                self.__client.Process(1)
                self._sched_msg()
            except KeyboardInterrupt:
                break

    def _message(self, sess, mess):
        'Method to handle receipt of XMPP messages'
        mess_text = mess.getBody()
        mess_from = mess.getFrom().getStripped()
        print strftime("%H:%M:%S") + ' ' + self.__whoami, 'received message from: ', mess_from
        # Sending a reply is based on the probability
        # of doing so, defined as a class variable
        r = random.randint(1,101)
        p = int(1 / ChatAgent.send_prob)
        if r % p == 0:
            f = os.popen('fortune')
            reply = f.read().strip()
            f.close()
            mess_reply = mess.buildReply(reply)
            self._send_msg(mess_reply, mess_from)

    def _presence(self,conn,msg):
        'Method to handle XMPP presence'
        jid=xmpp.protocol.JID(msg.getFrom())
        name=self._roster.getName(jid.getNode()+"@"+jid.getDomain())
        if not name:
            name=jid.getNode()+"@"+jid.getDomain()
        if not self.__showself and name == self.__my_jid.getNode()+"@"+self.__my_jid.getDomain():
            return
        status = msg.getStatus()
        show = msg.getShow()
        if not msg.getPriority():
            status="Signed out"
        elif not status and show:
            status="("+msg.getShow()+")"
        elif show and status:
            status="("+msg.getShow()+") " + status
        for f in self.__callbacks:
            f(name,status)
        
class ConnectionException(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Error connecting to chat server"

class AuthException(Exception):
    def __init__(self):
        pass
    def __str__(self):
        print "Error authenticating to chat server"

#if __name__=="__main__":
#    def callback(name,status):
#        print "%s: %s" % (name,status)
#        
#    DistTwit(sys.argv[1],sys.argv[2],callbacks=[callback])
