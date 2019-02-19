# Single-Shot Refinement Neural Network for Object Detection
fork from https://github.com/sfzhang15/RefineDet

### Introduction
添加widerface数据集训练脚本<br>

### Contents
1. [Installation](#installation)
2. [GetData](#getdata)
3. [Training](#training)
4. [Demo](#demo)

### Installation
1. Get the code. We will call the cloned directory as `$RefineDet_ROOT`.
  ```Shell
  https://github.com/ycdhqzhiai/RefineDet.git
  ```
2. Build the code.
  ```Shell
  cd $RefineDet_ROOT
  mkdir build
  cd build
  cmake ..
  make -j8
  ```  
### GetData

1. download datasets.<br>
   网盘链接: https://pan.baidu.com/s/10ZFFIgbp7H3bveyViMwkug#list/path=%2F<br/>
   密码：uc5s
2. 解压.<br>
   unzip XXX.zip
3. 生成VOC格式数据.<br>
  ```shell
  python face_labels.py
  ```
4. 生成lmdb.<br>
  ```shell
  # You can modify the parameters in create_data.sh if needed.
  # It will create lmdb files for trainval and test with encoded original image:
  #   - $HOME/data/VOCdevkit/VOC0712/lmdb/VOC0712_trainval_lmdb
  #   - $HOME/data/VOCdevkit/VOC0712/lmdb/VOC0712_test_lmdb
  # and make soft links at examples/VOC0712/
  cd $RefineDet_ROOT
  ./data/wider_face/create_data.sh
  ```
5.建立软链接.<br>
  ```shell
  cd face_data
  ln -s $wider_face_trian_lmdb trainval_lmdb
  ln -s $wider_face_test_lmdb test_lmdb
  ```
6.生成测试集name_size.txt.<br>
  ```shell
  cd $RefineDet_ROOT/data/wider_face/
  bash create_list.sh
  ```
### Training
  ```shell
  bash train.sh
  ```
### Demo
  ```Shell
  # For GPU users
  python test/refinedet_demo.py
  # For CPU users
  python test/refinedet_demo.py --gpu_id -1
  ```
