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
	@ echo " run         Execute the logger on the foreground. Hit Ctrl+C to stop it."

install-debian-deps:
	sudo apt-get install -y python3 supervisor curl dialog

install-pip3:
	wget https://bootstrap.pypa.io/get-pip.py
	sudo python3 get-pip.py
	rm get-pip.py

install-python-deps: install-pip3
	sudo pip3 install -U virtualenv

install-platformio:
	sudo python -c "$$(curl -fsSL https://raw.githubusercontent.com/platformio/platformio/master/scripts/get-platformio.py)"

setup: install-debian-deps install-python-deps install-platformio venv
	
venv: clean-venv
	@ echo "-------------------------------------------------------"
	virtualenv -v --python='${PYBIN}' ${VENVDIR} --no-site-packages
	${VENVDIR}/bin/pip install -r logger/requirements.pip
	@ echo "-------------------------------------------------------"
	@ echo "Required Python virtual environment sucessfully installed at "
	@ du -sh ${VENVDIR}

clean-venv:
	rm -rf ${VENVDIR}

check-venv:
	@ command -v ${VENVPY} >/dev/null 2>&1 || \
		{ printf "You need to prepare the required Python virtual environment";\
		  printf "\nfor running this software. Excecute, just once:";\
		  printf "\n\n    $$ make setup\n\nor\n\n    ";\
	   	  printf "$$ make setup PYBIN=<python_binary>\n\nfor specifying a ";\
		  printf "Python binary other than 'python3', like\n'python-3.x' ";\
		  printf "(where x is a number) for instance. \n\n"; exit 1; }

firmware:
	python3 scripts/run_platformio.py

serial: check-venv
	${VENVPY} scripts/init_serial.py --loop

pyserial: check-venv
	${VENVPY} -i scripts/init_serial.py

syncrtc:
	${VENVPY} scripts/init_serial.py --syncrtc

boardhash:
	${VENVPY} scripts/getboardhash.py
 
run: check-venv
	${VENVPY} logger/run.py

