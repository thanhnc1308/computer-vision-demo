import string
import argparse


import torch
import torch.backends.cudnn as cudnn
import torch.utils.data
import torch.nn.functional as F

from recognition.utils import CTCLabelConverter, AttnLabelConverter
from recognition.dataset import RawDataset, AlignCollate
from recognition.model import Model

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

import pandas as pd
import os


def demo(opt):
    """Open csv file wherein you are going to write the Predicted Words"""
    current_path = os.getcwd()
    directory = os.path.join(current_path, 'craft_pytorch/Results/data.csv')
    data = pd.read_csv(directory)

    """ model configuration """
    if 'CTC' in opt["Prediction"]:
        converter = CTCLabelConverter(opt["character"])
    else:
        converter = AttnLabelConverter(opt["character"])
    opt["num_class"] = len(converter.character)

    if opt["rgb"]:
        opt["input_channel"] = 3
    model = Model(opt)
    print('model input parameters', opt["imgH"], opt["imgW"], opt["num_fiducial"], opt["input_channel"], opt["output_channel"],
          opt["hidden_size"], opt["num_class"], opt["batch_max_length"], opt["Transformation"], opt["FeatureExtraction"],
          opt["SequenceModeling"], opt["Prediction"])
    model = torch.nn.DataParallel(model).to(device)

    # load model
    print('craft_recog.py | loading pretrained model from %s' % opt["saved_model"])
    model.load_state_dict(torch.load(opt["saved_model"], map_location=device))

    # prepare data. two demo images from https://github.com/bgshih/crnn#run-demo
    AlignCollate_demo = AlignCollate(imgH=opt["imgH"], imgW=opt["imgW"], keep_ratio_with_pad=opt["PAD"])
    demo_data = RawDataset(root=opt["image_folder"], opt=opt)  # use RawDataset
    demo_loader = torch.utils.data.DataLoader(
        demo_data, batch_size=opt["batch_size"],
        shuffle=False,
        num_workers=int(opt["workers"]),
        collate_fn=AlignCollate_demo, pin_memory=True)

    print('craft_recog.py | predict')

    # predict
    model.eval()
    print('craft_recog.py | torch: ', torch)
    with torch.no_grad():
        print("craft_recog.py | demo_loader: ",demo_loader)
        for image_tensors, image_path_list in demo_loader:
            print("looping:",image_tensors, image_path_list)
            batch_size = image_tensors.size(0)
            image = image_tensors.to(device)
            # For max length prediction
            length_for_pred = torch.IntTensor([opt["batch_max_length"]] * batch_size).to(device)
            text_for_pred = torch.LongTensor(batch_size, opt["batch_max_length"] + 1).fill_(0).to(device)

            if 'CTC' in opt["Prediction"]:
                preds = model(image, text_for_pred)

                # Select max probabilty (greedy decoding) then decode index to character
                preds_size = torch.IntTensor([preds.size(1)] * batch_size)
                _, preds_index = preds.max(2)
                # preds_index = preds_index.view(-1)
                preds_str = converter.decode(preds_index.data, preds_size.data)

            else:
                preds = model(image, text_for_pred, is_train=False)

                # select max probabilty (greedy decoding) then decode index to character
                _, preds_index = preds.max(2)
                preds_str = converter.decode(preds_index, length_for_pred)

            dashed_line = '-' * 80
            head = f'{"image_path":25s}\t {"predicted_labels":25s}\t confidence score'

            print(f'{dashed_line}\n{head}\n{dashed_line}')
            # log.write(f'{dashed_line}\n{head}\n{dashed_line}\n')

            preds_prob = F.softmax(preds, dim=2)
            preds_max_prob, _ = preds_prob.max(dim=2)
            for img_name, pred, pred_max_prob in zip(image_path_list, preds_str, preds_max_prob):
                current_path = os.getcwd()
                start = os.path.join(current_path, 'craft_pytorch/CropWords')
                # start = 'craft_pytorch\\CropWords\\'
                path = os.path.relpath(img_name, start)

                folder = os.path.dirname(path)

                image_name = os.path.basename(path)

                file_name = '_'.join(image_name.split('_')[:-8])

                txt_file = os.path.join(start, folder, file_name)

                log = open(f'{txt_file}_log_demo_result_vgg.txt', 'a')
                if 'Attn' in opt["Prediction"]:
                    pred_EOS = pred.find('[s]')
                    pred = pred[:pred_EOS]  # prune after "end of sentence" token ([s])
                    pred_max_prob = pred_max_prob[:pred_EOS]

                # calculate confidence score (= multiply of pred_max_prob)
                confidence_score = pred_max_prob.cumprod(dim=0)[-1]
                print(f'{image_name:25s}\t {pred:25s}\t {confidence_score:0.4f}')
                log.write(f'{image_name:25s}\t {pred:25s}\t {confidence_score:0.4f}\n')

            log.close()

class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]

def craft_recog():
    print("craft_recog.py | craft_recog")
    current_path = os.getcwd()
    directory = os.path.join(current_path, 'craft_pytorch/Results/data.csv')
    opt = {
        'image_folder' : os.path.join(current_path, 'craft_pytorch/CropWords'), #path to image_folder which contains cropped images
        'workers' : 4, #number of data loading workers
        'batch_size' : 192, #input batch size
        'saved_model' : os.path.join(current_path, 'craft_pytorch/weights/TPS-ResNet-BiLSTM-Attn-case-sensitive.pth'), #path to saved_model to evaluation
        'batch_max_length' : 25, #maximum-label-length
        'imgH' : 32, #the height of the input image
        'imgW' : 100, #the width of the input image
        'rgb' : 0, #use rgb input
        'character' : '0123456789abcdefghijklmnopqrstuvwxyz', #character label
        'sensitive' : True, #for sensitive character mode
        'PAD' : False, #whether to keep ratio then pad for image resize
        'Transformation' : 'TPS', #Transformation stage. None|TPS
        'FeatureExtraction' : 'ResNet', #FeatureExtraction stage. VGG|RCNN|ResNet
        'SequenceModeling' : 'BiLSTM', #SequenceModeling stage. None|BiLSTM
        'Prediction' : 'Attn', #Prediction stage. CTC|Attn
        'num_fiducial' : 20, #number of fiducial points of TPS-STN
        'input_channel' : 1, #the number of input channel of Feature extractor
        'output_channel' : 512, #the number of output channel of Feature extractor
        'hidden_size' : 256 #the size of the LSTM hidden state
    }

    """ vocab / character number configuration """
    if opt["sensitive"]:
        opt["character"] = string.printable[:-6]  # same with ASTER setting (use 94 char).

    cudnn.benchmark = True
    cudnn.deterministic = True
    opt["num_gpu"] = torch.cuda.device_count()
    # print (opt["image_folder"])

    # pred_words=demo(opt)
    demo(opt)
