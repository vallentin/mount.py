#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gunther Seiser, gunther.seiser.63@gmail.com
#
# Date Created: Aug 30, 2020
# Last Modified: Feb 3, 2023
#
# Developed and tested using Python 3.9.1
# compatible functions to mount_posix.py

import os
import os.path
import wmi
import pythoncom

DRIVE_TYPES = {0 : "Unknown",
    1 : "No Root Directory",
    2 : "Removable Disk",
    3 : "Local Disk",
    4 : "Network Drive",
    5 : "Compact Disc",
    6 : "RAM Disk"
    }


def list_drive_devices () ->list:
    """ alle Laufwerke auflisten 
    Liste aus drive-Objekten
    """
    devices = []
    c = wmi.WMI ()
    for drive in c.Win32_LogicalDisk ():
        devices.append (drive)
    return devices

def drive_properties (devlist) -> "print":
    """ list all properties """
    for device in devlist:
        print ("Availability: ", device.Availability)
        print ("BlockSize: ", device.BlockSize , " Caption: ", device.Caption )
        print ("Compressed: ", device.Compressed , " ConfigManagerErrorCode: ", device.ConfigManagerErrorCode )
        print ("ConfigManagerUserConfig: ", device.ConfigManagerUserConfig , " CreationClassName: ", device.CreationClassName )
        print ("Description: ", device.Description , " DeviceID: ", device.DeviceID )
        print ("DriveType: ", device.DriveType , " ErrorCleared: ", device.ErrorCleared )
        print ("ErrorDescription: ", device.ErrorDescription , " ErrorMethodology: ", device.ErrorMethodology )
        print ("FileSystem: ", device.FileSystem , " FreeSpace: ", device.FreeSpace )
        print ("InstallDate: ", device.InstallDate , " LastErrorCode: ", device.LastErrorCode )
        print ("MaximumComponentLength: ", device.MaximumComponentLength , " MediaType: ", device.MediaType )
        print ("Name: ", device.Name , " NumberOfBlocks: ", device.NumberOfBlocks )
        print ("PNPDeviceID: ", device.PNPDeviceID , " PowerManagementSupported: ", device.PowerManagementSupported )
        print ("ProviderName: ", device.ProviderName , " Purpose: ", device.Purpose )
        print ("QuotasDisabled: ", device.QuotasDisabled , " QuotasIncomplete: ", device.QuotasIncomplete )
        print ("QuotasRebuilding: ", device.QuotasRebuilding , " Size: ", device.Size )
        print ("Status: ", device.Status , " StatusInfo: ", device.StatusInfo )
        print ("SupportsDiskQuotas: ", device.SupportsDiskQuotas , " SupportsFileBasedCompression: ", device.SupportsFileBasedCompression )
        print ("SystemCreationClassName: ", device.SystemCreationClassName , " SystemName: ", device.SystemName )
        print ("VolumeDirty: ", device.VolumeDirty , " VolumeName: ", device.VolumeName )
        print ("VolumeSerialNumber: ", device.VolumeSerialNumber )
        print ("")


def list_media_devices(devlist:list=None) ->list:
    """ list all removable drives

    returns list of drive-objects
    """

    devices = []
    if not devlist:
        pythoncom.CoInitialize()
        c = wmi.WMI ()
        devlist = c.Win32_LogicalDisk () 
    for drive in devlist:
        # print (drive.Caption, DRIVE_TYPES[drive.DriveType])
        if drive.DriveType == 2:
            devices.append (drive.DeviceID)

    return devices


def get_device_name(device:str) ->str:
    """ compatibility with posix """
    return device

def get_media_path(device):
    return os.path.join (device, os.sep)

def mount(device, name=None):
    pass

def unmount(device, name=None):
    pass

def is_mounted(device):
    """ compatibility with posix:

    in win always True
    """
    return os.path.ismount (device)


def is_removable(device:str, devlist:list=None):

    if not devlist:
        c = wmi.WMI ()
        devlist = c.Win32_LogicalDisk () 
    for drive in devlist:
        if drive.DeviceID == device and drive.DriveType == 2:
            return True
    return False


def get_size(device:str, devlist:list=None):

    if not devlist:
        c = wmi.WMI ()
        devlist = c.Win32_LogicalDisk () 
    for drive in devlist:
        if drive.DeviceID == device:
            try:
                size = int (drive.Size)
            except:
                size = -1
            return size


def get_model(device:str, devlist:list=None):
    if not devlist:
        c = wmi.WMI ()
        devlist = c.Win32_LogicalDisk () 
    for drive in devlist:
        if drive.Caption == device:
            return drive.VolumeName
    return "unnnown"


def get_vendor(device:str, devlist:list=None):
    """ in NT not available
    compatibility with Posix
    """
    return "unnown"


def get_label(device:str, devlist:list=None) ->str:
    """ user friendly String to identify a device
    """
    if not devlist:
        c = wmi.WMI ()
        devlist = c.Win32_LogicalDisk () 
    for drive in devlist:
        if drive.Caption == device:
            if drive.VolumeName:
                name = drive.VolumeName
            else:
                name = "unknown drive"
            if drive.Size:
                size = "%.2f" % (int (drive.Size) /1024 ** 3) + " GB"
            else:
                size = "unnown size"
            
            if drive.FreeSpace:
                free = "%.2f" % ( int (drive.FreeSpace) /1024 ** 3) + " GB frei"
            else:
                free = "0 GB free"
            return name  + ", " + size + " , " + free
    return "unnown"



if __name__ == "__main__":
    # all drives:
    devicelist = list_drive_devices ()  
    # alle removable drives:
    medialist = list_media_devices (devicelist)    
    print ("Media list:", medialist)      
    
    for device in devicelist:
        name = device.Caption
        label = get_label (name, devicelist)
        print ("Label of {} {}".format (name, label))

