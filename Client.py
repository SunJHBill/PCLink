import time
import socket
import os
import datetime
command=['list','upload','download','quit','del','login','logout']
s=socket.socket()
loginstate=0
while True:
    while True:
        cmd=input('>>')
        if cmd.strip():
            cmd=cmd.split(' ')
            break
    if cmd[0] not in command:
        print('Error:Invalid command')
        continue
    else:
        if cmd[0]=='list' or cmd[0]=='quit' or cmd[0]=='logout':
            if len(cmd)!=1:
                print('Error:list,quit and logout don\'t need any arguments!')
                continue
        elif cmd[0]=='upload' or cmd[0]=='download' or cmd[0]=='login':
            if len(cmd)!=2:
                print('Error:upload,download and login need and only need one argument!')
                continue
            elif cmd[0]=='upload':
                try:
                    f=open(cmd[1],'rb')
                except:
                    print('File not found!The file needed to be transported should be pout under the same directory with the client!')
                    continue
    if cmd[0]=='quit':
        print(
        '''
        ╭──╮╭──╮╭──╮┌──╮╭──╮╭╮╭╮╭──╮
       │╭─╯│╭╮││╭╮│ │╭╮││╭╮││╰╯││╭─╯
       ││╭╮││││││││ │││││╰╯╯╰╮╭╯│╰─╮
       ││││││││││││ │││││╭╮╮　││　│╭─╯
       │╰╯││╰╯││╰╯│ │╰╯││╰╯│　││　│╰─╮
       ╰──╯╰──╯╰──╯ └──╯╰──╯　╰╯　╰──╯
        '''
        )
        time.sleep(2.0)
        exit(0)
    elif cmd[0]=='login':
        name=cmd[1]
        try:
            s.connect((name,1024))
        except:
            print('Invalid host name.Try again.')
        else:
            s.close()
            loginstate=1
    elif cmd[0]=='logout':
        name=''
        loginstate=0
    else:
        if loginstate==0:
            print('You haven\'t log in to any host!')
            continue
        s=socket.socket()
        s.connect((name,1024))
        s.send(' '.join(cmd).encode()+b' A0.0.1')
        
        if cmd[0]=='list':
            while True:
                size=s.recv(1024)
                if size:
                    break
            size=int(size)
            while True:
                if size==0:
                    break
                s.send(b'n')
                while True:
                    outp=s.recv(1024)
                    if outp:
                        break
                print(outp.decode()[:-1])
                size-=1
                ###
        elif cmd[0]=='del':
            while True:
                state=s.recv(1024)
                if state:
                    break
            if state==b'FNF':
                print('File not found.You can type list to check.')
            else:
                print(cmd[1],'have been deleted.')
        elif cmd[0]=='upload':
            while True:
                state=s.recv(1024)
                if state:
                    break
            if state!=b'#FR':
                d0=datetime.datetime.now()
                d=datetime.datetime.now()
                size=allsize=os.path.getsize(cmd[1])
                donesize=0
                s.send(str(size).encode())
                while True:
                    if size==0:
                        break
                    while True:
                        inpt=s.recv(1024)
                        if inpt==b'n':
                            break
                    if size>=4096:
                        outp=f.read(4096)
                    else:
                        outp=f.read()
                    s.send(outp)
                    size-=len(outp)
                    donesize+=len(outp)
                    if (datetime.datetime.now()-d).total_seconds()>=1:
                        d=datetime.datetime.now()
                        os.system('CLS')
                        print(round(donesize/1024/(d-d0).total_seconds(),2),'KB/s         ',donesize/allsize*100,'%')
                f.close()
            else:
                print('File name repeated.You can enter list to check.')
        elif cmd[0]=='download':
            d0=datetime.datetime.now()
            d=datetime.datetime.now()
            while True:     
                state=s.recv(1024)
                if state:
                    break
            if state!=b'#NLL':
                size=allsize=int(state[3:])
                donesize=0
                f=open(cmd[1],'wb')
                while True:
                    if size==0:
                        break
                    s.send(b'n')
                    while True:
                        outp=s.recv(8192)
                        if outp:
                            break
                    f.write(outp)
                    size-=len(outp)
                    donesize+=len(outp)
                    if (datetime.datetime.now()-d).total_seconds()>=1:
                        d=datetime.datetime.now()
                        os.system('CLS')
                        print(round(donesize/1024/(d-d0).total_seconds(),2),'KB/s         ',donesize/allsize*100,'%')
                f.close()
            else:
                print('File not found.You can type list to check.')
        s.close()
