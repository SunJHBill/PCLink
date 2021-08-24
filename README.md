# Luo
This programme aims to realizing fast and convenient file transportation between different computers.Server building is also allowed,but based on the principle of freedom and opening.

![Image of the logo](https://cdn.luogu.com.cn/upload/image_hosting/kv6v67zi.png)

This is the present design of the logo.If possible,you can offer yours.**P.S.Don't deliver by email!Just send the link by commenting.**

##Version Discription A0.0.1

Protocol A is come up with last year,but it wasn't transformed into reality till now.The network runs like this:

- First,the host establishes the connection and receives the command from the client.
- Second,the host finish the task according to the command.
 
 For the commands **download** and **upload**:
 
 - The host tries to open the file needed.If not found,the request will be refused(download).The host tries to open the file mentioned in the command,to check if the filename contradicts.If do,the request will be refused.
 - After these checks,the host and the client exchanges critical information(The size of the file).
 - Transportation begins.The side receiving data will send the other side a request byte.When the sender receives thr byte,it will send off the data and wait for the next turn.
 - In uploading process,the host will update the file list. 
 
 For the command **list**:
 
 The process is just host sending list.txt to the client.
 
 For the command **del**: yet to update.Time is limited.
 
 Such structure makes it simple to build up an inner network.But about public service......I haven't consider it,though.
 After some torturing time,I finally got to login Github,and I spend quite a long time understanding the functions because my English vocabulary on IT is poor.**Support is welcome!Protocol B and C is on the way.**
 
 **The version A0.0.1 will be released on 2021-8-24 10:00(Beijing Time).A0.0.0 is once on the schedule,but it's unusable and now abandoned.**
