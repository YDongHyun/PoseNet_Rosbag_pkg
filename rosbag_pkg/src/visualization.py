#!/usr/bin/env python3

import rospy
import tf
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
from visualization_msgs.msg import Marker
from PIL import Image 
import cv2
import torch
from data_loader import get_loader
from solver import Solver
from torch.backends import cudnn 

cnt=0
def Bag_Sub():
   rospy.init_node('sub',anonymous=True)     
   sub = rospy.Subscriber('/zed/left/image_rect_color/compressed', CompressedImage, Sixdof_Pub)
   rospy.spin()

def Sixdof_Pub(CompressedImage):
   global cnt
   cnt+=1
   pub = rospy.Publisher('/sixdof', Marker, queue_size=10)
   image=CompressedImage
   image = CvBridge().compressed_imgmsg_to_cv2(CompressedImage)
   pil_image=Image.fromarray(image)
   cudnn.benchmark = True
   data_loader = get_loader(model='Resnet', image_path=pil_image ,mode='test', batch_size=1)
   sol=Solver(data_loader)
   pos,ori=sol.test()
   quaternion = tf.transformations.quaternion_from_euler(ori[0], ori[1], ori[2])
   marker = Marker()
   marker.header.frame_id = "map"
   marker.header.stamp = rospy.Time.now()
   marker.type = 2
   marker.id = cnt
   marker.scale.x = 0.5
   marker.scale.y = 0.5
   marker.scale.z = 0.5
   marker.color.r = 0.0
   marker.color.g = 1.0
   marker.color.b = 0.0
   marker.color.a = 1.0
   marker.pose.position.x=float(pos[0])
   marker.pose.position.y=float(pos[1])
   marker.pose.position.z=float(pos[2])
   marker.pose.orientation.x=float(quaternion[0])
   marker.pose.orientation.y=float(quaternion[1])
   marker.pose.orientation.z=float(quaternion[2])
   marker.pose.orientation.w=float(quaternion[3])
   pub.publish(marker)

if __name__ == '__main__':
   try:
      Bag_Sub()
   except rospy.ROSInterruptException:
      pass
