#!/usr/bin/python
import thread, time
from chatagent_home import ChatAgent

agentList = {'hannah@elko.26maidenlane.net': 'bagjms6a', 'ella@elko.26maidenlane.net': 'afwtl7j4', 'joseph@elko.26maidenlane.net': 'xutxehdd', 'ava@elko.26maidenlane.net': 'ftgadqvl', 'victoria@elko.26maidenlane.net': 'pttktw42', 'sophia@elko.26maidenlane.net': 'famwzxe2', 'zoey@muliphen.26maidenlane.net': 'qndjgbt3', 'liam@elko.26maidenlane.net': '7nfun5em', 'charlotte@elko.26maidenlane.net': '6bgkmjfn', 'natalie@elko.26maidenlane.net': 'uc4r5ck8', 'michael@muliphen.26maidenlane.net': 'abpwlsud', 'isabella@muliphen.26maidenlane.net': 'ruftsefb', 'david@elko.26maidenlane.net': 'a22q6drp', 'olivia@elko.26maidenlane.net': 'ryex5cw2', 'chloe@muliphen.26maidenlane.net': 'ht9czbxz', 'joshua@muliphen.26maidenlane.net': 'nse9jg4k', 'logan@muliphen.26maidenlane.net': 'd8hlynaq', 'lucas@muliphen.26maidenlane.net': '2hpa92zw', 'emma@muliphen.26maidenlane.net': 'kbsemhzg', 'daniel@elko.26maidenlane.net': 'uutg3zbt', 'abigail@muliphen.26maidenlane.net': 'rlez4xd8', 'andrew@elko.26maidenlane.net': 'uakmbr33', 'william@muliphen.26maidenlane.net': '3hkkp8xt', 'elijah@muliphen.26maidenlane.net': 'drtkybpu', 'sofia@elko.26maidenlane.net': 'eyvwbunb', 'james@muliphen.26maidenlane.net': 'buahehfk', 'alexander@elko.26maidenlane.net': '6tvmhfu6', 'anthony@muliphen.26maidenlane.net': 'ntwqhace', 'grace@muliphen.26maidenlane.net': 'zsxhwdhj', 'ethan@elko.26maidenlane.net': 'wnz7s7gr', 'aiden@elko.26maidenlane.net': 'ngcy4zvy', 'emily@elko.26maidenlane.net': 'zha7utjl', 'jackson@elko.26maidenlane.net': 's79jvucp', 'addison@elko.26maidenlane.net': 'yytezmrb', 'aubrey@muliphen.26maidenlane.net': 'u36fnreq', 'jayden@muliphen.26maidenlane.net': 'veynzak6', 'madison@elko.26maidenlane.net': 'kkgez8uy', 'mia@muliphen.26maidenlane.net': 'uysjzwdr', 'harper@muliphen.26maidenlane.net': 'vyx4uaz7', 'mason@elko.26maidenlane.net': 'kmmfvqva', 'benjamin@elko.26maidenlane.net': '2ekvwjp7', 'gabriel@elko.26maidenlane.net': 'rdqp9qsq', 'amelia@elko.26maidenlane.net': '2d9hvmkp', 'jacob@muliphen.26maidenlane.net': 'sgwnd9km', 'evelyn@muliphen.26maidenlane.net': '88ctr5py', 'elizabeth@muliphen.26maidenlane.net': 'asdjswcv', 'avery@muliphen.26maidenlane.net': 'pzljljjh', 'samuel@muliphen.26maidenlane.net': '6bfdzq76', 'noah@muliphen.26maidenlane.net': 'f7eclstk', 'matthew@muliphen.26maidenlane.net': 'vdcukvuk'}

# Create some agent threads as follows
for agent in agentList:
    #if agent.find('elko') >=0:
    #    continue
    try:
        print 'Spawning thread for ' + agent + '...',
        thread.start_new_thread( ChatAgent, (agent, agentList[agent], ) )
        print 'Success!'
    except:
        print 'Error: unable to start thread for ' + agent
while True:
    time.sleep(30)
    if len(ChatAgent.crashed) > 0:
        for i in ChatAgent.crashed:
            try:
                print 'Respawning thread for ' + i + '...',
                thread.start_new_thread( ChatAgent, (i, agentList[i], ) )
                print 'Success!'
            except:
                print 'Error: unable to restart thread for ' + i
            ChatAgent.crashed.remove(i)
    #pass
