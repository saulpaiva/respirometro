PYBIN := python3
VENVDIR := $(shell pwd)/.venv
VENVPY := ${VENVDIR}/bin/python

BUILDDIR := .build

.PHONY: help setup firmware serial run 

all: help

help:
	@ echo "USAGE: make <target>    where <target> can be:"
	@ echo ""
	@ echo " setup       Execute once to prepare the required Python virtual environment" 
	@ echo " firmware    Compile and upload the firmware to the Arduino board via serial"
	@ echo " serial      Starts a serial session with Python for board communication"
	@ echo ""
	@ echo " store       Execute the logger on the foreground. Hit Ctrl+C to stop it."
	@ echo " analyse     Execute the analyses data routine"

install-debian-deps:
	sudo apt-get install -y python3 supervisor curl dialog

install-pip3:
	wget https://bootstrap.pypa.io/get-pip.py
	sudo python3 get-pip.py
	rm get-pip.py

install-python-deps: install-pip3
	sudo pip3 install -r scripts/requirements.pip

install-platformio:
	sudo python -c "$$(curl -fsSL https://raw.githubusercontent.com/platformio/platformio/master/scripts/get-platformio.py)"

setup: install-debian-deps install-python-deps install-platformio venv
	

firmware:
	python3 scripts/run_platformio.py

serial:
	python3 scripts/init_serial.py --loop

pyserial:
	python3 -i scripts/init_serial.py
 
run:
	python3 logger/run.py

