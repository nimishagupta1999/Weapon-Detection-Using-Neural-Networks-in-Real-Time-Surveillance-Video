# -*- coding: utf-8 -*-
"""working_script.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VT0ds73ShfmNpPHqQptcakzbLRO01V2L
"""
# to restart a fresh and clean vm
!kill -9 -1

# check if it's using gpu
import tensorflow as tf
tf.test.gpu_device_name()

# show tensorflow version
!pip show tensorflow

# upgrade tensorflow, for gpu version: ...--upgrade tensorflow-gpu
!pip install --upgrade tensorflow

# grand access for the vm from google drive
!apt-get install -y -qq software-properties-common python-software-properties module-init-tools
!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
!apt-get update -qq 2>&1 > /dev/null
!apt-get -y install -qq google-drive-ocamlfuse fuse
from google.colab import auth
auth.authenticate_user()
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
import getpass
!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}

# mount the drive
!mkdir -p my_drive
!google-drive-ocamlfuse my_drive

# show working directory
!ls

# install protobuf
!apt-get install -y -qq protobuf-compiler python-pil python-lxml

# change working directory
import os
os.chdir('my_drive/app/models/research')

# show current system path
# %pwd

# apply protoc
!protoc object_detection/protos/*.proto --python_out=.

# append slim to system path
import sys
sys.path.append('/content/my_drive/app/models/research/slim')

print(sys.path)

# run the to see if the object api is working
# %run object_detection/builders/model_builder_test.py

# formally install object detection api library
!python3 setup.py install

# change working directory
import os
os.chdir('object_detection')

# start training
%run train.py --logtostderr --train_dir=training/ --pipeline_config_path=training/faster_rcnn_inception_v2_coco.config

# use this when you encounter multiple flags error 
# (usually happens when you restart process after the process is interupted)
def del_all_flags(FLAGS):
    flags_dict = FLAGS._flags()
    keys_list = [keys for keys in flags_dict]
    for keys in keys_list:
        FLAGS.__delattr__(keys)
del_all_flags(tf.flags.FLAGS)

# not working, see comment below
!tensorboard --logdir=/content/my_drive/app/models/research/models/training

"""Not working, download the training folder to launch tensorboard locally"""

# import os
# os.chdir('/content/my_drive/app/models/research')

# output inference graph from the trained model
%run export_inference_graph.py \
    --input_type image_tensor \
    --pipeline_config_path training/faster_rcnn_inception_v2_coco.config \
    --trained_checkpoint_prefix training/model.ckpt-5347 \
    --output_directory WEAPON_DETECTION_GRAPH