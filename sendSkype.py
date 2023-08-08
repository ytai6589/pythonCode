from skpy import Skype
from skpy import SkypeAuthException
from skpy import SkypeConnection
import os, sys, setting 
import getopt

ProcName = 'sendSkype.py'
Version = '1.1'
Synopsis = '-u <username> -p <password> -g <groupID> -m <message>'


def login(username, password, token_file='.tokens-app'):
    "Login to Skype"
    sk = Skype(connect=False)
    sk.conn.setTokenFile(token_file)
    try:
        sk.conn.readToken()
    except SkypeAuthException:
        # Prompt the user for their credentials.
        if os.getenv("SKPY_DEBUG_HTTP"):
            print("==*> RESET USER TOKEN")
        sk.conn.setUserPwd(username, password)
        sk.conn.getSkypeToken()

    return sk


def post_message(sk, group_id, msg):
    "Post a message to a given channel"
    result_flag = False
    try:
        sk.conn.verifyToken(SkypeConnection.Auth.SkypeToken)
        channel = sk.chats[group_id]
        channel.sendMsg(msg)
        result_flag = True
        print("==*> SKPY SEND SUCCESS")
    except Exception as e:
        print("==*> SKPY SEND FAILED,", e)

    return result_flag


def main(argv):
    userName = ''
    userPwd = ''
    groupID = ''
    sendMsg = ''
   
    try:
        opts, args = getopt.gnu_getopt(argv, 'u:p:m:g:hv')
    except getopt.GetoptError:
        print (f'{ProcName} {Synopsis}')
        sys.exit(2)
   
    for opt, arg in opts:      
        if opt == '-h':
            print (f'{ProcName} {Synopsis}')
            sys.exit()
        elif opt in ("-v"):
            print (f'Version is {Version}')
            sys.exit()
        elif opt in ("-u"):
            userName = arg
        elif opt in ("-p"):
            userPwd = arg
        elif opt in ("-g"):
            groupID = arg
        elif opt in ("-m"):
            sendMsg = arg

    print("==*> SKPY_DEBUG_HTTP =", os.getenv("SKPY_DEBUG_HTTP"))

    if os.getenv("SKPY_DEBUG_HTTP"):
        print("==*> SKPY CONNECT")
    sk = login(userName, userPwd)

    if os.getenv("SKPY_DEBUG_HTTP"):
        print("==*> SKPY SEND MESSAGE")
    post_message(sk, groupID, sendMsg)
        
        
if __name__ == "__main__":
   main(sys.argv[1:])