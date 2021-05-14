import qrcode

# permet de créer un qrcode avec un string

img = qrcode.make('stop')
img.save("stop.png")
