#!/usr/bin/env python3
import rospy
import cv2
import time
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge

path = '/home/ydh/catkin_ws/image/'
cnt = 0
count = 0
def callback(data):
    global cnt
    global count
    if count%15==0:
        cv_bridge = CvBridge()
        img=cv_bridge.compressed_imgmsg_to_cv2(data,"bgr8")
        name=path+str(cnt).zfill(5)+".jpg"
        cv2.imwrite(name, img)
        print("subscribed")
        cnt+=1
    count+=1
    
def Image_sub():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/camera/color/image_raw/compressed',CompressedImage, callback)
    rospy.spin()


if __name__ == '__main__':      
   Image_sub()