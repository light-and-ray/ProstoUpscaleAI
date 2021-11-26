from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os, time
from subprocess import Popen, PIPE, STDOUT

import config

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def execCmd(cmd):
    print(cmd)
    with Popen(cmd, stdout=PIPE, bufsize=1,
        universal_newlines=True, shell=True) as p:
        for line in p.stdout:
            print(f'[execCmd] {line}', end='')

def cropImage(pathIn, pathOut, x, y, w, h):
    execCmd(f'{config.convert} "{pathIn}" -crop {w}x{h}+{x}+{y} -quality 100 "{pathOut}"')


def currentTime():
    return round(time.time() * 1000)

def filenameByPath(path: str):
    return path.split('/')[-1]

def fileUrlToPath(url: str):
    urlPrefix = 'file://'
    if url.startswith(urlPrefix):
        return url[len(urlPrefix):]
    else:
        return url
