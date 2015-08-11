#########################################################
# This script builds a dictionary of contact rosters    #
# for XMPP user accounts contained in a pickle          #
# dictionary produced with the script xmpp_accounts.py. #
# The rosters will contain a number of contacts in the  #
# specified range, and the rosters will be saved in a   #
# Python pickle file in the current directory.          #
#########################################################
import random
import pickle

# What are the min/max number of contacts each
# XMPP user should have in his roster?
min = 4
max = 8

def build_rosters(accounts):
    rosters = {}
    allUsers = list(accounts.keys())
    for user in allUsers:
        roster = []
        total = random.randint(min, max)
        print('Building roster of {} buddies for '.format(total) + user + ':')
        count = 0
        while count < total:
            test = random.choice(allUsers)
            if test != user and test not in roster:
                roster.append(test)
                count += 1
            rosters[user] = roster
    return rosters

if __name__=='__main__':
    try:
        accounts = pickle.load(open("xmpp_accounts.p", "rb"))
    except:
        print("ERROR: Can't open or read file ./xmpp_accounts.p")
    rosters = build_rosters(accounts)
    pickle.dump(rosters, open("xmpp_rosters.p", "wb"))
