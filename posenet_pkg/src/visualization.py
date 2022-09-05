#!/usr/bin/env python3
import rospy
import rosbag
import tf
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge
from visualization_msgs.msg import Marker
from PIL import Image 
import cv2
import torch
from data_loader import get_loader
from solver import Solver
from torch.backends import cudnn 

def Sixdof_Pub():
   cnt=0
   pub = rospy.Publisher('/estimate', Marker, queue_size=10)
   image=CompressedImage
   bag = rosbag.Bag("test.bag")
   for topic, img ,t in bag.read_messages(topics=['/zed/left/image_rect_color/compressed']):
      cnt+=1
      if cnt%5==0:
         image = CvBridge().compressed_imgmsg_to_cv2(img)
         color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
         pil_image=Image.fromarray(color_coverted)
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
         print(marker)  
         pub.publish(marker)

def Truth_Pub():
   cnt_truth=0
   truth_pub = rospy.Publisher('/ground_truth', Marker, queue_size=10)
   truth_marker=Marker()
   f=open("test.txt",'r')
   r=rospy.Rate(500) 
   while True:
      cnt_truth+=1
      line=f.readline()
      if not line: break
      arr=line.split(" ")
      tmp=arr[7]
      arr[7]=tmp[:-1]
      truth_marker.header.frame_id = "map"
      truth_marker.header.stamp = rospy.Time.now()
      truth_marker.type = 2
      truth_marker.id = cnt_truth
      truth_marker.scale.x = 0.5
      truth_marker.scale.y = 0.5
      truth_marker.scale.z = 0.5
      truth_marker.color.r = 0.0
      truth_marker.color.g = 0.0
      truth_marker.color.b = 1.0
      truth_marker.color.a = 1.0
      truth_marker.pose.position.x=float(arr[1])
      truth_marker.pose.position.y=float(arr[2])
      truth_marker.pose.position.z=float(arr[3])
      truth_marker.pose.orientation.x=float(arr[4])
      truth_marker.pose.orientation.y=float(arr[5])
      truth_marker.pose.orientation.z=float(arr[6])
      truth_marker.pose.orientation.w=float(arr[7])
      print(truth_marker)
      truth_pub.publish(truth_marker)
      r.sleep()
   f.close()

if __name__ == '__main__':      
   rospy.init_node('visulalization',anonymous=True)     
   try:
      Truth_Pub()
      Sixdof_Pub()
      
   except rospy.ROSInterruptException:
      pass
