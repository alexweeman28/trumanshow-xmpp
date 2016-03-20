## trumanshow-xmpp/accounts

This directory provides a collection of scripts and other files to support account creation for XMPP ChatBots.

* names.txt -- A collection of 5163 popular first names (from 1999?) downloaded from the Census Bureau (all in uppercase). It's heavily weighted toward female names, for some reason.

* xmpp_accounts.py -- This script reads in a list of names from a file names.txt in the current directory and produces a Python dictionary containing the specified number of XMPP account IDs, based on the names of provided servers, randomly-selected first names from names.txt and randomly-generated passwords. The newly created dictionary of account information is saved to a file named xmpp_accounts.p in the current directory, in Python Pickle format. This file can later be used with the script prosodyctl.py to create the accounts on the XMPP servers, and with the script build_rosters.py to create a dictionary of contact rosters for the XMPP accounts.

* xmpp_accounts.p -- A sample Python Pickle file produced by the xmpp_accounts.py script, using names from the names.txt file above.

* xmpp_rosters.p -- A sample Python Pickle file produced by the build_rosters.py script, using accounts created by the script xmpp_accounts.py.

* prosodyctl.py -- This script reads in the accounts dictionary from the Python Pickle file created with xmpp_accounts.py. The script then writes (to stdout) the prosodyctl statements to register the new accounts on their respective XMPP servers. The statements are written in distinct blocks, grouped by server name.

* build_rosters.py -- This script builds a dictionary of contact rosters for XMPP user accounts contained in a Python pickle dictionary produced with the script xmpp_accounts.py. The rosters will contain a number of contacts in the specified range, and the rosters will be saved in a Python pickle file in the current directory.

* buddy_list.py -- This script uses the dictionary of accounts built in the xmpp_accounts.py script and the rosters built in the build_rosters.py script to populate the rosters for all the ChatBots on their respective XMPP servers. This script also depends on the ChatBot class defined in chatboy.py, which in turn uses the sleekxmpp module to create XMPP clients. In particular, this script depvends on True settings for the auto_authorize and auto_subscribe options. In addition, it's important to keep in mind that the sleekxmpp.Client class uses threads. As a result, it's important to limit the number of ChatBot agents that are active at any given point in time. Otherwise, it's quite easy to exceed the Python interpreter's limit for active threads.

* chatbot.py -- This script provides a minimal, standalone implementation of the sleekxmpp.ClientXMPP class. It is used by the buddy_list.py script to log ChatBot agents (and the agents in their buddy lists) into their respective servers for the purpose of populating their rosters.
