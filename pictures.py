import PySimpleGUI as sg
import os.path
import PIL.Image
import io
import base64
from utils.config_tools import get_config


# from https://pysimplegui.readthedocs.io/en/latest/cookbook/
def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def listbox_values():
    folder = get_config('Common','dir') + '/runs/detect/exp/'
    print(folder)
    try:
        file_list = os.listdir(folder) 
    except:
        file_list = []
    fnames = [f for f in file_list if os.path.isfile(
        os.path.join(folder, f)) and f.lower().endswith((".jpg"))]
    print(fnames)
    return fnames


def pictures_window():
    # --------------------------------- Define Layout ---------------------------------
    folder = get_config('Common','dir') + '/runs/detect/exp/'
    left_col = [[sg.Text('Folder'), sg.Input(default_text=folder, size=(30,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
                [sg.Listbox(values=listbox_values(), enable_events=True, size=(40,61),key='-FILE LIST-')],]

    images_col = [[sg.Text(size=(100,1), key='-TOUT-')],
                [sg.Image(key='-IMAGE-', pad=(30,15),),]]

    # ----- Full layout -----
    layout = [[sg.Column(left_col, vertical_alignment='top', element_justification='up'), sg.VSeperator(),sg.Column(images_col, element_justification='c')]]

    # --------------------------------- Create Window ---------------------------------
    window = sg.Window('Detected data view', layout,resizable=False, size=(1800,1000))
    # --------------------------------- Event Loop ---------------------------------
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-FOLDER-':                         
            folder = values['-FOLDER-']
            try:
                file_list = os.listdir(folder) 
            except:
                file_list = []
            fnames = [f for f in file_list if os.path.isfile(
                os.path.join(folder, f)) and f.lower().endswith((".jpg"))]
            window['-FILE LIST-'].update(fnames)
        elif event == '-FILE LIST-':   
            try:
                filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
                window['-TOUT-'].update(filename)
                new_size = None
                window['-IMAGE-'].update(data=convert_to_bytes(filename, resize=new_size))
            except Exception as E:
                print(f'** Error {E} **')
                pass
    # --------------------------------- Close & Exit ---------------------------------
    window.close()
