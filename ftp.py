from ftplib import FTP
import os

# here you need input your information
def ftpconnect(host, username, password):
    ftp = FTP('your ip ')
    ftp.login(user='username', passwd='password')
    ftp = FTP(host)
    ftp.login(username, password)
    return ftp


def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR  ' + remotepath, fp.write, bufsize)
    # 接受服务器上文件并写入文本
    ftp.set_debuglevel(0)  # 关闭调试
    fp.close()  # 关闭文件


def uploadfile(ftp, remotepath, localpath):
    # ftp.mkd('comics')
    ftp.cwd("comics")

    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ', fp, bufsize)  # 上传文件
    ftp.set_debuglevel(0)
    fp.close()




