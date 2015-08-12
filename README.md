# trumanshow-xmpp

The included files provide for (semi-)autonomous chat bots for BetaPort.

TO DO: Update testagent3.py to use the dictionary of accounts saved in the xmpp_accounts.p file in the local directory, rather than a hardcoded version in the script itself.

* accounts/ -- This directory provides a collection of scripts and other files to support account creation of XMPP ChatBot agents for the Python 3 version.

* buddylist.py -- This is a script to create rosters (buddy lists) for the Python 2 chat bots. See the accounts directory for the Python 3 version.

* Python 3 version:
 * chatagent3.py -- The Python 3 ChatAgent class. Works well with Prosody servers. Note the requirements included in comments at the top of the file.
 * testagent3.py -- The driver script for chatagent3.py. The Python 3 version spawns child processes (rather than threads) for the agents. This change was necessitated by the fact that the sleekxmpp client is itself threaded.

* Differences between Python 3 and Python 2 versions:
 * Agent 'armies' created with the sleekxmpp ClientXMPP class require a slow start. Otherwise, it appears the system (client library and/or the XMPP server) is overwhelmed by the administrative message traffic, with the result, for example, that agents don't get their rosters from the server in a timely fashion. Disaster follows. The current lag time between spawning agent processes was chosen arbitrarily and can likely be reduced, if necessary.
 * Agents that are disconnected by the server when their messages are not well-formed (XML-speak), are evidently automatically (and silently) re-connected and authenticated by the ClientXMPP class. This is evident from the Prosody server logs. Therefore, the code in the Python 2 version that handled this task has been removed.

* Python 2 version:
 * chatagent_home.py -- The Python 2 ChatAgent class. Works well with Prosody servers. Note the requirements included in comments at the top of the file.
 * testagent_home.py -- The driver script for chatagent_home.py.
 * prosody.cfg.lua -- Example prosody config file.
