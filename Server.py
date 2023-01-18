# Python 3
# Usage: python3 Server.py server_port block_duration(s) timeout(s)
# coding: utf-8

from socket import *
from threading import Thread
import sys, select, time, re
import db

class ClientThread(Thread):
    def __init__(self, clientAddr, clientSocket, blockDuration, timeOut):
        Thread.__init__(self)
        self.clientAddr = clientAddr
        self.clientSocket = clientSocket
        self.blockTime = blockDuration
        self.timeOutTime = timeOut
        self.clientAlive = False
        
        print("===== New connection created with: ", clientAddr)
        self.clientAlive = True
        
    def run(self):
        usrName = self.clientSocket.recv(1024).decode()
        # check login
        user = self.processLogin(usrName)
        if not user:
            self.clientAlive = False
        
        socList = db.getNonBlockedSenderSock(user)
        if socList:
            for s in socList:
                if user:
                    s.send(f'{user} logged in'.encode())
        
        while self.clientAlive:
            message = self.clientSocket.recv(1024).decode()

            if message == 'logout':
                socList = db.getNonBlockedSenderSock(user)
                if socList:
                    for s in socList:
                        s.send(f'{user} logged out'.encode())
                db.logOutUser(user)
                # print(f"===== {user} logout")
                break
            
            elif message == 'whoelse':
                usrList = db.getOnlineUsr(user)
                if not usrList:
                    self.clientSocket.send('[NO ONE CURRENTLY ONLINE]'.encode())
                else:
                    for u in usrList:
                        self.clientSocket.send(u.encode())
                        time.sleep(0.1)
            
            elif re.search('whoelsesince ', message):
                sinceTime = re.search(r' (\d+)$', message).group(1)
                usrList = db.getSinceUsr(user, int(sinceTime))
                if not usrList:
                    self.clientSocket.send(f'[NO ONE ONLINE SINCE {sinceTime}]'.encode())
                else:
                    for u in usrList:
                        self.clientSocket.send(u.encode())
                        time.sleep(0.1)
            
            elif re.search('broadcast ', message):
                msg = message[10:]
                self.broadcast(msg, user)
                if db.isBlocked(user):
                    self.clientSocket.send(f'Your message could not be delivered to some recipients'.encode())

            elif re.search(r'^block ', message):
                blockee = message[6:]
                db.setBlock(user, blockee)
                self.clientSocket.send(f'{blockee} is blocked'.encode())
            
            elif re.search(r'^unblock ', message):
                blockee = message[8:]
                if db.setUnBlock(user, blockee):
                    self.clientSocket.send(f'{blockee} is unblocked'.encode())
                else:
                    self.clientSocket.send(f'Error. {blockee} was not blocked'.encode())

            elif re.search(r'^message ', message):
                name = re.search(r'^message ([^ ]+) (.+)$', message).group(1)
                msg = re.search(r'^message ([^ ]+) (.+)$', message).group(2)
                recipient = db.getUserInfo(name)
                if recipient:
                    if db.isOnBlacklist(user, name):
                        self.clientSocket.send(f'[SENDER BLOCKED]Your message could not be delivered as the recipient has blocked you'.encode())
                    else:
                        recSock = db.getMsgRecipSock(name)
                        try:
                            recSock.send(f'{user}: {msg}'.encode())
                        except:                            
                            db.addOfflineMsg(name, f'{user}: {msg}')
                else:
                    self.clientSocket.send(f'Error. Invalid user'.encode())

            elif message == 'read':
                msgList = db.getOfflineMsg(user)
                if msgList:
                    for m in msgList:
                        self.clientSocket.send(m.encode())
                        time.sleep(0.1)
                else:
                    self.clientSocket.send('[NO OFFLINE MESSAGE]'.encode())


        self.closeThread() 
    
    def processLogin(self, username):
        # process usrname
        user = db.getUserInfo(username)
        if user is None:
            self.clientSocket.send('Sign-up'.encode())
            psw = self.clientSocket.recv(1024).decode() 
            
            db.addNewUsrToTxtFile(username, psw)
            db.addNewUsrIntoDB(username, psw, self.clientSocket)
                       
            return username
        else:
            self.clientSocket.send('Log-in'.encode())
            for i in range(3):
                psw = self.clientSocket.recv(1024).decode()
                if user['password'] == psw:
                    timeO = user['time_frozen']
                    if timeO:
                        timeN = int(time.time())
                        block_time = timeN - timeO
                        if (block_time < self.timeOutTime):
                            self.clientSocket.send('Login Blocked'.encode())
                            return None
                        else:    
                            db.logInUser(username, self.clientSocket)
                            self.clientSocket.send('Login Success'.encode())
                            # print(f'===== {username} has logged in')
                            return username
                    else:
                        db.logInUser(username, self.clientSocket)
                        self.clientSocket.send('Login Success'.encode())
                        # print(f'===== {username} has logged in')
                        return username
                else:
                    self.clientSocket.send('Login Failed'.encode())
            db.freezeLogin(username)
        return None
    
    def closeThread(self):
        self.clientSocket.close()

    def broadcast(self, msg, name):
        socList = db.getNonBlockedReciSock(name)
        if socList:
            for s in socList:
                s.send(f'{name}: {msg}'.encode())

    def sendOfflineMsg(self, name):
        msgList = db.getOfflineMsg(name)
        if msgList:
            for m in msgList:
                self.clientSocket.send(m.encode())

if __name__ == '__main__':
    
    if len(sys.argv) != 4:
        print("\n===== Usage: python3 Server.py server_port block_duration(s) timeout(s) ======\n");
        exit(0);

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverAddr = ("localhost", int(sys.argv[1]))
    serverSocket.bind(serverAddr)
    # server to listen to incoming connections
    serverSocket.listen()

    print("\n===== Server is running =====")
    print("===== Waiting for connection request from clients...=====")

    # load credential to database
    db.loadTxtFile()
    
    blockDuration = int(sys.argv[2])
    timeOut = int(sys.argv[3])

    while True:
        try:
            clientSocket, clientAddr = serverSocket.accept()
            clientThread = ClientThread(clientAddr, clientSocket, blockDuration, timeOut)
            clientThread.start()
        
        except KeyboardInterrupt:
            serverSocket.close()
            exit()

        
