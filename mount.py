#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gunther Seiser <gunther.seiser.63@gmail.com>
# on the basis of Christian Vallentin <mail@vallentinsource.com>
# Website: http://vallentinsource.com
# Repository: https://github.com/MrVallentin/mount.py
#
# Date Created: March 25, 2016
# Last Modified: Feb 3, 2023
#
# Developed and tested using Python 3.9.1
# changes to the original master: compatible in Linux and Windows

# works with Raspi and Debian 11, where USB drives are automounted.
# works on Windows 10


import os
import os.path
import shutil

if os.name == "posix":
    import mount_posix as mnt
else:
    # print ("OS = nt")
    import mount_nt as mnt


def get_usbchoices () ->list:
    """ Choice for SelectField in Forms

    see: Flask Forms 
    """
    devices = mnt.list_media_devices()
    # num_devices = len (devices)
    choices = []
    for device in devices:
        choices.append ((device, mnt.get_label (device)))
    return choices


if __name__ == "__main__":

    devices = mnt.list_media_devices()
    num_devices = len (devices)
    medianum = 0
    if num_devices:
        pass

    
    infotxt = """
    commands:  x = Exit
               # = show this
               u = number of devices
               1,2,3 = number of media to use
               t = mkdir 'test'
               r = shutil.rmtree 'test'
               l = Choices-List
    """
    print (infotxt)
    try:
        i = 1
        while i != 'x':
            i = input ("CMD: ")
            if i == 'u':
                print ("{} Media drives found".format (num_devices))
            elif i == '#':
                print (infotxt)
            elif i == '1':
                medianum = 0
                print ("using {}".format (devices[medianum]))
            elif i == '2':
                medianum = min (1, num_devices-1)
                print ("using {}".format (devices[medianum]))
            elif i == '3':
                medianum = min (2, num_devices-1)
                print ("using {}".format (devices[medianum]))
            elif i == 't':
                if num_devices:
                    dev = devices[medianum]
                    print ("dev: ", dev)
                    mnt.mount (dev)
                    mediapath = mnt.get_media_path (dev)
                    print ("mediapath:", mediapath)
                    testdir = os.path.normpath ( os.path.join (mediapath, "test"))
                    try:
                        os.mkdir (testdir)
                        print ("ok")
                    except FileExistsError:
                        print ("directory 'test' exists already")
                    mnt.unmount (dev)
                else:
                    print ("No media drive found.")
            elif i == 'r':
                if num_devices:
                    dev = devices[medianum]
                    mnt.mount (dev)
                    mediapath = mnt.get_media_path (dev)
                    testdir = os.path.normpath ( os.path.join (mediapath, "test"))
                    try:
                        shutil.rmtree (testdir)
                        print ("ok")
                    except:
                        print ("Error on removing of {}".format (testdir))
                    mnt.unmount (dev)
            elif i == 'l':
                print (get_usbchoices ())
            else:
                pass
    finally:
        print ("exit...")



