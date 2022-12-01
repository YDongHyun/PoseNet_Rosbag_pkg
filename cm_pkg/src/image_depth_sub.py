#!/usr/bin/env python3
import rospy
import cv2
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

path = '/home/ydh/catkin_ws/image/'
path2 = '/home/ydh/catkin_ws/depth/'
cnt = 0
count =0 

def callback_depth(data):
    global dep_img
    cv_bridge = CvBridge()
    dep_img=cv_bridge.imgmsg_to_cv2(data)

        
def callback(data):
    global cnt
    global count
    if count%10 ==0:
        cv_bridge = CvBridge()
        img=cv_bridge.imgmsg_to_cv2(data,"bgr8")
        name=path+str(cnt).zfill(5)+".jpg"
        re = cv2.resize(img,(848,480))
        cv2.imwrite(name, img)
        print("subscribed_image")

        name=path2+str(cnt).zfill(5)+".png"
        cv2.imwrite(name,dep_img)
        print("subscribed_depth")
        cnt+=1
    count+=1

def Image_sub():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/device_0/sensor_1/Color_0/image/data',Image, callback)
    rospy.Subscriber('/device_0/sensor_0/Depth_0/image/data',Image, callback_depth)
    #rospy.Subscriber('/camera/color/image_raw',Image, callback)
    rospy.spin()

if __name__ == '__main__':      
   Image_sub()
