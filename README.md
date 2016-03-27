
# mount.py

[mount.py][mount.py] is a simple, small and self-contained [Python][Python] **only** module,
for listing, mounting and unmounting media drives on Linux.

*[mount.py][mount.py] is developed and tested using Python 3.5.1.
It was initially developed for and tested on a
[Raspberry Pi Model B+](https://www.raspberrypi.org/products/model-b-plus/)
running [Raspbian GNU/Linux](http://raspbian.org/).*

**Advice:** It isn't optimal, but I would highly advice to mount and unmount drives when
working with them, or at least just frequently unmount drives if they haven't been used
for some time. As forgetting to unmount a drive, before pulling it out can result in
a *broken* drive.


## Install

Installation is easily done through the terminal.

#### Using git

```
$ git clone https://github.com/MrVallentin/mount.py
$ sudo python mount.py/setup.py install
$ rm -rf mount.py
```

#### Using curl & unzip

```
$ curl -o mount.py.zip -L https://github.com/MrVallentin/mount.py/archive/master.zip
$ unzip mount.py.zip
$ sudo python mount.py-master/setup.py install
$ rm -rf mount.py-master
$ rm -rf mount.py.zip
```

#### Using wget & unzip

```
$ wget https://github.com/MrVallentin/mount.py/archive/master.zip -O mount.py.zip
$ unzip mount.py.zip
$ sudo python mount.py-master/setup.py install
$ rm -rf mount.py-master
$ rm -rf mount.py.zip
```

##### Uninstall

*Download the module using any of the above, and then do the following:*

```
$ sudo python mount.py/setup.py install --record files.txt
$ cat mount.py/files.txt | sudo xargs rm -rf
```


### Testing

After installation checking whether [mount.py][mount.py] is working,
can simply be done by doing:

```
$ sudo python -m mount
```


## How does it work?

Internally [mount.py][mount.py] relies on `os.system()` calls, which in
turn some require [superuser][superuser] access.

When listing media drives [mount.py][mount.py] queries and parses `/proc/partitions`.
When getting partitions `fdisk` is queried. Last for not least `mkdir` and `mount` is used
for mounting, follow by `umount` used for unmounting.


## Examples

- [List USB Drives](#example-list-usb-drives)
- [List Files on USB Drives](#example-list-files-on-usb-drives)
- [Write to USB](#example-write-to-usb)
- [Read from USB](#example-read-from-usb)
- [Detect USB Connections](#example-detect-usb-connections)


## API Reference

_The following references and examples are based on [mount.py][mount.py]
being imported using `from mount import *`._

```python
list_media_devices()
```
> Returns a list containing all the device paths,
> for media devices/[block][block] [devices][device-file] (suchs as USB flash drives).
>
> Example:
>
> *Tested with 2 USBs connected.*
>
> ```python
>>>> list_media_devices()
['/dev/sda', '/dev/sdb']
```

```python
get_device_name(device)
```
> Returns the device name from the device path.
>
> ```python
>>>> get_device_name("/dev/sda")
'sda'
```

```python
get_device_block_path(device)
```
> Returns the system block device path.
>
> ```python
>>>> get_device_block_path("/dev/sda")
'/sys/block/sda'
>>>> get_device_block_path("sda")
'/sys/block/sda'
```

```python
get_media_path(device)
```
> Returns the media path, where files on the device
> can be found after mounting.
>
> ```python
>>>> get_media_path("/dev/sda")
/media/sda
>>>> get_media_path("sda")
/media/sda
```

```python
get_partition(device)
```
> Returns the partition path.
>
> Requires [superuser][superuser].
>
> ```python
>>>> get_partition("/dev/sda")
/dev/sda1
```

```python
is_mounted(device)
```
> Returns `True` or `False` whether a device is mounted or not.

```python
mount(device, name=None)
```
> Mounts a specific device to a directory named `name` in `/media`.
> If the directory in `/media` doesn't exist, then it is created.
>
> If `name is None` then name is equivalent to `name = get_device_name(device)`.
>
> `mount()` can safely be called no matter whether a device is already mounted or not. 
>
> Requires [superuser][superuser].
>
> ```python
>>>> mount("/dev/sda")
```

```python
unmount(device, name=None)
```
> Unmounts a specific device from the directory named `name` in `/media`.
>
> If `name is None` then name is equivalent to `name = get_device_name(device)`.
>
> `unmount()` can safely be called no matter whether a device is already mounted or not. 
>
> Requires [superuser][superuser].
>
> ```python
>>>> unmount("/dev/sda")
```

```python
is_removable(device)
```
> Returns `True` or `False` whether a device is removable or not.

```python
get_size(device)
```
> Returns the total storage space in bytes.
>
> Example:
>
> *Tested with a 16 GB USB connected.*
>
> ```python
>>>> "%.2f" % (get_size("/dev/sda") / 1024 ** 3)
'14.84'
```

```python
get_model(device)
```
> Returns the model name.

```python
get_vendor(device)
```
> Returns the vendor name.


## Examples


### Example: List USB Drives

*The following example, is the equivalent of doing `python mount.py` in the terminal.*

vs `sudo python mount.py`


```python
import os
from mount import *

devices = list_media_devices()

for device in devices:
	name = get_device_name(device)
	path = get_media_path(device)
	
	print("Drive:", get_device_name(device))
	
	mount(device)
	
	print("Mounted:", "Yes" if is_mounted(device) else "No")
	print("Removable:", "Yes" if is_removable(device) else "No")
	print("Size:", get_size(device), "bytes")
	print("Size:", "%.2f" % (get_size(device) / 1024 ** 3), "GB")
	print("Model:", get_model(device))
	print("Vendor:", get_vendor(device))
	print()
```

Tested using a 16 GB USB, the above prints:

```
Drive: sda
Mounted: Yes
Removable: Yes
Size: 15931539456 bytes
Size: 14.84 GB
Model: SD/MMC
Vendor: Generic-
```


### Example: List Files on USB Drives

```python
import os
from mount import *

def list_files(root, indent=1):
	for filename in os.listdir(root):
		path = os.path.join(root, filename)
		
		if os.path.isfile(path):
			print("-" * indent, filename)
		elif os.path.isdir(path):
			print("+" * indent, filename)
			list_files(path, indent + 1)

devices = list_media_devices()

for device in devices:
	print("Drive:", get_device_name(device))
	
	mount(device)
	
	if is_mounted(device):
		print("Files:")
		list_files(get_media_path(device))
	
	unmount(device)
	
	print()

```

Using a USB with a few test files on, the above prints:

```
Drive: sda
Files:
- file.txt
+ folder
-- file in folder.txt
++ subfolder
--- file in subfolder.txt
```


### Example: Write to USB

```python
import os
from mount import *

devices = list_media_devices()

device = None
for check_device in devices:
	# Compare model, vendor, size, etc
	# to find the target drive.
	
	# In this example, we're just
	# gonna just the first.
	device = check_device
	break

if device:
	path = get_media_path(device)
	
	mount(device)
	
	if is_mounted(device):
		with open(path + "/hello-world.txt", "w") as f:
			f.write("Hello World")
	
	unmount(device)
```


### Example: Read from USB

```python
import os
from mount import *

devices = list_media_devices()

device = None
for check_device in devices:
	# Compare model, vendor, size, etc
	# to find the target drive.
	
	# In this example, we're just
	# gonna just the first.
	device = check_device
	break

if device:
	path = get_media_path(device)
	
	mount(device)
	
	if is_mounted(device):
		with open(path + "/hello-world.txt", "r") as f:
			print(f.read())
	
	unmount(device)
```

Targeting the same USB, and having executed the
[Write to USB example](#example-write-to-usb)
prior to executing this example.
Then the above prints:

```
Hello World
```


### Example: Detect USB Connections

*TO DO*


## Reporting Bugs & Requests

Feel free to use the [issue tracker](https://github.com/MrVallentin/mount.py/issues),
for reporting bugs, submitting patches or requesting features.

Before submitting bugs, make sure that you're using the latest version of [mount.py][mount.py].


## License

This module is shared under the MIT license, and is therefore free to use, shared, distribute and modify.
See [LICENSE](https://github.com/MrVallentin/mount.py/blob/master/LICENSE) for more details.


[mount.py]: https://github.com/MrVallentin/mount.py

[Python]: https://www.python.org

[block]: https://en.wikipedia.org/wiki/Block_(data_storage)
[device-file]: https://en.wikipedia.org/wiki/Device_file

[superuser]: https://en.wikipedia.org/wiki/Superuser
