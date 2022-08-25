#include "utility.h"

int sixdof[7];

void sixdof_sub(const nav_msgs::Odometry::ConstPtr& laserOdometry2){
  
  sixdof[0]= laserOdometry2->pose.pose.position.x;
  sixdof[1]= laserOdometry2->pose.pose.position.y;
  sixdof[2]= laserOdometry2->pose.pose.position.z;
  sixdof[3]= laserOdometry2->pose.pose.orientation.x;
  sixdof[4]= laserOdometry2->pose.pose.orientation.y;
  sixdof[5]= laserOdometry2->pose.pose.orientation.z;
       
  printf("x=%f, y=%f, z=%f, x=%f, y=%f, z=%f",sixdof[0],sixdof[1],sixdof[2],sixdof[3],sixdof[4],sixdof[5]);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("/integrated_to_init", 1000, sixdof_sub);
  ros::spin();

  return 0;
}
