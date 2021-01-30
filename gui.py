import PySimpleGUI as sg
from json import (load as jsonload, dump as jsondump)
from os import path
from utils.config_tools import *
from main import start_app
from pictures import pictures_window


DEFAULT_SETTINGS = {'dir': 'dir', 
                    'valdir': 'valdir' , 
                    'traindir': 'traindir' , 
                    'yolodir': 'yolodir', 
                    'imagesdir': 'imagesdir', 
                    'datayaml' : 'datayaml', 
                    'trainyaml': 'trainyaml',
                    'traindataid': 'traindataid' , 
                    'valdataid': 'valdataid', 
                    'yololink' : 'yololink', 
                    'epochs': 'epochs',
                    'batchsize': 'batchsize' , 
                    'workers': 'workers', 
                    'devices': 'devices', 
                    'name' : 'name', 
                    'confidence' : 'confidence', 
                    'imgsize': 'imgsize',
                    'weights': 'weights',
                    'trainset': 'trainset' , 
                    'valset': 'valset', 
                    'yolo' : 'yolo', 
                    'train' : 'train', 
                    'detect': 'detect',
                    }
                    
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'dir': 'dir', 
                                'valdir': 'valdir' , 
                                'traindir': 'traindir' , 
                                'yolodir': 'yolodir', 
                                'imagesdir': 'imagesdir', 
                                'datayaml' : 'datayaml', 
                                'trainyaml': 'trainyaml',
                                'traindataid': 'traindataid' , 
                                'valdataid': 'valdataid', 
                                'yololink' : 'yololink', 
                                'epochs': 'epochs',
                                'batchsize': 'batchsize' , 
                                'workers': 'workers', 
                                'devices': 'devices', 
                                'name' : 'name', 
                                'confidence' : 'confidence', 
                                'imgsize': 'imgsize',
                                'weights': 'weights',
                                'trainset': 'trainset' , 
                                'valset': 'valset', 
                                'yolo' : 'yolo', 
                                'train' : 'train', 
                                'detect': 'detect',
                                }


##################### Load/Save Settings File #####################
def load_settings(default_settings): 
    settings = default_settings
    save_settings(settings, None)
    return settings


def save_settings(settings, values):
    if values:
        for section in get_sections():
            for key, value in get_params(section):
                try:
                    set_config(section, key, str(values[key]))
                except Exception as e:
                    print(f'Problem updating settings from window values. Key = {key}')

        sg.popup('Settings saved')

##################### Make a settings window #####################
def create_settings_window(settings):

    def TextLabel(text): return sg.Text(text+':', justification='l', size=(30,1))

    layout = [  [sg.Text('Settings', font='Any 15')],
                [sg.Text('Files', font='Any 13')],
                [TextLabel('Main dir'), sg.Input(key='dir'), sg.FolderBrowse(target='dir')],
                [TextLabel('Train data dir'),sg.Input(key='traindir'), sg.FolderBrowse(target='traindir')],
                [TextLabel('Val data dir'),sg.Input(key='valdir'), sg.FolderBrowse(target='valdir')],
                [TextLabel('Yolo Dir'),sg.Input(key='yolodir'), sg.FolderBrowse(target='yolodir')],
                [TextLabel('Test images dir'),sg.Input(key='imagesdir'), sg.FolderBrowse(target='imagesdir')],
                [TextLabel('data.yaml dir'),sg.Input(key='datayaml'), sg.FolderBrowse(target='datayaml')],
                [TextLabel('train.yaml dir'),sg.Input(key='trainyaml'), sg.FolderBrowse(target='trainyaml')],
                [sg.Text('Download data', font='Any 13')],
                [TextLabel('Train data google drive Id'), sg.Input(key='traindataid')],
                [TextLabel('Val data google drive Id'), sg.Input(key='valdataid')],
                [TextLabel('Yolo git link'), sg.Input(key='yololink')],
                [sg.Text('Yolo training', font='Any 13')],
                [TextLabel('Weights'), sg.Input(key='weights'), sg.FolderBrowse(target='weights')],
                [TextLabel('Epochs'), sg.Input(key='epochs')],
                [TextLabel('Batch size'), sg.Input(key='batchsize')],
                [TextLabel('Workers'), sg.Input(key='workers')],
                [TextLabel('Devices (CPU/GPU:(0/1/2/3)'), sg.Input(key='devices')],
                [TextLabel('Name of dir results'), sg.Input(key='name')],
                [TextLabel('object confidence threshold'), sg.Input(key='confidence')],
                [TextLabel('Img size'), sg.Input(key='imgsize')],
                [sg.Text('Steps', font='Any 13')],
                [TextLabel('Download trainset'), sg.Checkbox(text='', key='trainset')],
                [TextLabel('Download valset'), sg.Checkbox(text='', key='valset')],
                [TextLabel('Download and compile Yolo'), sg.Checkbox(text='', key='yolo')],
                [TextLabel('Train data'), sg.Checkbox(text='', key='train')],
                [TextLabel('Detect from images dir'), sg.Checkbox(text='', key='detect')],
                [sg.Button('Save'), sg.Button('Exit')]  ]

    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)
    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
        for section in get_sections():
            for key, value in get_params(section):
                try:
                    param = get_config(section, key)
                    if param == 'True':
                        param = True
                    elif param == 'False':
                        param = False
                    window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=param)
                except Exception as e:
                    print(f'Problem updating PySimpleGUI window from settings. Key = {key}')

    return window

##################### Main Program Window & Event Loop #####################
def create_main_window(settings):
    layout = [[sg.T('Yolo automation training')],
              [sg.T('Change settings or start this app')],
              [sg.B('Exit'), sg.B('Change Settings'), sg.B('Start')]]

    return sg.Window('Main Application', layout)


def main():
    set_config('Common', 'Dir', path.dirname(__file__))
    window, settings = None, load_settings(DEFAULT_SETTINGS)
    while True:        
        if window is None:
            window = create_main_window(settings)

        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Change Settings':
            event, values = create_settings_window(settings).read(close=True)
            if event == 'Save':
                window.close()
                window = None
                save_settings(settings, values)
        if event == 'Start':
            window.close()  
            start_app()
            pictures_window()
    window.close()

if __name__ == '__main__':
    main()