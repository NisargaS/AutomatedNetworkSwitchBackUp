# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 10:49:55 2020
tkinter with only functions
@author: nisarga
"""
from threading import Thread as  process
import tkinter as tk 
import tkinter.messagebox as msg
import time
import paramiko 
import os
import datetime


ips =[]
val =[]
ipaddresslist =[]
index = 0


def search():
    
    if len(user.get()) == 0 and len(pasword.get()) == 0 and len(path.get()) == 0 and len(filename.get()) ==0 :
        msg.showinfo("Warning!", "All fields are mandatory, Please fill everything")
    elif len(user.get()) != 0 and len(pasword.get()) == 0 and len(path.get()) == 0 and len(filename.get()) ==0:
        msg.showinfo("Warning!", "Please enter password, output file destination path and input file name")
    elif len(user.get()) != 0 and len(pasword.get()) != 0 and len(path.get()) == 0 and len(filename.get()) ==0:
        msg.showinfo("Warning!", "Please enter output file destination path and input file name")
    elif len(user.get()) != 0 and len(pasword.get()) != 0 and len(path.get())!= 0 and len(filename.get()) ==0:
        msg.showinfo("Warning!","Please enter the input filename")
    else:
        showbtn.config(state = 'disabled')
        user.config(state = 'disabled')
        pasword.config(state='disabled')
        path.config(state='disabled')
        filename.config(state='disabled')
        Displaymes.configure(text = "Backup Started")
        ipaddresslist = preprocess(filename_prefix = path.get() + "\\",username = user.get()  ,passwd = pasword.get() )
        for ip in ipaddresslist:
            if(ipaddresslist[len(ipaddresslist)-1] == ip):
                val[3] = 1
            else:
                val[3] = 0
            sshconnection(ip,val)#threading.Thread(target= sshconnection,()).start()
        msg.showinfo("Info", "Backup of listed switches are completed!")
        #time.sleep(1) # added this because to avoid Runtime Error: main thread is not in main loop
        root.destroy()
            
            
def preprocess(filename_prefix,username,passwd):
    if(os.path.isdir(filename_prefix) and os.path.isfile(filename.get())):
        ips.clear()
        with open(filename.get()) as file:
            for ip in file:
                ip = ip.strip()
                ips.append(ip)
            #print(ips)
            val.append(filename_prefix)
            val.append(username)
            val.append(passwd)
            val.append(index)
        return ips
    else:
        msg.showinfo("Warning!", "Directory or File doesnot exists, please create it and try again later")
        
        
        
def sshconnection(ipadd,otherdetails):
    now = datetime.datetime.now()
    extension = "txt"
    port=22
    ssh = paramiko.SSHClient() # Initialise SSH Client
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Add SSH host key automatically if nedded
    try:
        ssh.connect(ipadd,port, otherdetails[1],otherdetails[2], look_for_keys=False) #Connect to router using username/password authentication not with key authentication
    except:
        msg.showinfo("Warning!", "Invalid username or password")
    try:    #print("Invalid username or password")
        chan = ssh.invoke_shell() # Method invoke_shell(): allows to set an interactive SSH session with server
        time.sleep(2)
        chan.send('term len 0\n')  # Method send : sends specified string to session and returns amount of sent bytes
        # 'term len 0\n' clear the terminal screen in a Cisco router/ switch                                                                           
        time.sleep(1)
    except:
        msg.showinfo("Warning!", "Connection failed!")
    try:
        chan.send('show run|in hostname\n')  # command used to get the host name of the cisco switch/router
        dev_name=chan.recv(1024) # Method receive : receives data from session. In parentheses, the maximum value in bytes that can be obtained is indicated.
        contentlist = dev_name.decode("utf-8").split("\r\n")
        hostname = contentlist.pop()
        hostname = hostname.replace("#","").strip() # bug fix, removing a empty space from the host name
        Displaymes.configure(text = f"Swicth_Name:{hostname}")
        SecondDisplaymsg.configure(text ="" )#['text']=f"Swicth_Name:{hostname}" #config(root,text = f"Swicth_Name:{hostname}")
        chan.send('sh run\n') # sh run determine the current status of a router, because it displays the active configuration file running in RAM.
        time.sleep(20)
        output = chan.recv(999999)
        print(hostname)
        print(otherdetails[0])
        filename = "%s_%.2i%.2i%i_%.2i%.2i%.2i.%s" % (hostname,now.year,now.month,now.day,now.hour,now.minute,now.second,extension)
        #print(otherdetails[0].append(filename))
        f1 = open((otherdetails[0]+filename),'a')
        f1.write(output.decode("utf-8") )
        f1.close()
        ssh.close()
        SecondDisplaymsg.configure(text =f"Backup of Switch {hostname} Completed" )#['text'] = f"Backup of Switch {hostname} Completed" #(text = f"Backup of Switch {hostname} Completed")
        #if(val[3]==1):
            #msg.showinfo("Info", "Backup of listed switches are completed!")
            #time.sleep(1) # added this because to avoid Runtime Error: main thread is not in main loop
            #root.destroy()
    except:
        msg.showinfo("Error!!!", "Unexpected Error,please try again later")
    
root = tk.Tk()
root.geometry("400x250")
root.title("Switch Backup")        
#frame = tk.Frame()
tk.Label(root, text="Enter username:").grid(row=0)
tk.Label(root, text="Enter Paswd:").grid(row=1)
tk.Label(root, text="Enter destination filepath for storing the files:").grid(row=2)
tk.Label(root, text="Iplist file name").grid(row=3)
Displaymes = tk.Label(root, text= "Initialised")
Displaymes.grid(row=7)
SecondDisplaymsg = tk.Label(root, text= "")
SecondDisplaymsg.grid(row=9)
user = tk.Entry(root)#tk.simpledialog.askstring("Name","Enter username")#input("Enter username:")
pasword = tk.Entry(root, show='*')
path = tk.Entry(root)
filename = tk.Entry(root)
user.grid(row=0, column=1)
pasword.grid(row=1, column=1)
path.grid(row=2, column=1)
filename.grid(row=3,column=1)
quitbtn = tk.Button(root, text='Quit', command=root.destroy)
quitbtn.grid(row=5, column=0, sticky=tk.W, pady=10)
showbtn = tk.Button(root, text='Start', command= lambda: process(target=search).start()) #,kwargs=dict(u=user.get(),ps=pasword.get(),pa=path.get())
showbtn.grid(row=5, column=1, sticky=tk.W, pady=10)
root.mainloop()

