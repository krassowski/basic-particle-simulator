# Basic Particle Simulator - what is it?

The basic-particle-simulator is rather a toy than program designed to professional usage.
It allows you to play one of pre-defined simulation scripts (written in python) or to create your own script with embeded editor.

![Preview](https://raw.githubusercontent.com/krassowski/basic-particle-simulator/master/documentation/preview_1.png)

## Who it is designed for?

It may be helpful for everybody with interest in physics and informatics
who is actually finishing a high school or starting undergraduate education.

Also some simulations are ready yet to show during lessons of physcis, so if you are a teacher you can try adopt it to your own needs.

## What can I learn from this?

The simulation engine in this app is not perfect. To be honest is the worst created by the author ever.
But wait a moment! It is a real feature not a bug! Thanks to the simulation showing rather many problems
than fine-tuned animations you can understand the basic issues of writing physics simulation without
need to make all of this mistakes on your own. 

## So what I need to use this program?

### Basic level

If you only want to take a look on existing simulations or modify them slightly, then it will be really easy. 

Only requrements are a basic knowledge in physics along with some computer skills.
It may be quite essentional that you need (at least now) a linux-based system to run it.  

### I you want something more

To understand all the things that works under the mask you need a little bit more knowledge in informatics.

The simulation engine is based on step-by-step procedures, written with use of Object-Oriented Programming.
All of essential engine scripts are in a single file `simulator/simulation.py`.
The scripts are written in Python, thus ability to understand this language will be helpful somehow.

# How to install

## Pre-installation steps

### On Ubuntu/Debian:

`sudo apt-get install python-gi python-gi-cairo gir1.2-gtksource-3.0 gir1.2-gstreamer-0.10 pygobject pygobject2-devel`

and:

`sudo apt-get install python-opengl`
or
`sudo apt-get install pyopengl`

### On Fedora 22:

`sudo dnf install PyOpenGL libX11-devel python-xlib`

(older versions users: use `yum` in place of `dnf`)

## Installation

On the beginning you need to download files. If you have git instaled, type:

`git clone http://github.com/krassowski/basic-particle-simulator`

enter the directory:

`cd basic-particle-simulator`

then type:

`./main.py`

## Any troubles with installation?

If you had problems with OpenGLContext installation, you can try following sources and codes:
 
`http://pyopengl.sourceforge.net/documentation/installation.html
https://python-gtk-3-tutorial.readthedocs.org/en/latest/install.html
	virtualenv oglc-env
	source oglc-env/bin/activate
	pip install PyOpenGL PyOpenGL_accelerate "PyVRML97==2.3.0a4" simpleparse numpy "OpenGLContext==2.2.0a3" pydispatcher pillow`


Feel fee to open an issue on the GitHub, I will take a look on that during my free time.

# Preview

![Preview](https://raw.githubusercontent.com/krassowski/basic-particle-simulator/master/documentation/preview_2.png)
