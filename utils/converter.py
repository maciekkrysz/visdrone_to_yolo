import struct
import imghdr
import os
import time

# Place this script in a folder together with "annotations" folder containing VisDrone format labels
# and a folder "lables" that darknet format labels will be put into


def get_point_between_points(p1, p2):

    x = p1[0] + 0.5 * (p2[0] - p1[0])
    y = p1[1] + 0.5 * (p2[1] - p1[1])

    return [x, y]


def get_image_size(fname):
    # Determine the image type of fhandle and return its size. From draco.
    with open(fname, 'rb') as fhandle:
        try:
            fhandle.seek(0)  # Read 0xff next
            size = 2
            ftype = 0
            while not 0xc0 <= ftype <= 0xcf:
                fhandle.seek(size, 1)
                byte = fhandle.read(1)
                while ord(byte) == 0xff:
                    byte = fhandle.read(1)
                ftype = ord(byte)
                size = struct.unpack('>H', fhandle.read(2))[0] - 2
            # We are at a SOFn block
            fhandle.seek(1, 1)  # Skip `precision' byte.
            height, width = struct.unpack('>HH', fhandle.read(4))
        except Exception:  # IGNORE:W0703
            return
        return width, height


def convert(path='./'):
    a = os.system(f'rm -r -f {path}/labels')
    a = os.system(f'mkdir {path}/labels')
    for filename in os.listdir(f'{path}/annotations'):
        a = os.system(f'> {path}/labels/{filename}')
        with open(str(f"{path}/annotations/{filename}"), "r") as file1:
            with open(str(f"{path}/labels/{filename}"), "w") as file2:
                for line in file1:
                    cline = line.split(",")
                    filename = filename.replace("txt", "jpg")
                    size = get_image_size(str(f"{path}/images/" + filename))
                    x, y = get_point_between_points((int(cline[0]), int(cline[1])), (int(
                        cline[0]) + int(cline[2]), int(cline[1]) + int(cline[3])))

                    cline[0] = x / size[0]
                    cline[1] = y / size[1]

                    cline[2] = int(cline[2]) / size[0]
                    cline[3] = int(cline[3]) / size[1]

                    print(int(cline[5]), f'{cline[0]:.6f}', f'{cline[1]:.6f}',
                          f'{cline[2]:.6f}', f'{cline[3]:.6f}', sep=" ", end="\n", file=file2)
