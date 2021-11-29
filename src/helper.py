from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os, time, pathlib
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

def listDirImages(path: str):
    res = []
    exts = ['jpg', 'jpeg', 'webp', 'png']
    files = os.listdir(path)
    for file in files:
        for ext in exts:
            if file.endswith(f'.{ext}')\
                and not file.endswith(f'4x.{ext}'):
                res.append(f'{path}/{file}')
    return res

imgExtantions = ['jpg', 'jpeg', 'png', 'webp']


def reconnect(signal, newhandler=None, oldhandler=None):
    try:
        if oldhandler is not None:
            while True:
                signal.disconnect(oldhandler)
        else:
            signal.disconnect()
    except TypeError:
        pass
    if newhandler is not None:
        signal.connect(newhandler)


def printObj(obj):
    for attr in dir(obj):
        if not attr.startswith('__') and not attr.startswith('set') :
            val = getattr(obj, attr)
            print(f'{attr} = {val}')


def dirOfFile(filePath):
    return pathlib.Path(filePath).parent.resolve()
