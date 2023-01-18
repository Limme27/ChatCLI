# Python 3
# Usage: python3 Client.py server_port
# coding: utf-8

from socket import *
import sys, re, threading, time

def login(clientSocket):
    # server's response to username input
    userName = input('Username: ')
    clientSocket.sendall(userName.encode())
    recvMsg = clientSocket.recv(1024).decode()
    
    if recvMsg == 'Sign-up':
        psw = input('This is a new user. Enter a password: ')
        clientSocket.sendall(psw.encode())
        print('Welcome to the greatest messaging application ever!')
        return userName
    
    elif recvMsg == 'Log-in':
        # 1st try
        psw = input('Password: ')
        clientSocket.sendall(psw.encode())
        recvMsg = clientSocket.recv(1024).decode()
        if recvMsg == 'Login Success':
            print('Welcome to the greatest messaging application ever!')
            return userName
        elif recvMsg == 'Login Blocked':
            print('Your account is blocked due to multiple login failures. Please try again later')
            return None
        elif recvMsg == 'Login Failed':
            print('Invalid Password. Please try again')
            # 2nd try
            psw = input('Password: ')
            clientSocket.sendall(psw.encode())
            recvMsg = clientSocket.recv(1024).decode()
            if recvMsg == 'Login Success':
                print('Welcome to the greatest messaging application ever!')
                return userName
            elif recvMsg == 'Login Blocked':
                print('Your account is blocked due to multiple login failures. Please try again later')
                return None
            elif recvMsg == 'Login Failed':
                print('Invalid Password. Please try again')
                # 3rd try   
                psw = input('Password: ')
                clientSocket.sendall(psw.encode())
                recvMsg = clientSocket.recv(1024).decode()
                if recvMsg == 'Login Success':
                    print('Welcome to the greatest messaging application ever!')
                    return userName
                elif recvMsg == 'Login Blocked':
                    print('Your account is blocked due to multiple login failures. Please try again later')
                    return None
                elif recvMsg == 'Login Failed':    
                    print('Invalid Password. Your account has been blocked. Please try again later')
    return None

def sendingCmd(clientSocket, user):
    while True:
        usrInput = input()
        
        try:
            command = re.search(r'^([^ ]+)', usrInput).group(1)
        except AttributeError:
            print('Error. Usage: Command')
            continue
        
        if command == 'message':
            try:
                re.search(r'^message ([^ ]+) (.+)$', usrInput).group(1)
                re.search(r'^message ([^ ]+) (.+)$', usrInput).group(2)
                clientSocket.sendall(usrInput.encode())
            except AttributeError:
                print('Error. Usage: message <user> <message>')
        
        elif command == 'broadcast':
            try:
                re.search(r'^broadcast (.+)$', usrInput).group(1)
                clientSocket.sendall(usrInput.encode())
            except AttributeError:
                print('Error. Usage: broadcast <message>')    
        
        elif command == 'whoelse':
            clientSocket.sendall(command.encode())
                
        elif command == 'whoelsesince':
            try:
                re.search(r'^whoelsesince (\d+)$', usrInput).group(1)
                clientSocket.sendall(usrInput.encode())
            except AttributeError:
                print('Error. Usage: whoelsesince <time(s)>')
        
        elif command == 'block':
            name = usrInput[6:]
            if name == user:
                print('Error. Cannot block self')
            else:
                clientSocket.sendall(usrInput.encode())
                
        elif command == 'unblock':
            name = usrInput[8:]
            if name == user:
                print('Error. Cannot unblock self')
            else:
                clientSocket.sendall(usrInput.encode())
                 
        elif command == 'logout':
            clientSocket.sendall(command.encode())
            clientSocket.close()        
            exit()
        
        elif command == 'read':
            clientSocket.sendall(command.encode())

        else:
            print('Error. Invalid command')
            
def receivingResp(clientSocket):
    while True:
        try:
            recvMsg = clientSocket.recv(1024).decode()
            if recvMsg:
                print(recvMsg)
        except:
             break       
            
             
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("\n===== Usage: python3 Client.py server_port ======\n");
        exit(0);
    
    serverPort = int(sys.argv[1])
    serverAddr = ('localhost', serverPort)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(serverAddr)
    print(f'Connected to server at {serverAddr}')

    user = login(clientSocket)
    if user:
        l = threading.Thread(target=receivingResp, args=[clientSocket])
        l.start()

        print("===== Please type command you want to send to server: =====")
        sendingCmd(clientSocket, user)
        
