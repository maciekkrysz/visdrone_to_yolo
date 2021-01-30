from utils.download_tools import download_file_from_google_drive, unzip
from utils.converter import convert
from utils.config_tools import get_config
import os


def download_train_google():
    train_data_id = get_config('Download', 'traindataid')
    train_zip_path = get_config('Common', 'dir') + '/train.zip'

    download_file_from_google_drive(train_data_id, train_zip_path)


def download_val_google():
    val_data_id = get_config('Download', 'valdataid')
    val_zip_path = get_config('Common', 'dir') + '/val.zip'

    download_file_from_google_drive(val_data_id, val_zip_path)
    

def unzip_train():
    train_zip_path = get_config('Common', 'dir') + '/train.zip'
    train_path = get_config('Paths', 'traindir')

    unzip(train_zip_path)
    exctract_from_visdrone_to_dir(train_path)


def unzip_val():
    val_zip_path = get_config('Common', 'dir') + '/val.zip'
    val_path = get_config('Paths', 'valdir')

    unzip(val_zip_path)
    exctract_from_visdrone_to_dir(val_path)


def exctract_from_visdrone_to_dir(path='.'):
    a = os.system(f'rm -r -f {path}')
    vis_dir = os.popen('find ./ -name "VisDrone*"').read()
    vis_dir = vis_dir.split("\n")[0]
    ls = os.popen(f'ls {vis_dir}').read()
    print(vis_dir)
    a = os.system(f'mkdir {path}')
    if 'annotations' in ls and 'images' in ls:
        a = os.system(f'mv {vis_dir}/* {path}')
        a = os.system(f'rm -r {vis_dir}')


def convert_train():
    train_path = get_config('Paths', 'traindir')
    convert(train_path)


def convert_val():
    val_path = get_config('Paths', 'valdir')
    convert(val_path)
