
# mount.py

[mount.py][mount.py] is a simple, small and self-contained [Python][Python] **only** library,
for listing, mounting and unmounting media drives on Linux.

*[mount.py][mount.py] is developed and tested using Python 3.5.1.
It was initially developed for and tested on a
[Raspberry Pi Model B+](https://www.raspberrypi.org/products/model-b-plus/)
running [Raspbian GNU/Linux](http://raspbian.org/).*

**Advice:** It isn't optimal, but I would highly advice to mount and unmount drives when
working with them, or at least just frequently unmount drives if they haven't been used
for some time. As forgetting to unmount a drive, before pulling it out can result in
a *broken* drive.


## Examples

- [List USB Drives](#example-list-usb-drives)
- [List Files on USB Drives](#example-list-files-on-usb-drives)
- [Write to USB](#example-write-to-usb)
- [Read from USB](#example-read-from-usb)
- [Detect USB Connections](#example-detect-usb-connections)


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

Targeting the same USB
and having executed the [Write to USB example](#example-write-to-usb) prior
to executing this example. Then the above prints:

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
