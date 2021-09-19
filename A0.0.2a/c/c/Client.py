import time
import socket
import os
import datetime
f=open(os.getcwd()+'\\clientfile\\entryani.txt','r',encoding='utf-8')
print(f.read())
f.close()
cfigf=open(os.getcwd()+'\\clientfile\\config.txt','r',encoding='utf-8')
contents=list(cfigf)
cmds=contents[0].split(':')[1][:-1].split(',')
noti=contents[1].split(':')[1][:-1].split(',')
cfigf.close()
loginstate=0
while True:
    s=socket.socket()
    while True:
        cmd=input('>>')
        if cmd.strip():
            cmd=cmd.split(' ')
            break
    if cmd[0] not in cmds:
        print(cmd[0],noti[0])
        continue
    else:
        if cmd[0] in cmds[:6]:
            if len(cmd)!=1:
                print(noti[1])
                continue
        elif cmd[0] in cmds[6:9]:
            if len(cmd)!=2:
                print(noti[2])
                continue
            elif cmd[0]==cmds[6]:
                try: f=open(cmd[1],'rb')
                except:
                    print(noti[3])
                    continue
    if cmd[0]=='quit':
        f=open(os.getcwd()+'\\clientfile\\exitani.txt','r',encoding='utf-8')
        print(f.read())
        f.close()
        time.sleep(2.0)
        exit(0)
    elif cmd[0]=='help':
        f=open(os.getcwd()+'\\clientfile\\helplog.txt','r',encoding='utf-8')
        print(f.read())
        f.close()
    elif cmd[0]=='login':
        name=cmd[1]
        try: s.connect((name,1024))
        except BaseException as E: print(E,'\n',noti[4])
        else:
            s.send(b'Connection Success')
            print(noti[5],name,noti[6])
            s.close()
            loginstate=1
    elif cmd[0]=='logout':
        name=''
        loginstate=0
        print()
    elif cmd[0]=='history':
        f=open(os.getcwd()+'\\clientfile\\hosts.txt','r',encoding='utf-8')
        print(f.read())
        f.close()
    elif cmd[0]=='clshis':
        f=open(os.getcwd()+'\\clientfile\\hosts.txt','w',encoding='utf-8')
        f.write('Hosts:\n')
        f.close()
    else:
        if loginstate==0:
            print(noti[7])
            continue
        s=socket.socket()
        s.connect((name,1024))
        s.send(' '.join(cmd).encode()+b' 0.0.2a')
        while True:
            state=s.recv(1024)
            if state: break
        f1=open(os.getcwd()+'\\clientfile\\hosts.txt','r',encoding='utf-8')
        contents=f1.read()
        f1.close()
        f1=open(os.getcwd()+'\\clientfile\\hosts.txt','w',encoding='utf-8')
        f1.write(contents+name+'  '+state.split()[1].decode()+'\n')
        f1.close()
        if cmd[0]=='list':
            while True:
                size=s.recv(1024)
                if size: break
            size=int(size)
            while True:
                if size==0: break
                s.send(b'n')
                while True:
                    outp=s.recv(1024)
                    if outp: break
                print(outp.decode()[:-1])
                size-=1
        elif cmd[0]=='del':
            while True:
                state=s.recv(1024)
                if state: break
            if state==b'FNF': print(noti[8])
            else: print(noti[9]+cmd[1]+'。')
        elif cmd[0]=='upload':
            while True:
                state=s.recv(1024)
                if state: break
            if state!=b'#FR':
                d0=datetime.datetime.now()
                d=datetime.datetime.now()
                size=allsize=os.path.getsize(cmd[1])
                donesize=0
                s.send(str(size).encode())
                while True:
                    if size==0: break
                    while True:
                        inpt=s.recv(1024)
                        if inpt==b'n': break
                    if size>=4096: outp=f.read(4096)
                    else: outp=f.read()
                    s.send(outp)
                    size-=len(outp)
                    donesize+=len(outp)
                    if (datetime.datetime.now()-d).total_seconds()>=1:
                        d=datetime.datetime.now()
                        os.system('CLS')
                        print(round(donesize/1024/(d-d0).total_seconds(),2),'KB/s         ',donesize/allsize*100,'%')
                f.close()
            else: print(noti[10])
        elif cmd[0]=='download':
            d0=datetime.datetime.now()
            d=datetime.datetime.now()
            while True:     
                state=s.recv(1024)
                if state: break
            if state!=b'#NLL':
                size=allsize=int(state[3:])
                donesize=0
                f=open(cmd[1],'wb')
                while True:
                    s.send(b'n')
                    while True:
                        outp=s.recv(8192)
                        if outp: break
                    f.write(outp)
                    size-=len(outp)
                    donesize+=len(outp)
                    if (datetime.datetime.now()-d).total_seconds()>=1:
                        d=datetime.datetime.now()
                        os.system('CLS')
                        print(round(donesize/1024/(d-d0).total_seconds(),2),'KB/s         ',donesize/allsize*100,'%')
                    if size==0: break
                f.close()
            else: print(noti[8])
        s.close()
