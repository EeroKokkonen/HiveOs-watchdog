# HiveOS-watchdog
Watchdog made for HiveOS to keep track of electricity price and shutting down mining rig for the time that eletricity price is higher than user's set price.

Note than watchdog only works in HiveOS. Price of electricity comes from NordPool and it includes Finnish electricity tax rate which is 24%.

Watchdog is still being tested so be aware that there might be some bugs.

# Getting started

## Downloading needed files
Open Hive shell
![image](https://github.com/EeroKokkonen/HiveOs-watchdog/assets/101599252/530c892c-ac09-4bcc-88a4-14f911b89a00)

Go to user folder:
`cd /home/user`

Clone this github repository:
`git clone https://github.com/EeroKokkonen/HiveOs-watchdog.git`

Go to repository:
`cd HiveOs-watchdog`

Type `ls` and you should see some files there.

## Updating python3
By default HiveOS has python3.6 version which is too old so we need to update that.
You can make sure of your python version by typing:
`python3 --version`

Update linux packages:
`sudo apt update`

Check if python3.8 is available:
`apt list | grep python3.8`

You should see something like this
![image](https://github.com/EeroKokkonen/HiveOs-watchdog/assets/101599252/33eacbc9-80f0-4fdb-9d84-007af1dc99c5)

Install python3.8:
`sudo apt install python3.8`

Update alternatives (Not sure if this is necessary but atleast I have done this)
```
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
```

Check python3 version again:
`python3 --version`

If it says 3.8 all is fine, otherwise change alternative python3:
`sudo update-alternatives --config python3`
And select python3.8.

To fix some bugs you need to remove and reinstall python3:
```
sudo apt remove --purge python3-apt
sudo apt autoclean
sudo apt install python3-apt
```
Also you need to install some additional stuff:
```
sudo apt install python3.8-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3.8 get-pip.py
sudo apt install python3.8-venv
```

Now all should be ready for configurating and installing watchdog.

## Configure HiveOS-watchdog <ins>before</ins> installation
If you are not already inside HiveOs-watchdog folder type:
```cd /home/user/HiveOs-watchdog```

To modify confugrations type:
```nano electric-watchdog.env```
![image](https://github.com/EeroKokkonen/HiveOs-watchdog/assets/101599252/f643d84d-7796-4ffb-b0a8-590fcaf03d73)

### PRICE
The price determines at what point the watchdog shuts down the rig. <br />
Example: <br />
`PRICE=8.7`  Means rig will be off when electricity price is over 8.7cents/kWh <br />
`PRICE=10`   Means rig will be off when electricity price is over 10cents/kWh <br />

### LOGGING
Logging is just for debugging Watcdog, so most likely you don't want it to be on. <br />
Example: <br />
`LOGGING=0`  Means logging is off <br />
`LOGGING=1`  Means logging is on <br />

### TIMEZONE
This only affects to logging so if you dont use logging you don't need to touch this. <br />
Example: <br />
`TIMEZONE=3`  Means you are in UTC+3 Time Zone<br />

### Saving the file
After you have made all the wanted changes, press following keys:  
`ctrl + o`  
`enter`  
`ctrl + x`  


## Installing HiveOs-watchdog
If you are not already inside HiveOs-watchdog folder type:
`cd /home/user/HiveOs-watchdog`

Type:
`make install`

## Starting HiveOs-watchdog
To start watchdog:
`systemctl start electric-watchdog`

To check if watchdog is running:
`systemctl status electric-watchdog`

To make watchdog start when rig boots:
`systemctl enable electric-watchdog`

Now everything should be fine and watchdog should keep watch over your rig.

## Modifying configs <ins>after</ins> installation
If you want to change the price cap you can to do it by typing: <br />
`nano /usr/local/etc/electric-watchdog/electric-watchdog.env` <br />
And changing the price. After rebooting the rig, watchdog will follow the new price cap.  
  
<ins>More detailed information can be found above.</ins>

## Other usefull commands

If you just want to turn watchdog off type: <br />
`systemctl stop electric-watchdog`

If you don't want watchdog to automatically go on when booting type: <br />
`systemctl disable electric-watchdog`

If you want to get rid of watchdog go to the HiveOs-watchdog folder and type: <br />
`make uninstall`







