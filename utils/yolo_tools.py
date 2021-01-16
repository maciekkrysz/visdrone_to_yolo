import os
import sys

path = '.'
yolo_url = 'https://github.com/ultralytics/yolov5'


def download_yolo():
    a = os.system(f'git clone {yolo_url} {path}/yolo')
    a = os.system(f'pip install -r {path}/yolo/requirements.txt')
    # subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', f'{path}/yolo/requirements.txt'])


def train_yolo():
    a = os.system("python yolo/train.py --img 400 --batch 8 --epochs 3 --data '/home/maciekkrysz/Code/GitDir/visdrone/data.yaml' --cfg '/home/maciekkrysz/Code/GitDir/visdrone/train.yaml' --weights '' --name joos --nosave --cache")
# python yolo/train.py --img 400 --batch 16 --epochs 3 --data '/home/maciekkrysz/Code/GitDir/visdrone/data.yaml' --cfg '/home/maciekkrysz/Code/GitDir/visdrone/train.yaml' --weights '' --name joos --nosave --cache
