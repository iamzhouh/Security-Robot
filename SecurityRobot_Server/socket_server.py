import socket
import os
import datetime
import shutil

server = socket.socket()  # 1.声明协议类型，同时生成socket链接对象
server.bind(('', 12000))  # 绑定要监听端口=(服务器的ip地址+任意一个端口)
server.listen(5)  # 监听

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获得当前目录

print("waitting connection...")
while True:
    conn, addr = server.accept()
    print("收到来自{}请求".format(addr))
    while True:
        data = conn.recv(1024)  # 接收客户端的内容

        if len(str(data,'utf-8').split('|')) == 3:
            filepath,filename, filesize = str(data,'utf-8').split('|')  # 获得指定图像的名称，图像大小
            path = os.path.join(BASE_DIR+'/'+filepath, filename)  # 指定图像的保存路径
            # print(BASE_DIR+'/'+filepath)

            data = str(datetime.datetime.now().strftime('%Y-%m-%d'))  # 获取当前的日期
            year,month,day = data.split('-')[0],data.split('-')[1],data.split('-')[2]
            # print(year,month,day)
            for root, dirs, files in os.walk('FaceDetection_Img/'):
                # print(dirs)
            # 当前目录路径,当前路径下所有子目录,当前路径下所有非目录子文件
                for dir in dirs:
                    pre_year,pre_month,pre_day = dir.split('-')[0],dir.split('-')[1],dir.split('-')[2]
                    if (int(pre_year) < int(year)) | (int(pre_month) < int(month)) | (int(pre_day)+3 < int(day)):
                        shutil.rmtree('FaceDetection_Img/' + dir)
                        print('remove dir')

           
            if not os.path.exists(BASE_DIR+'/'+filepath):   
                os.makedirs(BASE_DIR+'/'+filepath)

            filesize = int(filesize)  # 图像大小转换成整形

            f = open(path, 'ab')  # 以二进制格式打开一个文件用于追加。如果该文件不存在，创建新文件进行写入。
            has_receive = 0  # 统计接收到的字节数
            while has_receive != filesize:
                data1 = conn.recv(1024)  # 一次从服务端接收1024字节的数据
                f.write(data1)  # 写入
                has_receive += len(data1)  # 更新接收到的字节数
            f.close()  # 关闭文件
        print("recv:", filename)
        break
server.close()