# PoseNet_Rosbag_pkg

- .bag파일을 읽어오기 위해 ROS1 설치
- rosbag info를 이용하여 bag파일 정보를 확인
![image](https://user-images.githubusercontent.com/80799025/186364054-0714ec98-9f2f-4635-85f4-41b79c0889fc.png)

- rviz를 이용한 bag 파일 시각화\
< blog참조 : https://bigbigpark.tistory.com/36 >

![Peek 2022-08-24 21-57](https://user-images.githubusercontent.com/80799025/186424296-cda031fd-3b6c-4335-b3f3-1421c8ec850c.gif)

- Lidar값을 받아오는 node 작성

- Ground Truth metadata를 얻기위해 Lego_LOAM 및 gstam 설치
 < https://github.com/RobustFieldAutonomyLab/LeGO-LOAM >

## Lego_LOAM 빌드 오류

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
