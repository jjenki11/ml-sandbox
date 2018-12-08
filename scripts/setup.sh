#!/bin/bash

echo "Now installing..."

sudo apt-get -y install update-manager-core python3 python3-pip
sudo easy_install3 pip
sudo pip3 install --upgrade pip3

if sudo pip3 list | grep rpy2
then 
    echo "OK";
else
    echo "NOT FOUND"
    sudo apt purge r-base* r-recommended r-cran-*
    sudo apt autoremove
    sudo apt update
    sudo do-release-upgrade
    sudo add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/'
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
    sudo apt update
    sudo apt install r-base r-base-core r-recommended
fi

# TBD 
#sudo pip3 install -r $PWD/requirements.txt

sudo pip3 install pandas scikitlearn matplotlib rpy2\

echo "Done. Have fun!"