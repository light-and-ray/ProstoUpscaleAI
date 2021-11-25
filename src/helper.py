from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os, pathlib, io
from subprocess import Popen, PIPE, STDOUT

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def root():
    return pathlib.Path(__file__).parent.parent.resolve()

def execCmd(cmd):
    print(cmd)
    with Popen(cmd, stdout=PIPE, bufsize=1,
        universal_newlines=True, shell=True) as p:
        for line in p.stdout:
            print(f'[execCmd] {line}', end='')

def cropImage(pathIn, pathOut, x, y, w, h):
    execCmd(f'convert "{pathIn}" -crop {w}x{h}+{x}+{y} -quality 100 "{pathOut}"')

def dummyUpscaleGenerator(pathIn, pathOut):
    def generator():
        realsr = f'{root()}/realsr/realsr-ncnn-vulkan'
        model = f'{root()}/realsr/realsr-ncnn-vulkan-models/models-DF2K_JPEG'
        cmd = f'"{realsr}" -t 100 -m "{model}" -i "{pathIn}" -o "{pathOut}"'

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        for line in io.TextIOWrapper(p.stdout, encoding='utf-8'):
            print(f'[dummyUpscale] {line}', end='')
            if line.endswith('%\n'):
                yield float(line[:-2])
        print('dummyUpscale complete')

    return generator
