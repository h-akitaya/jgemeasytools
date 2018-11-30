# jgemtools
Support tools for J-GEM project

# Requirements

* Python3
* numpy, astropy, etc.

# Setup
## append package path to your $PATH shell variable (if necessary).
## Create user/password file for Planner/Image Server.
    $ ./mkpasswdfile.py
    User: user
    Password: xxxx
## Edit observatory/instrument information in *jgeminfo.py*

# Usage
## interactive planner viewer
    $ ./jgemobs.py -i  # for playground
    $ ./jgemobs.py -i --planner # for actual event planner

## image uploader to Image Server
    $ ./uploadfile.py xxxxxx.fits

## candidates sky mapper (under construction)
    $ ./jgemskymap.py
