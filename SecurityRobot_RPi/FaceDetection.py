import cv2
import datetime
import os
import shutil
import socket_client
import time

def face_rec():
    # 加载视频
    cameraCapture = cv2.VideoCapture(0)
    # cv2级联分类器CascadeClassifier,xml文件为训练数据
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # 读取数据
    success, frame = cameraCapture.read()

    face_times = 0
    while success and cv2.waitKey(1) == -1:
        # 读取数据
        ret, img = cameraCapture.read()
        # 进行人脸检测
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        # 绘制矩形框
        # print(faces)

        if faces != ():
            face_times = face_times + 1
        if face_times > 50:
            for (x, y, w, h) in faces:
                img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # print(x, y, w, h)
                # img_cut = img[y:y+h,x:x+w]
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
                            print('remove')
                dir = 'FaceDetection_Img/' + data  # 需要创建的目录
                if not os.path.exists(dir):   # 创建以日期为单位的目录
                    os.makedirs(dir)
                img_cut_name = dir +'/'+datetime.datetime.now().strftime('%H-%M-%S') + '.jpg'   # 以秒为单位写入文件

            cv2.imwrite(img_cut_name, img)
            print('cut success!')
            socket_client.socket_client_sent_img(dir,datetime.datetime.now().strftime('%H-%M-%S') + '.jpg')  # socket发送图片
            print(str(img_cut_name)+'  send success!')  # 打印文件名

            face_times = 0

        # 设置显示窗口
        cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)
        #cv2.resizeWindow('camera', 840, 480)
        # 显示处理后的视频
        cv2.imshow('camera', img)
        # 读取数据
        success, frame = cameraCapture.read()
    # 释放视频
    cameraCapture.release()
    # 释放所有窗口
    cv2.destroyAllWindows()


# if __name__ == '__main__':
#     face_rec()