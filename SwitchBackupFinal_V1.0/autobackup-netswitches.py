# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:13:02 2020

@author: nisarga
"""
import sys
import time
import paramiko 
import os
import re
import datetime

now = datetime.datetime.now()
user = input("Enter username:")
password = input("Enter Paswd:")
filepath = input("Enter destination filepath for storing the files:")
port=22
f0 = open('iplist.txt')
extension = "txt"
for ip in f0.readlines():
       ip = ip.strip()
       filename_prefix = filepath + ip 
       ssh = paramiko.SSHClient()
       ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       ssh.connect(ip,port, user, password, look_for_keys=False)
       chan = ssh.invoke_shell()
       time.sleep(2)
       chan.send('term len 0\n')
       time.sleep(1)
       chan.send('sh run\n')
       time.sleep(20)
       output = chan.recv(999999)
       '''dev_name=chan.send('show run|in hostname')
       hname=re.search(r'hostname\s+(\w+)',dev_name)
       hostname=hname.group(1)'''
       filename = "%s_%.2i%.2i%i_%.2i%.2i%.2i.%s" % (ip,now.year,now.month,now.day,now.hour,now.minute,now.second,extension)
       f1 = open(filename, 'a')
       f1.write(output.decode("utf-8") )
       f1.close()
       ssh.close() 
       f0.close()

