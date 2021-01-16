from utils.visdrone_tools import download_train_google, download_val_google
from utils.visdrone_tools import unzip_train, unzip_val
from utils.visdrone_tools import convert_train, convert_val

from utils.yolo_tools import download_yolo, train_yolo
import time

def main():
    # download_train_google()
    # unzip_train()
    # convert_train()

    # download_val_google()
    # unzip_val()
    # convert_val()

    # download_yolo()
    train_yolo()
    pass
# python yolo/detect.py --source images --weights runs/train/joos9/weights/best.pt --img 416 --conf 0.5 --save-txt                 
main()