# PoseNet_Rosbag_pkg

- .bag파일을 읽어오기 위해 ROS noetic 설치
- rosbag info를 이용하여 bag파일 정보를 확인
![image](https://user-images.githubusercontent.com/80799025/186364054-0714ec98-9f2f-4635-85f4-41b79c0889fc.png)

- rviz를 이용한 bag 파일 시각화\
< blog참조 : https://bigbigpark.tistory.com/36 >

![Peek 2022-08-24 21-57](https://user-images.githubusercontent.com/80799025/186424296-cda031fd-3b6c-4335-b3f3-1421c8ec850c.gif)

- Lidar값을 받아오는 node 작성

- Ground Truth metadata를 얻기위해 Lego_LOAM 및 gstam 설치
 < https://github.com/RobustFieldAutonomyLab/LeGO-LOAM >

# Lego_LOAM

### 빌드 오류
다음 블로그 참조 < https://xiaotaoguo.com/p/lego-loam-setup-ubuntu20/ >
- pcl 파일 eigen::index를 int로 수정
- utiliy.h 파일에서 opencv2 수정 및 unit16_6 -> std::uint16_t로 수정
- Cmake_list파일에 boost관련 추가


```
find_package(Boost REQUIRED COMPONENTS thread)
find_package(Boost REQUIRED COMPONENTS serialization)
find_package(Boost REQUIRED COMPONENTS timer)
```

- LeGO_LOAM cpp파일중, frame_id관련 코드의 / 를 지워 오류 해결

- 최종적으로 LeGO_LOAM 실행
![image](https://user-images.githubusercontent.com/80799025/186603344-bcb7c2d0-6796-40be-979a-b16c2d096ef1.png)

- LeGo_LOAM의 rqt graph
![image](https://user-images.githubusercontent.com/80799025/186645810-0c39abb9-1a26-4882-a16a-527eea9285f1.png)


- sixdof_sub 노드 제작
- LeGo_LOAM에서 6 dof값을 받아오는 노드
![image](https://user-images.githubusercontent.com/80799025/186845576-128216d7-8749-4abb-a73a-663afed57cdc.png)
- 결과들을 train.txt로 저장하도록 노드 수정 
- datasetmaker로 수정

## datasetmaker.cpp
- PoseNet을 위한 Dataset을 만드는 Node
- Lego_LOAM을 통해 6 dof값을 train.txt파일에 저장하고, Compressed Image를 받아와 변환하여 저장하는 노드
- 아래 커맨드로 bag파일 실행시 생성
```
rosbag play train.bag --clock --topic /zed/left/image_rect_color/compressed /imu/data /velodyne_points
```
- datasetmaker 노드 실행 후, bag파일 실행시 아래와 같이 자동으로 데이터셋 생성 및 저장
![image](https://user-images.githubusercontent.com/80799025/187027494-8cea6889-09b0-4bea-9682-303c8c286b31.png)

# PoseNet
- 위에서 생성한 데이터셋으로 PoseNet 학습
- 16batch 100 epoch으로 학습

![image](https://user-images.githubusercontent.com/80799025/187037027-fe14810e-8583-4093-ae29-c32547d3a1ed.png)

- test 데이터셋과 train데이터 셋의 시작지점이 달라 기준이 다르게 되어 좌표 오차가 많이 발생하였다. 추후 test데이터셋을 다시 확인해야겠다.
- test bag을 돌릴 때 train bag파일과 시점을 맞춘 후 다시 돌렸다.

![image](https://user-images.githubusercontent.com/80799025/187063968-207507c1-49b0-44e0-8f7c-ecb79f88f530.png)
- 다음과 같은 결과를 얻었다. 좌표를 맞춘 후 다시 test하니 오차가 크게 줄었다.
- 학습 epoch을 더 늘려 모델을 더 정확하게 만들어 볼 계획이다.

-200 epoch

![image](https://user-images.githubusercontent.com/80799025/187084152-382c5217-db5c-4be1-b7e5-9d2cd19be28f.png)


# 시각화
- test.bag파일을 visualization.py로 이미지를 받아, PoseNet을 실행시킨 후 결과를 출력
- 아래 사진은 estimate값만을 표현, PoseNet을 수행하는데 시간이 오래걸려 중간에 프레임이 끊긴것을 확인할 수 있다.

![image](https://user-images.githubusercontent.com/80799025/187133430-ed6008b6-c0cf-4c38-9e8e-dc45f7fc6ffb.png)


