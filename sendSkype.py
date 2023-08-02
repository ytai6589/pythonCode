from skpy import Skype
import sys, getopt

ProcName = 'sendSkype.py'
Version = '1.0'
Synopsis = '-u <username> -p <password> -g <groupID> -m <message>'

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

    sk = Skype(userName, userPwd)
    ch = sk.chats[groupID]
    ch.sendMsg(sendMsg)

if __name__ == "__main__":
   main(sys.argv[1:])