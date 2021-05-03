import socket
import os

client = socket.socket()  # 声明socket类型，同时生成socket连接对象
client.connect(('175.27.245.39', 12000))  # 链接服务器的ip + 端口

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获得当前目录

while True:
	msg = input(">>:").strip()  # 获得要向服务端发送的信息，字符串格式
	if len(msg) == 0:
		continue

	client.send(msg.encode("utf-8"))  # 将字符串格式编码成bytes，发送
	if msg == 'break':
		break
	data = client.recv(1024)  # 接收服务端返回的内容
	if len(str(data, 'utf-8').split('|')) == 2:  # 如果返回的字符串长度为2，说明针对的任务2，从服务端传回一张图片
		filename, filesize = str(data, 'utf8').split('|')  # 获得指定图像的名称，图像大小
		path = os.path.join(BASE_DIR, filename)  # 指定图像的保存路径
		filesize = int(filesize)  # 图像大小转换成整形

		f = open(path, 'ab')  # 以二进制格式打开一个文件用于追加。如果该文件不存在，创建新文件进行写入。
		has_receive = 0  # 统计接收到的字节数
		while has_receive != filesize:
			data1 = client.recv(1024)  # 一次从服务端接收1024字节的数据
			f.write(data1)  # 写入
			has_receive += len(data1)  # 更新接收到的字节数
		f.close()  # 关闭文件
	print("recv:", data.decode())

client.close()
