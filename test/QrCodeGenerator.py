import qrcode
from PIL import Image

img = qrcode.make('demo2')
img.save("try2.png")
