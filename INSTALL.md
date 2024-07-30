Before You Start
================

Binwalk supports Python 3.8+. 

It is recommended to install Binwalk through the package repository of your Linux distribution, whenever possible. 

Installation
============

Installation follows the typical Python installation procedure:

```bash
# Python3.x
$ python3 setup.py install --user
```

**NOTE**: Older versions of binwalk (e.g., v1.0) are not compatible with the latest version of binwalk. It is strongly recommended that you uninstall any existing binwalk installations before installing the latest version in order to avoid API conflicts.

Dependencies
============

Besides a Python interpreter, there are no installation dependencies for binwalk. All dependencies are optional run-time dependencies, and unless otherwise specified, are available from most Linux package managers.

Binwalk uses pytest for tests and `pytest-cov` for test coverage:

```bash
$ sudo apt install python3-pytest python3-pytest-cov
```

Binwalk uses [matplotlib](https://matplotlib.org/) to generate graphs and visualizations: 

```bash
$ sudo apt install python3-matplotlib
```

Binwalk's `--disasm` option requires the [Capstone](http://www.capstone-engine.org/) disassembly framework and its corresponding Python bindings:

```bash
$ sudo apt install python3-capstone
```

Binwalk relies on multiple external utilties in order to automatically extract/decompress files and data:

```bash
# Install standard extraction utilities
$ sudo apt install mtd-utils gzip bzip2 tar arj lhasa p7zip p7zip-full cabextract cramfsswap squashfs-tools sleuthkit default-jdk lzop srecord
```

```bash
# Install sasquatch to extract non-standard SquashFS images
$ sudo apt install zlib1g-dev liblzma-dev liblzo2-dev
$ git clone https://github.com/devttys0/sasquatch
$ cd sasquatch
$ wget https://github.com/devttys0/sasquatch/pull/47.patch && patch -p1 < 47.patch
$ ./build.sh
```

```bash
# Install cramfs tools
$ git clone --quiet --depth 1 --branch "master" https://github.com/npitre/cramfs-tools
$ (cd cramfs-tools && make && sudo install cramfsck /usr/local/bin)
```

```bash
# Install jefferson to extract JFFS2 file systems
$ pipx install jefferson
```

```bash
# Install ubi_reader to extract UBIFS file systems
$ pipx install ubi_reader
```

```bash
# Install yaffshiv to extract YAFFS file systems
$ git clone https://github.com/devttys0/yaffshiv
$ (cd yaffshiv && pipx install .)
```

Note that for Debian/Ubuntu users, all of the above dependencies can be installed automatically using the included `deps.sh` script:

```bash
$ sudo ./deps.sh
```

Installing the IDA Plugin
=========================

If IDA is installed on your system, you may optionally install the binwalk IDA plugin:

```bash
$ python setup.py idainstall --idadir=/home/user/ida
```

Likewise, the binwalk IDA plugin can be uninstalled:

```bash
$ python setup.py idauninstall --idadir=/home/user/ida
```


Uninstalling Binwalk
====================

If binwalk has been installed to a standard system location (e.g., via `setup.py install`), it can be removed by running:

```bash
# Python3
$ sudo python3 setup.py uninstall
```

Note that this does _not_ remove any of the manually installed dependencies.

