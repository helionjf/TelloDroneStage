# TelloDroneStage

youtube url: https://youtu.be/2l2CBuHc2kU

## Installation

Use the package manager [pip](https://pip.pypa.io/fr/stable/) to install the requirement

```bash
pip install -r requirement.txt
```

## Usage

### Control drone with keyboard

This first program is to control the tello drone with your keyboard.
In first connect drone wifi to your computer and then run this command on the root directory.

```bash
python test/test.py 
```

#### Keyboard usage

Z: go up

S: go down

Q: rotate clockwise

D: rotate counter clockwise

UP Arrow: go forward

Down Arrow: go backward

Left Arrow: go left

Right Arrow: go right

A: land

E: takeoff

### FaceTracking with drone

This second program is to control the tello drone with your face.
In first connect drone wifi to your computer and then run this command on the root directory.
This program doesn't work very well.

```bash
python test/FaceTrackingTest.py
```

### QRCode with drone

this third program is to control the tello drone with QRCode.
In first connect drone wifi to your computer and then run this command on the root directory.

```bash
python test/QrCodeTracking.py
```

This program need QRCode to do something. So go to the test/Ressources/QRCode/ and take one or more QRCode.
You simply need to show the QRCode to the drone and the drone do the QRCode command.

### Application to control drone

This program is to control the tello drone with button and keyboard.
In first connect drone wifi to your computer and then run this command.

```bash
python app/core.py
```