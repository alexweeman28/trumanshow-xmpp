# trumanshow-xmpp

A tool to generate network traffic in the form of XMPP messages exchanged among virtual agent threads with user accounts on chat servers running Prosody.

## Files

**accounts/:** This directory provides a collection of scripts and other files to support account creation of XMPP chat agents. See README.md in the accounts folder for details.

**READMD.md:** This file.

**chatagent3.py:** The ChatAgent class. Works well with Prosody servers.

**prosody.cfg.lua:** A sample prosody config file.

**testagent3.py:** The driver script for chatagent3.py. This script spawns child processes (rather than threads, as in the earlier, Python 2 version) for the agents. This change was necessitated by the fact that the sleekxmpp library client is itself threaded.

## Installation

The ChatAgent class (defined in chatagent3.py) requires Ubuntu 14.04 or later. Earlier versions do not appear to offer the required, up-to-date sleekxmpp library. It must also be noted that the sleekxmpp package included in Ubuntu 14.04 (python3-sleekxmpp is not sufficient (as of 8/2015), because it is not kept up to date with important changes.

Follow these steps to install the latest version of the sleekxmpp library:
```
sudo apt-get update
sudo apt-get install python3-pip  # also adds many dependencies
sudo pip3 install sleekxmpp
```
In addition, the ChatAgent class requires the fortune-mod package:
```
sudo apt-get install fortune-mod
```

## Configuration and Use

Prior to running this application, user accounts for virtual chat agents must be created on the XMPP servers among which chat traffic is to be exchanged. Scripts and other files needed to generate randomly-selected usernames and passwords, as well as creating accounts, are included in the accounts directory in this repository. See the README.md file in the accounts directory for details.

Once the virtua chat accounts have been created, run the ```testagent3.py``` script to generate random XMPP traffic among the virtual chat agents:
```
python3 testchat3.py
```
The configuration settings in the file settings.ini control the behavior of the user agents, specifically the probability of sending emails and the range of sleep times between rounds of activity.