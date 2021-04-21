# TelloDroneStage

youtube url: https://youtu.be/2l2CBuHc2kU

## Installation

### Windows Python Install
1. In first please install [python](https://www.python.org/downloads/). The site will detect that you are on Windows and the version you are using: it will then display the appropriate Windows installer.
2. Choose the 3.9.4 python version to run the app.
3. Run the installer after the download is complete. Click on the desired version button and the installer download will begin. Once on your hard drive, run it.
4. Check the Add Python 3.x.x to PATH checkbox. This will allow you to run Python directly from the command prompt.
5. Click Install Now. Python is then installed with all of its default settings, which are more than sufficient for most users.
6. Python is now installed.

For Windows, you need to install [c++](https://www.microsoft.com/fr-FR/download/details.aspx?id=40784) for the QRCode option.
So now go to the repository folder with a terminal and then use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirement.
```Bash
pip install -r requirement.txt
```
Here is ! You can now check the [usage](https://github.com/despire907/TelloDroneStage#usage) to know the all possibility's of the project.
### Linux Python Install
TODO

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