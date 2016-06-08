# trumanshow-xmpp/accounts

This directory provides a collection of scripts and other files to support account creation for XMPP ChatBots.

## Files
**names.txt:** A collection of 5,000+ popular first names (from 1999?) downloaded from the Census Bureau (all in uppercase). It's heavily weighted toward female names, for some reason.

**xmpp_accounts.py:** This script reads in a list of names from the file ```names.txt``` in the current directory and produces a Python dictionary containing the specified number of XMPP account IDs, based on the names of provided servers, randomly-selected first names and randomly-generated passwords. The newly created dictionary of account information is saved to a file named ```xmpp_accounts.p``` in the current directory, in Python Pickle format. This file can later be used with the script ```prosodyctl.py``` to create accounts on the XMPP servers, and with the script ```build_rosters.py``` to create a dictionary of contact rosters for the XMPP accounts.

**xmpp_accounts.p:** A sample Python Pickle file produced by the ```xmpp_accounts.py``` script, using names from the ```names.txt``` file described above.

**xmpp_rosters.p:** A sample Python Pickle file produced by the ```build_rosters.py``` script, using accounts created by the script ```xmpp_accounts.py```.

**prosodyctl.py:** This script reads in the accounts dictionary from the Python pickle file ```xmpp_accounts.p``` created by ```xmpp_accounts.py```. The script then writes (to stdout) the ```prosodyctl``` statements needed to register the new accounts on their respective XMPP servers. The statements are written in distinct blocks, grouped by server name.

**build_rosters.py:** This script builds a dictionary of contact rosters for XMPP user accounts contained in the Python pickle dictionary ```xmpp_accounts.p``` produced with the script xmpp_accounts.py. The rosters will contain a number of contacts in the specified range, and the rosters will be saved in a Python pickle file named ```xmpp_rosters.p``` in the current directory.

**buddy_list.py:** This script uses the dictionary of accounts ```accounts.p``` built in the ```xmpp_accounts.py``` script and the rosters built in the ```build_rosters.py``` script to populate the rosters for all the ChatAgents on their respective XMPP servers. This script also depends on the ChatBot class defined in ```accounts/chatbot.py```, which in turn uses the sleekxmpp module to create XMPP clients. In particular, this script depends on ```True``` settings for the auto_authorize and auto_subscribe options. In addition, it's important to keep in mind that the sleekxmpp.Client class uses threads. As a result, it's important to limit the number of ChatBot agents that are active at any given point in time. Otherwise, it's quite easy to exceed the Python interpreter's limit for active threads.

**chatbot.py:** This script provides a minimal, standalone implementation of the sleekxmpp.ClientXMPP class. It is used by the ```buddy_list.py``` script to log ChatBot agents (and the agents in their buddy lists) into their respective servers for the purpose of populating their rosters.

## Installation

The script chatbot.py``` requires the third-party sleekxmpp library. See the installation in ```README.md``` in the main directory for installation steps.

## Configuration and Use

1) Run ```xmpp_accounts.py``` to create a dictionary of new XMPP account IDs and passwords. Prior to running the script, the fully-qualified domain name for each XMPP server, the numbers of accounts to be generated for each server (left to right), and the desired length of the randomly generated passwords must be entered in the first few lines of the script. When the script is run, the user account information will be written to a Python pickle file named ```xmpp_accounts.p``` in the present working directory.

2) Run ```build_rosters.py``` to create a dictionary of contact rosters for the XMPP user accounts generated in Step 1. These rosters will be written to the file ```xmpp_rosters.p``` in the current directory. The rosters for each account will contain a number of contacts in the range (between ```min``` and ```max```) specified in the first lines of the script.

3) Run ```prosodyctl.py``` to generate (to stdout) the prosodyctl statements to register the accounts generated in Step 1 above on their respective servers. For convenience's sake, the statements are written in distinct blocks, grouped by server name.

4) Using the prosodyctl statements generated in the previous step, register the XMPP accounts generated in Step 1 on their respective servers.

5) Run ```buddy_list.py``` to populate the rosters created in Step 2 for all the XMPP accounts registered in Step 4 on their respective XMPP servers.

