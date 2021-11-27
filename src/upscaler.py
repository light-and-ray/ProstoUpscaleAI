from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import threading, io
from subprocess import Popen, PIPE, STDOUT

import helper, config

class Upscaler():
#public:
    def __init__(self):
        self.init()

    def init(self):
        self._complete = False
        self._process = None
        self._done = False
        self.percents = 0
        self.showBlackout = None


    def run(self, pathIn, pathOut):
        self.init()
        self._thread = threading.Thread(target=lambda: self._run(pathIn, pathOut))
        self._thread.start()


    def kill(self):
        if not self._done and self._process is not None:
            print('killing')
            self._done = True
            self._process.terminate()
            # self._process.kill()
            self._process = None
            self._thread.join()
            print('killed')


    def complete(self):
        complete = self._complete and not self._done
        if complete:
            self._done = True
        return complete

#private:

    def _run(self, pathIn, pathOut):
        self.percents = 0.00
        self.showBlackout = True
        cmd = f'"{config.realsr}" -t 100 -m "{config.modelJpeg}" -i "{pathIn}" -o "{pathOut}"'
        print(cmd)

        with Popen('exec ' + cmd, shell=True, stdout=PIPE, stderr=STDOUT, encoding='utf-8') as p:
            self._process = p
            for line in p.stdout:
                print(f'[dummyUpscale] {line}', end='')
                if line.endswith('%\n'):
                    self.percents = float(line[:-2])

        self.percents = 100.00
        self._complete = True
        self.showBlackout = False
