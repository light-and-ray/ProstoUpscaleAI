from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import threading, os
from subprocess import Popen, PIPE, STDOUT

import helper, config, errorHandling


class UpscaleOptions:
    def __init__(self, imagePath : str, savePath : str):
        self.imagePath = imagePath
        self.savePath = savePath
        self.fileName = imagePath.split('/')[-1]
        self.ext = None
        self._updateExt()
        self.preScale = 1.0
        # self.postprocessScale = 1.0
        self.denoiseLevel = 0.0
        self.removeJpegArtifacts = True
        self.saveFormat = 'jpg' #if savePath is a directory
        self.saveQuality = 91
        self.realsrNeedX = False
        self.realsrT = 100


    def setImagePath(self, imagePath):
        self.imagePath = imagePath
        self.fileName = imagePath.split('/')[-1]
        self._updateExt()

    def setSavePath(self, savePath):
        self.savePath = savePath

    def setPreScale(self, preScale):
        self.preScale = preScale

    def setDenoiseLevel(self, denoiseLevel):
        self.denoiseLevel = denoiseLevel

    def setRemoveJpegArtifacts(self, removeJpegArtifacts):
        self.removeJpegArtifacts = removeJpegArtifacts

    def setSaveQuality(self, saveQuality):
        self.saveQuality = saveQuality

    def setRealsrNeedX(self, realsrNeedX):
        self.realsrNeedX = realsrNeedX


    def _updateExt(self):
        split = self.fileName.split('.')
        if len(split) != 0:
            ext = split[-1]
            self.ext = ext
            if ext in helper.imgExtantions:
                pos = len(self.fileName) - len(ext) - 1
                self.fileName = self.fileName[:pos]



class _Upscaler:
    def __init__(self, options: UpscaleOptions):
        self.fileIn = options.imagePath
        if options.ext not in helper.imgExtantions:
            self.filePreConverted = f'{config.tmp}/{options.fileName}-preconverted.png'
        else:
            self.filePreConverted = self.fileIn

        if options.preScale != 1.0:
            self.fileScaled = f'{config.tmp}/{options.fileName}-preprocessed.png'
        else:
            self.fileScaled = self.filePreConverted

        if options.denoiseLevel != 0.0:
            self.fileFullDenoised = f'{config.tmp}/{options.fileName}-fullDenoised.png'
            self.fileDenoised = f'{config.tmp}/{options.fileName}-denoised.png'
        else:
            self.fileFullDenoised = None
            self.fileDenoised = self.fileScaled

        self.fileUpscaled = f'{config.tmp}/{options.fileName}-upscaled.png'

        if os.path.isdir(options.savePath):
            self.fileOut = f'{options.savePath}/{options.fileName}-prostoUpscaled.{options.saveFormat}'
        else:
            self.fileOut = options.savePath

        self.options = options
        self.err = None
        self.process = None
        self.percents = None

    def checkError(self):
        if self.err is not None:
            errorHandling.instance.add(self.err)
            return True
        return False


    def run(self):
        if self.options.ext not in helper.imgExtantions:
            self.preConvert()
            if self.checkError(): return

        if self.options.preScale != 1.0:
            self.preScale()
            if self.checkError(): return

        if self.options.denoiseLevel != 0.0:
            self.denoise()
            if self.checkError(): return

        self.upscale()
        if self.checkError(): return

        self.save()


    @staticmethod
    def popen(cmd):
        cmd = map(str, cmd)
        return Popen(cmd, encoding=config.ENCODING, stdout=PIPE, stderr=STDOUT)


    def execCmd(self, cmd, errPrefix):
        p = self.popen(cmd)
        print('[execCmd]', cmd)
        self.process = p
        for line in p.stdout:
            print(f'[execCmd] {line}', end='')
        data = p.communicate()[0]
        if p.returncode != 0:
            self.err = f'{errPrefix} [{p.returncode}]: {data}'
        self.process = None

    def preConvert(self):
        self.execCmd([config.convert, '-verbose', self.fileIn, self.filePreConverted], 'preconvert error')


    def preScale(self):
        self.execCmd([config.convert, '-verbose', '-resize', f'{self.options.preScale * 100}%',
                self.filePreConverted, self.fileScaled], 'preScale error')


    def denoise(self):
        self.execCmd([config.convert, '-verbose', '-enhance', self.fileScaled, self.fileFullDenoised],
            'denoise convert -enhance error')
        if self.checkError(): return
        self.execCmd([config.composite, '-blend', self.options.denoiseLevel * 100,
            self.fileFullDenoised, self.fileScaled, self.fileDenoised],
            'denoise composite -blend error')


    def upscale(self):
        self.percents = 0.00
        x = '-x' if self.options.realsrNeedX else ''
        model = config.modelJpeg if self.options.removeJpegArtifacts else config.model
        p = self.popen([config.realsr, x, '-t', self.options.realsrT,
                '-m', model, '-i', self.fileDenoised,
                '-o', self.fileUpscaled])
        self.process = p
        for line in p.stdout:
            print(f'[upscale] {line}', end='')
            if line.endswith('%\n'):
                self.percents = float(line[:-2])

            if line.startswith('WARNING: lavapipe is not a conformant vulkan implementation, testing use only.'):
                errorHandling.instance.add("Your system doesn't spport Vilkan Api")
                self.err = 1
                p.kill()
                break

        self.percents = 100.00
        self.process = None

    def save(self):
        self.execCmd([config.convert, '-quality', self.options.saveQuality,
                self.fileUpscaled, self.fileOut], 'save fileOut error')






class UpscaleRunner:
#public:
    def __init__(self):
        self.init()

    def init(self):
        self._complete = False
        self._process = None
        self._done = False
        self._upscaler = None
        self.percents = 0.00
        self.inProcess = None
        self.err = 0


    def run(self, options: UpscaleOptions):
        helper.printObj(options)
        self.init()
        self._upscaler = _Upscaler(options)
        self._thread = threading.Thread(target=self._run)
        self._thread.start()


    def kill(self):
        if not self._done and self._upscaler is not None and self._upscaler.process is not None:
            print('killing')
            self._done = True
            self._upscaler.process.terminate()
            # self._process.kill()
            self._upscaler.process = None
            self._thread.join()
            print('killed')


    def complete(self):
        complete = self._complete and not self._done
        if complete:
            self._done = True
        return complete


    def getPercents(self):
        if self._upscaler is None:
            return None
        return self._upscaler.percents


    def setPercents(self, per):
        self._upscaler.percents = per


#private:

    def _run(self):

        self.inProcess = True

        self._upscaler.run()

        self._complete = True
        self.inProcess = False
