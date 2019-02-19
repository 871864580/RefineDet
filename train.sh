#!/bin/sh
if ! test example/MobileNetSSD_train.prototxt ;then
	echo "error: example/MobileNetSSD_train.prototxt does not exist."
	echo "please use the gen_model.sh to generate your own model."
        exit 1
fi
mkdir -p snapshot
./build/tools/caffe train -solver=/home/yc/workplace/deeplearning/object_detect/RefineDet/models/VGGNet/widerface/refinedet_vgg16_320x320/solver.prototxt -gpu 0,1,2,3  2>&1 | tee examples/widerface_train_log.log
