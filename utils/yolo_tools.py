import os
import sys
from utils.config_tools import get_config, get_params

def download_yolo():
    path = get_config('Paths', 'yolodir')
    yolo_url = get_config('Downloads', 'yololink')
    a = os.system(f'git clone {yolo_url} {path}')
    a = os.system(f'pip install -r {path}/requirements.txt')
    # subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', f'{path}/yolo/requirements.txt'])


def get_train_params(params_dict):
    params = '--epochs ' + params_dict['epochs']
    params += ' --batch ' + params_dict['batchsize']
    params += ' --workers ' + params_dict['workers']
    params += ' --name ' + params_dict['name']
    if params_dict['devices'] != 'CPU':
        params += ' --devices ' + params_dict['devices']
    if params_dict['imgsize'] != '':
        params += ' --img ' + params_dict['imgsize']

    params += " --weights '" + params_dict['weights'] + "'"

    data = get_config('Paths', 'datayaml')
    train = get_config('Paths', 'trainyaml')
    params += f" --data '{data}' --cfg '{train}'"

    params += ' --nosave --cache'

    return params


def get_detect_params(params_dict):
    main_dir = get_config('Common', 'dir')
    images = get_config('Paths', 'imagesdir')
    params = '--source ' + images
    params += ' --weights ' + f"{main_dir}/runs/train/{params_dict['name']}/weights/best.pt"
    params += ' --conf ' + params_dict['confidence']
    params += ' --name ' + params_dict['name']
    params += ' --save-txt --exist-ok'
    return params

def get_command_yolo(type_yolo):
    params = get_params('Yolo')
    params_dict = {}
    for param, value in params: 
        params_dict[param] = value

    path = get_config('Paths', 'yolodir')

    if type_yolo == 'train':
        params_string = get_train_params(params_dict)
    elif type_yolo == 'detect':
        params_string = get_detect_params(params_dict)

    command = f'python {path}/{type_yolo}.py {params_string}'
    return command


def train_yolo():
    command = get_command_yolo('train')
    a = os.system(command)
    # a = os.system("python yolo/train.py --img 400 --batch 8 --epochs 3 --data '/home/maciekkrysz/Code/GitDir/visdrone/data.yaml' --cfg '/home/maciekkrysz/Code/GitDir/visdrone/train.yaml' --weights '' --name joos --nosave --cache")
# python yolo/train.py --img 400 --batch 16 --epochs 3 --data '/home/maciekkrysz/Code/GitDir/visdrone/data.yaml' --cfg '/home/maciekkrysz/Code/GitDir/visdrone/train.yaml' --weights '' --name joos --nosave --cache


def detect_yolo():
    command = get_command_yolo('detect')
    a = os.system(command)
    # a = os.system("python yolo/detect.py --source images --weights runs/train/yolo/weights/best.pt --conf 0.3 --save-txt")