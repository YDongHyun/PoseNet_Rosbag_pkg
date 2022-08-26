#include "utility.h"
#include <fstream>
#include <sensor_msgs/CompressedImage.h>
#include <cv_bridge/cv_bridge.h>

float sixdof[7];
std::ofstream fout;

void sixdof_sub(const nav_msgs::Odometry::ConstPtr& laserOdometry2){
  
  sixdof[0]= laserOdometry2->pose.pose.position.z;
  sixdof[1]= laserOdometry2->pose.pose.position.x;
  sixdof[2]= laserOdometry2->pose.pose.position.y;
  sixdof[3]= laserOdometry2->pose.pose.orientation.x;
  sixdof[4]= laserOdometry2->pose.pose.orientation.y;
  sixdof[5]= laserOdometry2->pose.pose.orientation.z;
  sixdof[6]= laserOdometry2->pose.pose.orientation.w;
  ofstream fout("train.txt",std::ios_base::out|std::ios_base::app);
  fout << fixed;
  fout.precision(6);
  fout<<sixdof[0]<<" "<<sixdof[1]<<" "<<sixdof[2]<<" "<<sixdof[3]<<" "<<sixdof[4]<<" "<<sixdof[5]<<" "<<sixdof[6]<<endl; 
  fout.close();
  //printf("x=%f, y=%f, z=%f, w=%f, p=%f, q=%f, r=%f \n",sixdof[0],sixdof[1],sixdof[2],sixdof[3],sixdof[4],sixdof[5],sixdof[6]);
}

void Image_sub(const sensor_msgs::CompressedImage::ConstPtr& CompressedImage){
  cv_bridge::CvImagePtr cvImg = cv_bridge::toCvCopy(CompressedImage, "bgr8");
  cv::Mat myOpenCVImg = cvImg->image;
  cv::imwrite("test.png", myOpenCVImg);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  ros::Subscriber sub_image = n.subscribe("/zed/left/image_rect_color/compressed", 1000, Image_sub);
  ros::Subscriber sub_sixdof = n.subscribe("/integrated_to_init", 1000, sixdof_sub);
  ros::spin();

  return 0;
}
