import sys
import os
import time
import argparse

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable

from PIL import Image

import cv2
from skimage import io
import numpy as np

import json
import zipfile
import pandas as pd

from craft_pytorch import craft_utils
from craft_pytorch import test
from craft_pytorch import imgproc
from craft_pytorch import file_utils
from craft_pytorch.craft import CRAFT

from collections import OrderedDict

# google.colab.patches import cv2_imshow

def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")

a_trained_model = 'craft_pytorch/weights/craft_mlt_25k.pth'
a_text_threshold = 0.5 # bao nhieu % la chu / original 0.7
a_low_text = 0.4 # dien tich de nhan la ky / original 0.4
a_link_threshold = 0.4
a_cuda = False
a_canvas_size = 1280 # original 1280
a_mag_ratio = 8 # original 1.5
a_poly = False
a_show_time = False
a_test_folder = 'raw_image'
a_refine = False
a_refiner_model = 'craft_pytorch/weights/craft_refiner_CTW1500.pth'

""" For test images in a folder """
image_list, _, _ = file_utils.get_files(a_test_folder)

image_names = []
image_paths = []

#CUSTOMISE START
start = a_test_folder

for num in range(len(image_list)):
  image_names.append(os.path.relpath(image_list[num], start))


result_folder = 'craft_pytorch/Results'
if not os.path.isdir(result_folder):
    os.mkdir(result_folder)

# if __name__ == '__main__':
def pipeline():
    data=pd.DataFrame(columns=['image_name', 'word_bboxes', 'pred_words', 'align_text'])
    data['image_name'] = image_names

    # load net
    net = CRAFT()     # initialize

    print('Loading weights from checkpoint (' + a_trained_model + ')')
    if a_cuda:
        net.load_state_dict(test.copyStateDict(torch.load(a_trained_model)))
    else:
        net.load_state_dict(test.copyStateDict(torch.load(a_trained_model, map_location='cpu')))

    if a_cuda:
        net = net.cuda()
        net = torch.nn.DataParallel(net)
        cudnn.benchmark = False

    net.eval()

    # LinkRefiner
    refine_net = None
    if a_refine:
        from craft_pytorch.refinenet import RefineNet
        refine_net = RefineNet()
        print('Loading weights of refiner from checkpoint (' + a_refiner_model + ')')
        if a_cuda:
            refine_net.load_state_dict(copyStateDict(torch.load(a_refiner_model)))
            refine_net = refine_net.cuda()
            refine_net = torch.nn.DataParallel(refine_net)
        else:
            refine_net.load_state_dict(copyStateDict(torch.load(a_refiner_model, map_location='cpu')))

        refine_net.eval()
        a_poly = True

    t = time.time()

    # load data
    for k, image_path in enumerate(image_list):
        print("Test image {:d}/{:d}: {:s}".format(k+1, len(image_list), image_path), end='\r')
        image = imgproc.loadImage(image_path)

        a_poly = False
        bboxes, polys, score_text, det_scores = test.test_net(net, image, a_text_threshold, a_link_threshold, a_low_text, a_cuda, a_poly, a_canvas_size, a_mag_ratio, refine_net)

        bbox_score={}

        for box_num in range(len(bboxes)):
          key = str (det_scores[box_num])
          item = bboxes[box_num]
          bbox_score[key]=item

        data['word_bboxes'][k]=bbox_score
        # save score text
        filename, file_ext = os.path.splitext(os.path.basename(image_path))
        mask_file = result_folder + "/res_" + filename + '_mask.jpg'
        cv2.imwrite(mask_file, score_text)

        file_utils.saveResult(image_path, image[:,:,::-1], polys, dirname=result_folder)

    #data.to_csv('/content/Pipeline/data.csv', sep = ',', na_rep='Unknown')
    data.to_csv('craft_pytorch/Results/data.csv', sep = ',', na_rep='Unknown')

    #dataFile = result_folder + "/data.csv"
    #if not os.path.isfile(dataFile)
       #should not create file???
    #data.to_csv('./Results/data.csv', sep = ',', na_rep='Unknown')
    print("elapsed time : {}s".format(time.time() - t))
