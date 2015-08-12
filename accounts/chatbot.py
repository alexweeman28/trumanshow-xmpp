###############################################
# This script provides a minimal, standalone  #
# implementation of the sleekxmpp.ClientXMPP  #
# class. It is used by the buddy_list.py      #
# to log ChatBot agents into their respective #
# servers for the purpose of populating their #
# rosters.                                    #
###############################################
import sys
import sleekxmpp
from time import strftime

class ChatBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.whoami = jid
        self.auto_authorize = True
        self.auto_subscribe = True                        
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0199')
        self.run()
        
    def start(self, event):
        self.send_presence()
        self.get_roster()
        
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            who = str(msg['from']).split('/')[0]
            print(strftime('%H:%M:%S') + ' Received message from ' + who)
        else:
            print(msg['type'])
            
    def handle_probe(self, presence):
        self.sendPresence(pto = event["from"])

    def send_msg(self, to, msg):
        self.send_message(to, msg)

    def subscribe(self, to):
        self.send_presence(pto=to, ptype='subscribe')
        
    def run(self):
        if self.connect():
            self.process(block=False)
            print('Running...')
        else:
            print('ERROR: ' + self.whoami + ' unable to connect to XMPP server')
            sys.exit(1)
