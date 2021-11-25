from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os, pathlib, time
from subprocess import Popen, PIPE, STDOUT

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

root = pathlib.Path(__file__).parent.parent.resolve()
tmp = f'{root}/tmp'
realsr = f'{root}/bin/realsr-ncnn-vulkan'
modelJpeg = f'{root}/bin/realsr-ncnn-vulkan-models/models-DF2K_JPEG'
model = f'{root}/bin/realsr-ncnn-vulkan-models/models-DF2K'


def execCmd(cmd):
    print(cmd)
    with Popen(cmd, stdout=PIPE, bufsize=1,
        universal_newlines=True, shell=True) as p:
        for line in p.stdout:
            print(f'[execCmd] {line}', end='')

def cropImage(pathIn, pathOut, x, y, w, h):
    execCmd(f'convert "{pathIn}" -crop {w}x{h}+{x}+{y} -quality 100 "{pathOut}"')


def currentTime():
    return round(time.time() * 1000)
