[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!-- Project Intro -->
<br />
<p align="center">
    <a href="https://github.com/despire907/TelloDroneStage">
        <img src="images/logo.png" alt="Logo" width="80" height="80">
    </a>
    <h3 align="center">TelloDrone Stage</h3>
    <p align="center">
        A project to control your Tello Drone !
        <br />
        <a href="https://github.com/despire907/TelloDroneStage/issues">Report Bug</a>
        ·
        <a href="https://github.com/despire907/TelloDroneStage/issues">Request Feature</a>
    </p>
</p>

<!-- Table of Contents -->
<details open="open">
    <summary>Table of Contents</summary>
    <ol>
        <li>
            <a href="#about-the-project">About The Project</a>
            <ul>
                <li><a href="#build-with">Build With</a> </li>
            </ul>
        </li>
        <li>
            <a href="#getting-started">Getting Started</a>
            <ul>
                <li><a href="#prerequisites">Prerequisites</a></li>
                <li>
                    <a href="#installation">Installation</a>
                    <ul>
                        <li><a href="#windows-installation">Windows Installation</a></li>
                        <li><a href="#linux-installation">Linux Installation</a></li>
                        <li><a href="#raspberry-installation">Raspberry Installation</a></li>
                    </ul>
                </li>
            </ul>
        </li>
        <li>
            <a href="#usage">Usage</a>
            <ul>
                <li><a href="#app-usage">Control App Usage</a></li>
                <li><a href="#qrcode-app-usage">QRCode App Usage</a></li>
                <li><a href="#swarm-app-usage">Swarm App Usage</a></li>
                <li><a href="#test-usage">All Test Usage</a></li>
            </ul>
        </li>
    </ol>
</details>

<!-- About The Project -->
## About The Project

This project was carried out in the context of an internship at Orange DTSI under the supervision of Jean-François Helion.
The goal of this project is to provide an easier way to control your Tello edu drone as well as to add some pacage option.
This was carried out over the period from April 2021 to September 2021.

### Build With

All the frameworks used in this project are contained in the requirements.txt, please refer to it.
<br />Some essential framework of the project:

<a href="https://pypi.org/project/djitellopy/">Djitellopy</a>
<br />
<a href="https://kivy.org/#home">Kivi</a>
<br />
<a href="https://pypi.org/project/opencv-python/">OpenCv</a>
<br />
<a href="https://pypi.org/project/pyzbar/">Pyzbar</a>

<!-- youtube url: https://youtu.be/2l2CBuHc2kU -->


## Getting Started

Here is a brief explanation of how to install and use the project

### Prerequisites

For the prerequisite of this project, you need [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/).
<br/>If you don't have python installed please follow the next steps depending on your operating system. 
<br/>[Windows](#windows-installation) · [Linux](#linux-installation) · [Raspberry](#raspberry-installation)
<br/>If python is already installed, you just need to run this command:
<br/>
```Bash
pip install -r requirements.txt
```

###Installation

#### Windows Installation
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
#### Linux Installation
TODO

#### Raspberry Installation 
TODO

## Usage

###Control App Usage

This first application will allow you to control a tello edu drone by wifi connection. At first you will have to connect the drone by wifi to your computer, then you can launch the following command in a terminal at the root of the project.

```Bash
python app/core.py
```
Once done, you should see several buttons appear on the page. Here is a small explanation of each button:
<br/><img src="app/Resources/img/icons8-back-50.png" alt="Move Left"> This button allows you to move to the left
<br/><img src="app/Resources/img/icons8-forward-50.png" alt="Move Right"> This button allows you to move to the right



<!--
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
-->