#!/bin/bash

# Check for the --yes command line argument to skip yes/no prompts
if [ "$1" = "--yes" ]
then
    YES=1
else
    YES=0
fi

set -eu
set -o nounset
set -x

if ! which lsb_release > /dev/null
then
    lsb_release() {
        if [ -f /etc/os-release ]
        then
            [[ "$1" = "-i" ]] && cat /etc/os-release | grep ^"ID" | cut -d= -f 2
            [[ "$1" = "-r" ]] && cat /etc/os-release | grep "VERSION_ID" | cut -d= -d'"' -f 2
        elif [ -f /etc/lsb-release ]
        then
            [[ "$1" = "-i" ]] && cat /etc/lsb-release | grep "DISTRIB_ID" | cut -d= -f 2
            [[ "$1" = "-r" ]] && cat /etc/lsb-release | grep "DISTRIB_RELEASE" | cut -d= -f 2
        else
            echo Unknown
        fi
    }
fi

if [ $YES -eq 0 ]
then
    distro="${1:-$(lsb_release -i|cut -f 2)}"
    distro_version="${1:-$(lsb_release -r|cut -f 2|cut -c1-2)}"
else
    distro="${2:-$(lsb_release -i|cut -f 2)}"
    distro_version="${2:-$(lsb_release -r|cut -f 2|cut -c1-2)}"
fi
APTCMD="apt"
APTGETCMD="apt-get"
APT_CANDIDATES="arj build-essential bzip2 cabextract cpio cramfsswap git gzip lhasa liblzma-dev liblzo2-dev locales lzop mtd-utils p7zip p7zip-full python3-distutils python3-setuptools python3-matplotlib python3-capstone python3-pycryptodome python3-gnupg pipx squashfs-tools sleuthkit srecord tar wget zlib1g-dev"

# Check for root privileges
if [ $UID -eq 0 ]
then
    echo "UID is 0, sudo not required"
    SUDO=""
else
    SUDO="sudo -E"
fi

install_yaffshiv()
{
    git clone --quiet --depth 1 --branch "master" https://github.com/devttys0/yaffshiv /home/$USR
    (cd yaffshiv && python setup.py install .)
    rm -rf yaffshiv
}

install_sasquatch()
{
    git clone --quiet --depth 1 --branch "master" https://github.com/devttys0/sasquatch
    (cd sasquatch &&
        wget https://github.com/devttys0/sasquatch/pull/47.patch &&
        patch -p1 < 47.patch &&
        ./build.sh)
    rm -rf sasquatch
}

install_cramfstools()
{
  # Downloads cramfs tools from sourceforge and installs them to $INSTALL_LOCATION
  TIME=`date +%s`
  INSTALL_LOCATION=/usr/local/bin

  # https://github.com/torvalds/linux/blob/master/fs/cramfs/README#L106
  git clone --quiet --depth 1 --branch "master" https://github.com/npitre/cramfs-tools
  # There is no "make install"
  (cd cramfs-tools \
  && make \
  && $SUDO install cramfsck $INSTALL_LOCATION)

  rm -rf cramfs-tools
}

install_cramfstools()
{
(curl -sSL https://install.python-poetry.org | python3 -)
}

install_pip_package()
{
    PACKAGE="$1"
    pip3 install $PACKAGE
}

find_path()
{
    FILE_NAME="$1"

    echo -ne "checking for $FILE_NAME..."
    which $FILE_NAME > /dev/null
    if [ $? -eq 0 ]
    then
        echo "yes"
        return 0
    else
        echo "no"
        return 1
    fi
}

# Make sure the user really wants to do this
if [ $YES -eq 0 ]
then
    echo ""
    echo "WARNING: This script will download and install all required and optional dependencies for binwalk."
    echo "         This script has only been tested on, and is only intended for, Debian based systems."
    echo "         Some dependencies are downloaded via unsecure (HTTP) protocols."
    echo "         This script requires internet access."
    echo "         This script requires root privileges."
    echo ""
    if [ "$distro" != Unknown ]
    then
        echo "         $distro $distro_version detected"
    else
        echo "WARNING: Distro not detected, using package-manager defaults"
    fi
    echo ""
    echo -n "Continue [y/N]? "
    read YN
    if [ "$(echo "$YN" | grep -i -e 'y' -e 'yes')" == "" ]
    then
        echo "Quitting..."
        exit 1
    fi
elif [ "$distro" != Unknown ]
then
     echo "$distro $distro_version detected"
else
    echo "WARNING: Distro not detected, using package-manager defaults"
fi

# Check for supported package managers and set the PKG_* envars appropriately
find_path $APTCMD
if [ $? -eq 1 ]
then
    find_path $APTGETCMD
    if [ $? -ne 1 ]
    then
        PKGCMD="$APTGETCMD"
        PKGCMD_OPTS="install -y"
        PKG_CANDIDATES="$APT_CANDIDATES"
    fi
else
    if "$APTCMD" install -s -y dpkg > /dev/null
    then
        PKGCMD="$APTCMD"
        PKGCMD_OPTS="install -y"
        PKG_CANDIDATES="$APT_CANDIDATES"
    else
        PKGCMD="$APTGETCMD"
        PKGCMD_OPTS="install -y"
        PKG_CANDIDATES="$APT_CANDIDATES"
    fi
fi

# Install system packages
$SUDO $PKGCMD $PKGCMD_OPTS $PKG_CANDIDATES

# Do the install(s)
cd /tmp
if [ $? -ne 0 ]
    then
    echo "Package installation failed: $PKG_CANDIDATES"
    exit 0
fi

install_pip_package ubi_reader
install_pip_package jefferson
install_sasquatch
install_yaffshiv
install_cramfstools

