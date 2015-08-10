import string
import random
import pickle
# Identify some servers and the number of accounts
# per server
password_length = 8
num_accounts = [50, 50]
servers = ['davis.26maidenlane.net','reno.26maidenlane.net']

def make_passwords(n, x):
    'Create n random passwords each containing x characters'
    letters = [x for x in string.ascii_letters]
    digits = [x for x in string.digits]
    chars = letters + digits
    passwords = []
    for _ in range(n):
        passwords.append(''.join([random.choice(chars) for i in range(x)]))
    return passwords

def get_names(n):
    'Selects n random names from names.txt in current directory'
    all_names = []
    names = set()
    try:
        f = open('names.txt')
        for line in f:
            name = line.strip()
            all_names.append(name.lower())
        f.close()
    except:
        print("ERROR: Can't open and or read names.txt")
        return
    while len(names) < n:
        names.add(random.choice(all_names))
  
    return list(names)

def make_accounts(names, passwords, num_accounts, servers):
    'Create a dictionary of accounts:passwords from inputs'
    if len(names) != len(passwords):
        print("Error: The number of passwords doesn't match the nunber of names.")
        return
    if len(names) != sum(num_accounts):
        print("Error: The number of names doesn't match the number of accounts.")
        return

    accounts = {}
    j = 0
    offset = 0
    for i in range(len(servers)):
        while j < offset + num_accounts[i]:
            accounts[names[j] + '@' + servers[i]] = passwords[j]
            j += 1
        offset += num_accounts[i]
    return accounts

if __name__=='__main__':
    passwords = make_passwords(sum(num_accounts), password_length)
    names =  get_names(sum(num_accounts))
    accts = make_accounts(names, passwords, num_accounts, servers)
    print('Made a total of', len(accts), 'accounts')
    print('Dictonary of accounts saved to "./xmpp_accounts.p"')
    pickle.dump( accts, open( "xmpp_accounts.p", "wb" ) )
