import os, pathlib, time

TIMEOUT_BEFORE_UPSCALE = 900
BLACKOUT_OPACITY = 0.6
MOVE_SCALE = 3

defaultOpenDirectory = os.environ['HOME']

root = pathlib.Path(__file__).parent.parent.resolve()
tmp = f'{root}/tmp'
bin = f'{root}/bin'
realsr = f'{bin}/realsr-ncnn-vulkan'
convert = f'{bin}/convert'
modelJpeg = f'{bin}/realsr-ncnn-vulkan-models/models-DF2K_JPEG'
model = f'{bin}/realsr-ncnn-vulkan-models/models-DF2K'

