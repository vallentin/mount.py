#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Christian Vallentin <mail@vallentinsource.com>
# Website: http://vallentinsource.com
# Repository: https://github.com/MrVallentin/mount.py
#
# Date Created: March 25, 2016
# Last Modified: March 2, 2023
#
# Developed and tested using Python 3.9.1
# changes to the original master: use pmount instead of mount.
# therefore no need of sudo rights. 
# works with Raspi and Debian 11, where USB drives are automounted.

import os
import time


def list_media_devices():
    # If the major number is 8, that indicates it to be a disk device.
    #
    # The minor number is the partitions on the same device:
    # - 0 means the entire disk
    # - 1 is the primary
    # - 2 is extended
    # - 5 is logical partitions
    # The maximum number of partitions is 15.
    #
    # Use `$ sudo fdisk -l` and `$ sudo sfdisk -l /dev/sda` for more information.
    with open("/proc/partitions", "r") as f:
        devices = []
        
        for line in f.readlines()[2:]: # skip header lines
            words = [ word.strip() for word in line.split() ]
            minor_number = int(words[1])
            device_name = words[3]
            
            if (minor_number % 16) == 0:
                path = "/sys/class/block/" + device_name
                
                if os.path.islink(path):
                    if os.path.realpath(path).find("/usb") > 0:
                        devices.append("/dev/" + device_name)
        
        return devices


def get_device_name(device):
    """ returns str, i.e. sdb 
    
    device: i.e. /dev/sdb
    """
    return os.path.basename(device)

def get_device_block_path(device):
    return "/sys/block/%s" % get_device_name(device)

def get_media_path(device):
    """ full path of media drive
    
    device: i.e. sdb, /dev/sdb, /media/gunther/GS-USB
    return: is a subdir in case of Automount (Debian)!
        i.e. /media/sdb1 oder /media/gunther/GS_2GB
    """
    os.system ("pmount > output")
    # device already mounted:
    with open ("output", "r") as f:
        for line in f:
            data = line.split ()
            if  device in data[0] or device == data[2]:
                try:
                    os.remove ("output")
                except:
                    # busy error occurred
                    pass
                return data[2]
    # device not mounted:
    try:
        os.remove ("output")
    except:
        # busy error occurred
        pass
    return "/media/" + device + "1"
    

def is_mounted(device):
    return os.path.ismount(get_media_path(device))


def mount_partition(partition, name="usb"):
    path = get_media_path(name)
    if not is_mounted(path):
        os.system (f"pmount {partition}")
        # os.system("sudo mkdir -p " + path)
        # os.system("sudo mount %s %s -o iocharset=iso8859-1,uid=%s" % (partition, path, user))

def unmount_partition(name="usb"):
    path = get_media_path(name)
    if is_mounted(path):
        # possible 'target is busy' Error:
        ret = 1
        while ret:
            time.sleep (0.5)
            ret = os.system (f"pumount {path}")
        print ("pumount ok")
        # os.system("sudo umount " + path)
        #os.system("rm -rf " + path)


def mount(device, name=None):
    if not name:
        # name = get_device_name(device)
        name = os.path.basename(device)
    else:
        name = os.path.basename (name)
    
    mpath = get_media_path (name)
    if not is_mounted(mpath):
        partition = device + "1"
        os.system (f"pmount {partition}")
    # mount_partition(get_partition(device), name)

def unmount(device, name=None):
    if not name:
        name = get_device_name(device)
    unmount_partition(name)


def is_removable(device):
    path = get_device_block_path(device) + "/removable"
    
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip() == "1"
    
    return None


def get_size(device):
    path = get_device_block_path(device) + "/size"
    
    if os.path.exists(path):
        with open(path, "r") as f:
            # Multiply by 512, as Linux sectors are always considered to be 512 bytes long
            # Resource: https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121
            return int(f.read().strip()) * 512
    
    return -1


def get_model(device):
    path = get_device_block_path(device) + "/device/model"
    
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return None

def get_vendor(device):
    path = get_device_block_path(device) + "/device/vendor"
    
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return None

def get_label(device:str, devlist:list=None) ->str:
    """ benutzerfreundlicher String zur Identifizierung von device
    """
    name  = get_device_name(device)
    model = get_model(device)
    size  = "%.2f" % (get_size(device) / 1024 ** 3)
    return name + ", " + model + ", " + size + " GB"


if __name__ == "__main__":
    devices = list_media_devices()
    print ("Devices:", devices)
    
    for device in devices:
        mount(device)
        
        print("Drive:", get_device_name(device))
        print("Mounted:", "Yes" if is_mounted(device) else "No")
        print("Removable:", "Yes" if is_removable(device) else "No")
        print("Size:", get_size(device), "bytes")
        print("Size:", "%.2f" % (get_size(device) / 1024 ** 3), "GB")
        print("Model:", get_model(device))
        print("Vendor:", get_vendor(device))
        print(" ")
        
        unmount(device)
