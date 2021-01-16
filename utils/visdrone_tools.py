from utils.download_tools import download_file_from_google_drive, unzip
from utils.converter import convert
import os

train_data_id = '1a2oHjcEcwXP8oUF95qiwrqzACb2YlUhn'
val_data_id = '1bxK5zgLn0_L8x276eKkuYA_FzwCIjb59'
train_zip_path = "./train.zip"
val_zip_path = "./val.zip"


def download_train_google():
    download_file_from_google_drive(train_data_id, train_zip_path)


def download_val_google():
    download_file_from_google_drive(val_data_id, val_zip_path)
    

def unzip_train():
    unzip(train_zip_path)
    exctract_from_visdrone_to_dir('./train')


def unzip_val():
    unzip(val_zip_path)
    exctract_from_visdrone_to_dir('./val')


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
    convert('./train')


def convert_val():
    convert('./val')
