import time

'''
data = {
    'users': [ {
                'username':             str
                'password':             str
                'time_last_login':      int
                'time_last_logout':     int
                'time_frozen':          int
                'time_last_active':     int
                'soc':                  object
                'blocker':              set()
                'blockee':              set()
                'recvMsg':              []
                } ]
'''
# initialise all keys in data
data = { 'users': [] }    

def loadTxtFile():
    with open('credentials.txt', 'r') as f:
        for line in f:
            name, psw = line.strip().split()
            loadTxtUser(name, psw)       

def loadTxtUser(name, psw):
    global data
    userInfo = { 'username': name, 
                 'password': psw, 
                 'time_last_login': 0,
                 'time_last_logout': 0,
                 'time_frozen': 0,
                 'time_last_active': 0,
                 'soc': None,
                 'blocker': set(),
                 'blockee': set(),
                 'recvMsg': []
                }
    data['users'].append(userInfo)

def addNewUsrToTxtFile(username, psw):
    with open('credentials.txt', 'a') as f:
        f.write(f'\n{username} {psw}')
    # return True

def getUserInfo(name):
    global data
    for user in data['users']:
        if user['username'] == name:
            return user.copy()

def addNewUsrIntoDB(name, psw, socket):
    global data
    newUserInfo = { 'username': name, 
                    'password': psw, 
                    'time_last_login': int(time.time()),
                    'time_last_logout': 0,
                    'time_frozen': 0,
                    'time_last_active': 0,
                    'soc': socket,
                    'blocker': set(),
                    'blockee': set(),
                    'recvMsg': []
                  }
    data['users'].append(newUserInfo)

def freezeLogin(name):
    global data
    for user in data['users']:
        if user['username'] == name:
            user['time_frozen'] = int(time.time())

def logInUser(name, socket):
    global data
    for user in data['users']:
        if user['username'] == name:
            user['time_last_login'] = int(time.time())
            user['time_frozen'] = 0
            user['soc'] = socket

def logOutUser(name):
    global data
    for user in data['users']:
        if user['username'] == name:
            user['time_last_logout'] = int(time.time())
            user['time_last_active'] = 0
            user['soc'] = None

def updateActiveTime(name):
    global data
    for user in data['users']:
        if user['username'] == name:
            user['time_last_active'] = int(time.time())

def isUsrOnline(name):
    for user in data['users']:
        if user['username'] == name and user['time_last_login'] > user['time_last_logout']:
            return True

def getOnlineUsr(name):
    global data
    usrsOn = []
    for user in data['users']:
        if user['username'] != name and name not in user['blockee']:
            if user['time_last_login'] > user['time_last_logout']:
                usrsOn.append(user['username'])
    return usrsOn        

def getSinceUsr(name, sinceTime):
    global data
    usrsOn = []
    for user in data['users']:
        if user['username'] != name and name not in user['blockee']:
            diff = int(time.time()) - sinceTime
            if user['time_last_logout'] != 0 and user['time_last_logout'] > diff:
                usrsOn.append(user['username'])
            elif user['time_last_login'] != 0  and user['time_last_logout'] == 0:
                usrsOn.append(user['username'])
    return usrsOn

def getNonBlockedReciSock(sender):
    global data
    usrsOn = []
    for user in data['users']:
        if user['username'] != sender and user['soc']:
            if not isOnBlacklist(sender, user['username']):
                usrsOn.append(user['soc'])
    return usrsOn

def getNonBlockedSenderSock(sender):
    global data
    usrsOn = []
    for user in data['users']:
        if user['username'] != sender and user['soc']:
            if not isOnBlacklist(user['username'], sender):
                usrsOn.append(user['soc'])
    return usrsOn

def getMsgRecipSock(name):
    global data
    for user in data['users']:
        if user['username'] == name:
            return user['soc']

def setBlock(ber, bee):
    global data
    for user in data['users']:
        if user['username'] == ber:
            user['blockee'].add(bee)
        if user['username'] == bee:
            user['blocker'].add(ber)   

def setUnBlock(ber, bee):
    global data
    for user in data['users']:
        if user['username'] == ber:
            try:
                user['blockee'].remove(bee)
            except KeyError:
                return False
        if user['username'] == bee:
            try:
                user['blocker'].remove(ber)
            except KeyError:
                return False
    return True            

def isOnBlacklist(sender, receiver):
    global data
    for user in data['users']:
        if user['username'] == receiver and sender in user['blockee']:
            return True
    return False        

def isBlocked(name):
    global data
    for user in data['users']:
        if name in user['blockee']:
            return True
    return False

def addOfflineMsg(name, message):
    global data
    for user in data['users']:
        if user['username'] == name:
            user['recvMsg'].append(message)

def getOfflineMsg(name):
    global data
    msgs = []
    for user in data['users']:
        if user['username'] == name and user['recvMsg']:
            for m in user['recvMsg']:
                msgs.append(m)
            user['recvMsg'] = []
    return msgs        

def getAllUsers():
    global data
    return data['users'].copy()


def clearAllDate():
    global data
    data = { 'users': [] }

