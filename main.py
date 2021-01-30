from utils.visdrone_tools import download_train_google, download_val_google
from utils.visdrone_tools import unzip_train, unzip_val
from utils.visdrone_tools import convert_train, convert_val
from utils.yolo_tools import download_yolo, train_yolo, detect_yolo
from utils.config_tools import *
import time

def start_app():
    steps = []
    print('Steps:')
    for key, value in get_params('Optionals'):
        if value == 'True':
            print('-' + key)
            steps.append(key)

    if 'trainset' in steps:
        print('\nTrainSet download and convert')
        download_train_google()
        unzip_train()
        convert_train()

    if 'valset' in steps:
        print('\nValset download and convert')
        download_val_google()
        unzip_val()
        convert_val()

    if 'yolo' in steps:
        print('\nYolo download and compile')
        download_yolo()

    if 'train' in steps:
        print('\nTraining yolo')
        train_yolo()

    if 'detect' in steps:
        print('\Detecting')
        detect_yolo()
    
# python yolo/detect.py --source images --weights runs/train/joos9/weights/best.pt --img 416 --conf 0.5 --save-txt                 

if __name__ == '__main__':
    start_app()