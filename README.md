
# mount.py

[mount.py][mount.py] is a simple, small and self-contained [Python][Python] **only** library,
for listing, mounting and unmounting media drives on Linux.

*[mount.py][mount.py] is developed and tested using Python 3.5.1.
It was initially developed for and tested on a
[Raspberry Pi Model B+](https://www.raspberrypi.org/products/model-b-plus/)
running [Raspbian GNU/Linux](http://raspbian.org/).*


## How does it work?

Internally [mount.py][mount.py] relies on `os.system()` calls.

When listing media drives [mount.py][mount.py] queries and parses `/proc/partitions`.
When getting partitions `fdisk` is queried. Last for not least `mkdir` and `mount` is used
for mounting, follow by `umount` used for unmounting.


### License

This module is shared under the MIT license, and is therefore free to use, shared, distribute and modify.
See [LICENSE](https://github.com/MrVallentin/mount.py/blob/master/LICENSE) for more details.


[mount.py]: https://github.com/MrVallentin/mount.py

[Python]: https://www.python.org
