import cv2
import datetime
import os
import shutil
import socket_client
import time
import socket_client_video
import threading

def face_rec():
    # sock,encode_param = socket_client_video.Init_SendVideo()

    # 加载视频
    cameraCapture = cv2.VideoCapture(0)
    # cv2级联分类器CascadeClassifier,xml文件为训练数据
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # 读取数据
    success, frame = cameraCapture.read()
    faces = ()


    def send_video():
        while True:  # 连接尝试
            try:
                sock, encode_param = socket_client_video.Init_SendVideo()
                while True:  # 视频发送尝试
                    try:
                        socket_client_video.SendVideo(sock, img, encode_param)
                    except Exception as e:
                        break
            except Exception as e:
                print("Video TCP socket reconnect!")


    def send_img():
        face_times = 0
        while True:
            if faces != ():
                face_times = face_times + 1
            if face_times > 30:
                # img_cut = img[y:y+h,x:x+w]
                data = str(datetime.datetime.now().strftime('%Y-%m-%d'))  # 获取当前的日期
                year, month, day = data.split('-')[0], data.split('-')[1], data.split('-')[2]
                # print(year,month,day)
                for root, dirs, files in os.walk('FaceDetection_Img/'):
                    # print(dirs)
                    # 当前目录路径,当前路径下所有子目录,当前路径下所有非目录子文件
                    for dir in dirs:
                        pre_year, pre_month, pre_day = dir.split('-')[0], dir.split('-')[1], dir.split('-')[2]
                        if (int(pre_year) < int(year)) | (int(pre_month) < int(month)) | (int(pre_day) + 3 < int(day)):
                            shutil.rmtree('FaceDetection_Img/' + dir)
                            print('remove')
                dir = 'FaceDetection_Img/' + data  # 需要创建的目录
                if not os.path.exists(dir):  # 创建以日期为单位的目录
                    os.makedirs(dir)
                img_cut_name = dir + '/' + datetime.datetime.now().strftime('%H-%M-%S') + '.jpg'  # 以秒为单位写入文件

                cv2.imwrite(img_cut_name, img)
                print('cut success!')
                socket_client.socket_client_sent_img(dir, datetime.datetime.now().strftime(
                    '%H-%M-%S') + '.jpg')  # socket发送图片
                print(str(img_cut_name) + '  sending')  # 打印文件名

                face_times = 0


    send_video_threading = threading.Thread(target=send_video)  # 给视频发送单独给个线程
    send_video_threading.start()  # 线程开始

    send_img_threading = threading.Thread(target=send_img)  # 给视频发送单独给个线程
    send_img_threading.start()  # 线程开始

    while success and cv2.waitKey(1) == -1:
        # 读取数据
        ret, img = cameraCapture.read()
        # 进行人脸检测
        try:
            faces = face_cascade.detectMultiScale(img, 1.3, 5)
        except Exception as e:
            print(e)
        # 绘制矩形框
        # print(faces)

        for (x, y, w, h) in faces:   #画出人脸位置
                img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # print(x, y, w, h)

        # socket_client_video.SendVideo(sock,img,encode_param)


        # 设置显示窗口
        # cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)
        #cv2.resizeWindow('camera', 840, 480)
        # 显示处理后的视频
        # cv2.imshow('camera', img)
        # 读取数据
        success, frame = cameraCapture.read()
    # 释放视频
    cameraCapture.release()
    # 释放所有窗口
    cv2.destroyAllWindows()


# if __name__ == '__main__':
#     face_rec()