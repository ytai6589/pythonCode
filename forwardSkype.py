from skpy import Skype
from skpy import SkypeAuthException
from skpy import SkypeConnection
import os, sys, getopt
import pytz, json
from datetime import datetime

ProcName = 'forwardSkype.py'
Version = '1.0'
Synopsis = '-u <username> -p <password> -f <groupID> -t <groupID>'

def login(username, password, token_file='.tokens-app'):
    sk = Skype(connect=False)
    sk.conn.setTokenFile(token_file)
    try:
        sk.conn.readToken()
    except SkypeAuthException:
        sk.conn.setUserPwd(username, password)
        sk.conn.getSkypeToken()
        
    return sk

def post_message(sk, group_id, msg):
    result_flag = False
    try:
        sk.conn.verifyToken(SkypeConnection.Auth.SkypeToken)
        chat_channel = sk.chats[group_id]
        chat_channel.sendMsg(msg)
        result_flag = True
        print('==*> SKPY SEND SUCCESS')
    except Exception as e:
        print('==*> SKPY SEND FAILED,', e)
        
    return result_flag
    
def forword_message(sk, group_id, forword_msg, msg_raw):
    result_flag = False
    try:
        sk.conn.verifyToken(SkypeConnection.Auth.SkypeToken)
        chat_channel = sk.chats[group_id]
        chat_channel.sendMsg(forword_msg)
        chat_channel.sendRaw(editid=msg_raw.id, messagetype='RichText', content=msg_raw.content)
        result_flag = True
        print('==*> SKPY SEND SUCCESS')
    except Exception as e:
        print('==*> SKPY SEND FAILED,', e)
        
    return result_flag
    
def get_message(sk, group_id):
    msg_lst = []
    try:
        sk.conn.verifyToken(SkypeConnection.Auth.SkypeToken)
        chat_channel = sk.chats[group_id]
        msg_lst = chat_channel.getMsgs()
        print('==*> SKPY Get SUCCESS')
    except Exception as e:
        print('==*> SKPY Get FAILED,', e)
        
    return msg_lst
    
def get_userName(sk, user_id):
    sk.conn.verifyToken(SkypeConnection.Auth.SkypeToken)
    
    return str(sk.contacts.user(user_id).name)

def read_lstTime(token_file='.tokens-lstTime'):
    date_str = ''
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            date_str = f.read()
        date_str = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')

    return date_str
        
def write_lstTime(content, token_file='.tokens-lstTime'):
    with os.fdopen(os.open(token_file, os.O_WRONLY | os.O_CREAT, 0o600), 'w') as f:
        f.truncate()
        f.write(str(content))
        
def read_usrInfo(token_file='.tokens-usrInfo'):
    str = ''
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            str = f.read()
    
    if not str:
        return {}
    else:
        return json.loads(str)
        
def write_usrInfo(usr_dic, token_file='.tokens-usrInfo'):
    with os.fdopen(os.open(token_file, os.O_WRONLY | os.O_CREAT, 0o600), 'w') as f:
        f.truncate()
        f.write(json.dumps(usr_dic) + "\n")
  
def UTCtoLocalTime(convertTime):
    utc = pytz.timezone('UTC')
    utctime = utc.localize(convertTime)
    localtz = pytz.timezone('Asia/Taipei')
    localtime = localtz.normalize(utctime.astimezone(localtz))
    
    return localtime.strftime('%Y-%m-%d %H:%M:%S')

def main(argv):
    usr_name = ''
    usr_pwd = ''
    from_gId = ''
    to_gId = ''
   
    try:
        opts, args = getopt.gnu_getopt(argv, 'u:p:f:t:hv')
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
            usr_name = arg
        elif opt in ("-p"):
            usr_pwd = arg
        elif opt in ("-f"):
            from_gId = arg
        elif opt in ("-t"):
            to_gId = arg

    if not usr_name or not usr_pwd or not from_gId or not to_gId:
        print (f'{ProcName} {Synopsis}')
        sys.exit(2)

    lstTime = read_lstTime()
    usr_dic = read_usrInfo()

    sk = login(usr_name, usr_pwd)
    msg_lst = get_message(sk, from_gId)

    for msg_raw in sorted(msg_lst, key=lambda x: x.time, reverse=False):
        if lstTime == '':
            lstTime = msg_raw.time
            
        if msg_raw.time > lstTime:
            if msg_raw.content:
                if not usr_dic.get(msg_raw.userId):
                    usr_dic[msg_raw.userId] = get_userName(sk, msg_raw.userId)
                forword_msg = f"{UTCtoLocalTime(msg_raw.time)} - {usr_dic.get(msg_raw.userId)}:"
                forword_message(sk, to_gId, forword_msg, msg_raw)
            write_lstTime(msg_raw.time)
    
    write_usrInfo(usr_dic)

if __name__ == '__main__':
    main(sys.argv[1:])
