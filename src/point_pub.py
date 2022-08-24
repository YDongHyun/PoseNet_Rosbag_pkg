#!/usr/bin/env python

import rospy
from sensor_msgs.msg import CompressedImage
import rosbag

bag = rosbag.Bag('/media/ydh/18262CDF262CC01C/2017-12-05-13-23-48.bag')
for msg in bag.read_messages(topics=['/velodyne_points']):
   print(msg)
bag.close()
