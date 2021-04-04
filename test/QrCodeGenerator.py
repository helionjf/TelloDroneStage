import qrcode
from PIL import Image

img = qrcode.make('demo1')
img.save("try1.png")
