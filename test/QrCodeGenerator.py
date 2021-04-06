import qrcode
from PIL import Image

# permet de créer un qrcode avec un string

img = qrcode.make('demo2')
img.save("try2.png")
