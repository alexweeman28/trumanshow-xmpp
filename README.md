# trumanshow-xmpp

A tool to generate network traffic in the form of XMPP messages exchanged among virtual agent threads with user accounts on chat servers running Prosody.

## Files

* accounts/ -- This directory provides a collection of scripts and other files to support account creation of XMPP chat agents for the Python 3 version.
* chatagent3.py -- The Python 3 ChatAgent class. Works well with Prosody servers. Note the requirements included in comments at the top of the file.
* prosody.cfg.lua -- Example prosody config file.
* testagent3.py -- The driver script for chatagent3.py. The Python 3 version spawns child processes (rather than threads) for the agents. This change was necessitated by the fact that the sleekxmpp client is itself threaded.

* python2_version/ -- This directory contains :
 * chatagent_home.py -- The Python 2 ChatAgent class. Works well with Prosody servers. Note the requirements included in comments at the top of the file.
 * testagent_home.py -- The driver script for chatagent_home.py.
 * buddylist.py -- This is a script to create rosters (buddy lists) for the Python 2 chat bots.

Differences between Python 3 and Python 2 versions:
 * Agent 'armies' created with the Python3 sleekxmpp ClientXMPP class require a slow start. Otherwise, it appears the system (client library and/or the XMPP server) is overwhelmed by the administrative message traffic, with the result, for example, that agents don't get their rosters from the server in a timely fashion. Disaster follows. The current lag time between spawning agent processes was chosen arbitrarily and can likely be reduced, if necessary.
 * Agents that are disconnected by the server when their messages are not well-formed (XML-speak), are evidently automatically (and silently) re-connected and authenticated by the Python 3 ClientXMPP class. This is evident from the Prosody server logs. Therefore, the code in the Python 2 version that handled this task has been removed.
