import os, pathlib

TIMEOUT_BEFORE_UPSCALE = 900
BLACKOUT_OPACITY = 0.6
MOVE_SCALE = 3
ENCODING = 'utf-8'
TERMINATED_ERROR_CODES = [-15, 15]

defaultOpenDirectory = os.environ['HOME']

root = pathlib.Path(__file__).parent.parent.resolve()
tmp = f'{root}/tmp'
bin = f'{root}/bin'
realsr = f'{bin}/realsr-ncnn-vulkan'
convert = f'{bin}/convert'
composite = f'{bin}/composite'
modelJpeg = f'{bin}/realsr-ncnn-vulkan-models/models-DF2K_JPEG'
model = f'{bin}/realsr-ncnn-vulkan-models/models-DF2K'

