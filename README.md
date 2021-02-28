#  Vaccine Finder App

* [General info](#general-info)
* [Commands](#commands)

##  General info

Finds available vaccines in a given zip/state from multiple sources and notifies appropriately about availability thorugh a easy-to-use GUI interface. 

## Commands

With Python

Install Python for Windows and at the end make sure to select the following to be installed:

<img src="https://i.stack.imgur.com/GSWfw.png" alt="optional features that are required for this to work"/>

Once Python installation is done, open CMD and run the following command:

pip install requests
pip install pgeocode

If pip does not work, use pip3

With Docker:

$ docker pull madirajurv/develop:text_comparison

$ docker run -d -p 5000:5000 madirajurv/develop:text_comparison
