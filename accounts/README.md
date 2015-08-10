## trumanshow-xmpp/accounts

This directory provides a collection of scripts and other files to support account creation for XMPP ChatBots.

* names.txt -- A collection of 5163 popular first names (from 1999?) downloaded from the Census Bureau (all in uppercase). It's heavily weighted toward female names, for some reason.

* xmpp_accounts.py -- This script reads in the names from names.txt and produces a Python dictionary containing the specified number of XMPP account IDs, based on the names of provided servers, randomly-selected first names from names.txt and randomly-generated passwords. The newly created dictionary of account information is saved to a file named xmpp_accounts.p in the current directory, in Python Pickle format.

* xmpp_accounts.p -- A sample Python Pickle file produced by the xmpp_accounts.py script, using names from the names.txt file above.

* prosodyctl.py -- This script reads in the accounts dictionary from the Python Pickle file created with xmpp_accounts.py. The script then writes (to stdout) the prosodyctl statements to register the new accounts on their respective XMPP servers. The statements are written in distinct blocks, grouped by server name.

