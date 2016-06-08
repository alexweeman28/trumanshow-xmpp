# trumanshow-xmpp

A tool to generate network traffic in the form of XMPP messages exchanged among virtual agent threads with user accounts on chat servers running Prosody.

## Files

**accounts/:** This directory provides a collection of scripts and other files to support account creation of XMPP chat agents.
**READMD.md:** This file.
**chatagent3.py:** The ChatAgent class. Works well with Prosody servers.
**prosody.cfg.lua:** A sample prosody config file.
**testagent3.py:**The driver script for chatagent3.py. This script spawns child processes (rather than threads, as in the earlier Python 2 version) for the agents. This change from the earlier version was necessitated by the fact that the sleekxmpp library client is itself threaded.

## Installation

The ChatAgent class (defined in chatagent3.py) requires Ubuntu 14.04 or later. Earlier versions do not appear to offer the required, up-to-date sleekxmpp library. It must also be noted that the sleekxmpp package included in Ubuntu 14.04 (python3-sleekxmpp is not sufficient (as of 8/2015), because it is not kept up to date with important changes.

Follow these steps to install the latest version of the sleekxmpp library:
```sudo apt-get update
sudo apt-get install python3-pip  # also adds many dependencies
sudo pip3 install sleekxmpp```
In addition, the ChatAgent class requires the fortune-mod package:
```sudo apt-get install fortune-mod```