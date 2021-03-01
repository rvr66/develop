#  Vaccine Finder App

* [General info](#general-info)
* [Commands](#commands)

##  General info

Finds available vaccines in a given zip/state from multiple sources and notifies appropriately about availability thorugh a easy-to-use GUI interface. 

## Commands

With Python

Install Python for Windows and at the end make sure to select the following to be installed:

<img src="https://i.stack.imgur.com/GSWfw.png" alt="optional features that are required for this to work"/>

Once Python installation is done, open CMD and run the following commands:

pip install requests

pip install pgeocode

If pip does not work, use pip3

To start the program run:

python <location of file ex. C:/Desktop/vaccine_finder.py>

With Docker:

$ docker pull madirajurv/develop:vaccine_finder

$ docker run --rm --network=host --privileged -v /dev:/dev  -e DISPLAY=$DISPLAY  -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority -it madirajurv/develop:vaccine_finder
