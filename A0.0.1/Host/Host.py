import socket
import os
s=socket.socket()
name=socket.gethostbyname(socket.gethostname())
print(name)
port=1024
s.bind((name,port))
s.listen(10)
while True:
    c,addr=s.accept()
    print("INFO:Got connection from",addr)
    cmd=c.recv(1024).decode()
    print("INFO:Command:",cmd)
    cmd=cmd.split(" ")
    if cmd[0]=='list':
        f=open(os.getcwd()+"\\serverfile\\flist.txt","r")
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
            f=open(os.getcwd()+"\\serverfile\\flist.txt","r")
            content=list(f)
            content.remove(cmd[1]+'\n')
            f.close()
            f=open(os.getcwd()+"\\serverfile\\flist.txt","w")
            f.write(content)
            f.close()
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
                    if size==0:
                        break
                    outp=c.recv(8192)
                    if outp:
                        break
                f.write(outp)
                size-=len(outp)
                print(round(size/allsize*100,2),"%","left")
            f.close()
            f=open(os.getcwd()+"\\serverfile\\flist.txt","r")
            content="".join(list(f)+[cmd[1]+'\n'])
            f.close()
            f=open(os.getcwd()+"\\serverfile\\flist.txt","w")
            f.write(content)
            f.close()   
        else:
            print("INFO:Error:FilenameRepeated")
            c.send(b"#FR")
            f.close()
        
    elif cmd[0]=='download':
        try:
            f=open(cmd[1],'rb')
        except:
            c.send(b'#NLL')
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
                print(round(size/allsize*100,2),"%","left")
            f.close()
    print("INFO:Connection off with",addr)
    c.close()
