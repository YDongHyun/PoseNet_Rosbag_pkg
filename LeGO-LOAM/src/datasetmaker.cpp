#include "utility.h"
#include <fstream>
#include <sensor_msgs/CompressedImage.h>
#include <cv_bridge/cv_bridge.h>
#include <string>

float sixdof[7];
std::ofstream fout;
using namespace std;
using std::string;
using std::to_string;
int global_cnt=0;
int global_len_zero;
string global_zeros;

void Sixdof_sub(const nav_msgs::Odometry::ConstPtr& laserOdometry2){
  global_cnt+=1;
  global_zeros="";
  string tmp=to_string(global_cnt);
  int len=tmp.size();
  global_len_zero=6-len;
  for (int i=0;i<global_len_zero;i++){
    global_zeros+="0";
  }
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
  fout<<"seq/frame"<<global_zeros<<global_cnt<<".png "<<sixdof[0]<<" "<<sixdof[1]<<" "<<sixdof[2]<<" "<<sixdof[3]<<" "<<sixdof[4]<<" "<<sixdof[5]<<" "<<sixdof[6]<<endl; 
  fout.close();
  //printf("x=%f, y=%f, z=%f, w=%f, p=%f, q=%f, r=%f \n",sixdof[0],sixdof[1],sixdof[2],sixdof[3],sixdof[4],sixdof[5],sixdof[6]);
}

void Image_sub(const sensor_msgs::CompressedImage::ConstPtr& CompressedImage){
  cv_bridge::CvImagePtr cvImg = cv_bridge::toCvCopy(CompressedImage, "bgr8");
  cv::Mat myOpenCVImg = cvImg->image;
  string str ="seq/frame";
  string png = ".png";
  str+=global_zeros+to_string(global_cnt)+png;
  cv::imwrite(str, myOpenCVImg);
}

int main(int argc, char **argv)
{
  //boost::filesystem::create_directory("/seq");
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  ros::Subscriber sub_sixdof = n.subscribe("/integrated_to_init", 1000, Sixdof_sub);
  ros::Subscriber sub_image = n.subscribe("/zed/left/image_rect_color/compressed", 1000, Image_sub);
  ros::spin();

  return 0;
}
