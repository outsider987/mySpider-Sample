from ftplib import FTP
import os


def ftpconnect(host, username, password):
    # ftp = FTP('156.67.222.57')
    # ftp.login(user='u565698326.topceo.online', passwd='T5204t5204')
    ftp = FTP(host)
    ftp.login(username, password)
    # ftp.set_debuglevel(1)
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


def uploadftpfile(ftp, fpLocal, path_name, image_name):
    print("upload file path:" + ftp.pwd())
    ftp.cwd("comics")
    if path_name in ftp.nlst():
        ftp.cwd(path_name)
    else:
        ftp.mkd(path_name)
        ftp.cwd(path_name)
    if image_name in ftp.nlst():
        fpLocal.close()
        os.remove(fpLocal.name)
        print("upload file path:" + ftp.pwd())
        ftp.close()
        return False
    print(ftp.pwd())
   
    # fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + image_name, fpLocal)  # 上传文件
    fpLocal.close()
    # os.remove(fpLocal.name) 
    ftp.set_debuglevel(0)
    ftp.close()
    return True
# uploadfile(ftpconnect('156.67.222.57', 'u565698326.topceo.online', 'T5204t5204'), "", "https://cdn-msp.msp-comic1.xyz/media/albums/229854.jpg?v=1619346279")
# print(ftp.cwd("folderOne"))
# print(ftp.pwd())

# change path 

# ftp.quit()
# ftp.close()
