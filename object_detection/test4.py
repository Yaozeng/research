
import cv2

import numpy as np
import os
from matplotlib import pyplot as plt
import sys

import tensorflow as tf
from PIL import Image

## This is needed to display the images.
#%matplotlib inline

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

from object_detection.utils import label_map_util

from object_detection.utils import visualization_utils as vis_util

# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

#download model
#opener = urllib.request.URLopener()
#下载模型，如果已经下载好了下面这句代码可以注释掉
#opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
#tar_file = tarfile.open(MODEL_FILE)
#for file in tar_file.getmembers():
# file_name = os.path.basename(file.name)
 # if 'frozen_inference_graph.pb' in file_name:
   # tar_file.extract(file, os.getcwd())
clicked=False
def onMounse(event,x,y,param):
    global clicked
    if event==cv2.EVENT_LBUTTONUP:
        clicked=True

#Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')
#Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
#Helper code

# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_PATHS = os.path.join(PATH_TO_TEST_IMAGES_DIR, 'test2.mp4')
print(TEST_IMAGE_PATHS)
cv2.namedWindow('mywindows')
cv2.setMouseCallback('mywindows', onMounse)
with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
      camerCapture = cv2.VideoCapture(0)
      success,frame=camerCapture.read()
      while success and cv2.waitKey(1) == -1 and not clicked:
          # the array based representation of the image will be used later in order to prepare the
          # result image with boxes and labels on it.
          # image_np = load_image_into_numpy_array(image)
          # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
          #image_np = frame.transpose(1,0,2).astype(np.uint8)
          #print(image_np)
          image_np_expanded = np.expand_dims(frame, axis=0)
          image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
          # Each box represents a part of the image where a particular object was detected.
          boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
          # Each score represent how level of confidence for each of the objects.
          # Score is shown on the result image, together with the class label.
          scores = detection_graph.get_tensor_by_name('detection_scores:0')
          classes = detection_graph.get_tensor_by_name('detection_classes:0')
          num_detections = detection_graph.get_tensor_by_name('num_detections:0')
          # Actual detection.
          (boxes, scores, classes, num_detections) = sess.run(
              [boxes, scores, classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})
          # Visualization of the results of a detection.
          vis_util.visualize_boxes_and_labels_on_image_array(
              frame,
              np.squeeze(boxes),
              np.squeeze(classes).astype(np.int32),
              np.squeeze(scores),
              category_index,
              use_normalized_coordinates=True,
              line_thickness=8)
          #print(image_np.shape)
          #plt.imshow(image_np)
          #image_np=image_np.transpose(1,0,2)
          cv2.imshow('mywindows', frame)
          success,frame=camerCapture.read()
      cv2.destroyWindow('mywindows')
      camerCapture.release()
