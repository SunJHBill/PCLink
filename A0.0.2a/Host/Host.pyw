import socket
import os
import datetime
import traceback
s=socket.socket()
f0=open(os.getcwd()+'\\logging\\logging.txt','w',encoding='utf-8')
name=socket.gethostbyname(socket.gethostname())
f0.write(name+'\n')
port=1024
s.bind((name,port))
s.listen(10)
f0.close()
while True:
    try:
        f0=open(os.getcwd()+'\\logging\\logging.txt','a+',encoding='utf-8')
        c,addr=s.accept()
        d0=datetime.datetime.now()
        f0.write("INFO:Got connection from"+str(addr)+'\n')
        while True:
            cmd=c.recv(1024).decode()
            if cmd: break
        c.send((name+' '+str(datetime.datetime.now())).encode())
        f0.write("INFO:Command:"+cmd+'\n')
        cmd=cmd.split(" ")
        if cmd[0]=='list':
            f=open(os.getcwd()+"\\serverfile\\flist.txt","r",encoding='utf-8')
            lst=list(f)
            size=len(lst)
            c.send(str(len(lst)).encode())
            while lst:
                while True:
                    inpt=c.recv(1024)
                    if inpt==b'n':
                        break
                c.send(lst.pop(0).encode())
            c.send(b'E')
            f.close()
        elif cmd[0]=='del':
            try:
                f=open(cmd[1],"rb")
            except:
                c.send(b'FNF')
            else:
                f.close()
                os.remove(cmd[1])
                f=open(os.getcwd()+"\\serverfile\\flist.txt","r",encoding='utf-8')
                content=list(f)
                content.remove(cmd[1])
                content="".join(content)
                f.close()
                f=open(os.getcwd()+"\\serverfile\\flist.txt","w",encoding='utf-8')
                f.write(content)
                f.close()
                c.send(b'OK')
        elif cmd[0]=='upload':
            try:
                f=open(cmd[1],"rb")
            except:
                c.send("#OK".encode())
                f=open(cmd[1],'wb')
                while True:
                    size=c.recv(1024)
                    if size:
                        break
                size=allsize=int(size)
                while True:
                    c.send(b'n')
                    while True:
                        outp=c.recv(8192)
                        if outp:
                            break
                    f.write(outp)
                    size-=len(outp)
                    if size==0:
                        break
                f.close()
                f=open(os.getcwd()+"\\serverfile\\flist.txt","r",encoding='utf-8')
                content="".join(list(f)+[cmd[1]+'\n'])
                f.close()
                f=open(os.getcwd()+"\\serverfile\\flist.txt","w",encoding='utf-8')
                f.write(content)
                f.close()
                
            else:
                f0.write("INFO:Error:FilenameRepeated\n")
                c.send(b"#FR")
                f.close()       
        elif cmd[0]=='download':
            try:
                f=open(cmd[1],'rb')
            except:
                c.send(b'#NLL')
                f0.write("INFO:Error:Filenotfound\n")
            else:
                size=allsize=os.path.getsize(cmd[1])
                c.send(b'#OK'+str(size).encode())
                while True:
                    if size==0:
                        break
                    while True:
                        inpt=c.recv(1024)
                        if inpt==b'n':
                            break
                    if size>=4096:
                        outp=f.read(4096)
                    else:
                        outp=f.read()
                    c.send(outp)
                    size-=len(outp)
                f.close()
        f0.write("INFO:Connection off with"+str(addr)+'\n')
        f0.write('Done in'+str((datetime.datetime.now()-d0).total_seconds())+'\n')
        f0.close()
        c.close()
    except BaseException as E:
        f0.write('A deadly exception handled\n'+traceback.format_exc())
        f0.close()
        break
