# Image Resizer

This script allows to resize the image files.

# Quickstart

For script launch need to install Python 3.5 and then install all dependencies:

```bash

$ pip install -r requirements.txt

```

Usage:

```bash

$ python3 image_resize.py -h
usage: image_resize.py [-h] [--width WIDTH] [--height HEIGHT] [--scale SCALE]
                       [--output OUTPUT]
                       filepath

positional arguments:
  filepath         a path to the source image file

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    a width of output image file (in pixels)
  --height HEIGHT  a height of output image file (in pixels)
  --scale SCALE    a scaling coefficient of output image file (should be > 0)
  --output OUTPUT  a directory for saving of output image file

```

**Notes**:

* For image resizing need to given either **scale** or size (**width** and/or **height**)
* If given only either **width** or **height** then resizing of image executes with saving of image proportions
* If **output** directory are not given the saving of resized image executes to the directory with source image file

Examples of script launch on Linux (suppose we have the **some_picture.jpg** source image file with size of **800x600**):

```bash

$ python3 image_resize.py some_picture.jpg --width 700 --height 700
Warning: proportions of source image will not be saved
Resized image successfully saved to some_picture__700x700.jpg

$ python3 image_resize.py some_picture.jpg --width 600 --height 450
Resized image successfully saved to some_picture__600x450.jpg

$ python3 image_resize.py some_picture.jpg --width 500
Resized image successfully saved to some_picture__500x375.jpg

$ python3 image_resize.py some_picture.jpg --height 225
Resized image successfully saved to some_picture__300x225.jpg

$ python3 image_resize.py some_picture.jpg --scale 0.5
Resized image successfully saved to some_picture__400x300.jpg

$ python3 image_resize.py some_picture.jpg --scale 0.25 --output /home/user
Resized image successfully saved to /home/user/some_picture__200x150.jpg

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
