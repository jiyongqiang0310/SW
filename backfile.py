#!/usr/bin/env python

import paramiko
import os
import threading
import time

class BackUp(threading.Thread):
    def __init__(self,threadID,server,username,password):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.server = server
        self.username = username
        self.password = password

    def run(self):
        backupdir = r'/NetBackConfig'
        sftp = self.conn()
        serdir = sftp.listdir(path='.')
        ctime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        if 'startup.cfg' in serdir:
            serpath = r'startup.cfg'
            clipath = backupdir+os.sep+ctime+self.server+'startup.cfg'
        elif 'config.cfg' in serdir:
            serpath = r'config.cfg'
            clipath = backupdir+os.sep+ctime+self.server+'config.cfg'
        else:
            serpath = r'/config/juniper.conf.gz'
            clipath = backupdir+os.sep+ctime+self.server+'juniper.conf.gz'
        sftp.get(serpath, clipath)
        sftp.close()

    def conn(self):
        client = paramiko.Transport((self.server, 22))
        client.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(client)
        return sftp

def backupconf(serverlist,username,passwd):
    for server in serverlist:
        mybackup = BackUp(serverlist.index(server),server,username,passwd)
        mybackup.start()

if __name__ == '__main__':
    serverlist = ['ip1','ip2','ip3','ipn']
    username = ''
    passwd = ''
    try:
        backupconf(serverlist,username,passwd)
    except:
        print('faild')
    else:
        print('ok')

