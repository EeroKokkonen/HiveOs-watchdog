all: electric-watchdog electric-watchdog.service
.PHONY: all electric-watchdog install uninstall
lib_dir=/usr/local/lib/electric-watchdog
conf_dir=/usr/local/etc/electric-watchdog
service_dir=/etc/systemd/system
venv=$(lib_dir)/venv

install: $(service_dir) electric-watchdog.service
	@echo Installing the service file...
	cp electric-watchdog.service $(service_dir)
	chown root:root $(service_dir)/electric-watchdog.service
	chmod 644 $(service_dir)/electric-watchdog.service

	@echo Installing library files...
	mkdir -p $(lib_dir)
	cp electric-watchdog.py $(lib_dir)
	chown root:root $(lib_dir)/*
	chmod 644 $(lib_dir)/*

	@echo Installing configuration files...
	mkdir -p $(conf_dir)
	cp electric-watchdog.env $(conf_dir)
	chown root:root $(conf_dir)/*
	chmod 644 $(conf_dir)/*

	@echo Creating python virtual environment and isntalling packages...
	python3 -m venv $(venv)
	$(venv)/bin/pip3 install -r requirements.txt

	@echo Installation complete...
	@echo run 'systemctl start mypythonservice' to start service
	@echo run 'systemctl status mypythonservice' to view status

uninstall:
	-systemctl stop electric-watchdog
	-systemctl disable electric-watchdog
	-rm -r $(lib_dir)
	-rm -r $(conf_dir)
	-rm -r $(service_dir)/electric-watchdog.service
