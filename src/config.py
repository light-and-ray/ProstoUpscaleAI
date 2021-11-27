import os, pathlib, time

TIMEOUT_BEFORE_UPSCALE = 900
DEFAULT_PICTURE = 'photo.jpg'
BLACKOUT_OPACITY = 0.6
MOVE_SCALE = 3

defaultOpenDirectory = os.environ['HOME']

root = pathlib.Path(__file__).parent.parent.resolve()
tmp = f'{root}/tmp'
realsr = f'{root}/bin/realsr-ncnn-vulkan'
convert = f'convert'
modelJpeg = f'{root}/bin/realsr-ncnn-vulkan-models/models-DF2K_JPEG'
model = f'{root}/bin/realsr-ncnn-vulkan-models/models-DF2K'

