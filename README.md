# jgemtools
Support tools for J-GEM project

# Requirements

* Python3
* numpy, astropy, etc.

# Setup
1. append package path to your $PATH shell variable (if necessary).
2. Create user/password file for Planner/Image Server.
    $ ./mkpasswdfile.py
    User: user
    Password: xxxx
3. Edit observatory information in *jgeminfo.py*

# Usge
## interactive planner viewer
    $ ./jgemobs.py -i  # for playground
    $ ./jgemobs.py -i --planner # for actual event planner

## image uploader to Image Server
    $ ./uploadfile.py xxxxxx.fits

## candidates sky mapper (under construction)
    $ ./jgemskymap.py
