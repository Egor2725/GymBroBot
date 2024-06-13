# GymBot Bott Appication


## App structures
main.py - Start enpoint of app
server.py - Telegram Bot server.
config.py - Store configs
services/ - Packages with business login off application

## virtual enviroment 

activate enviroment

```sh
poetry shell
```

in cases
```
The currently activated Python version 3.*.* is not supported by the project (3.12).
Trying to find and use a compatible version. 
```
should set python path with correct version
```sh
poetry env use /usr/bin/python3.12
```

poetry add new deps
for example:
```sh
poetry add setuptools==1.2.3
```
add to `dev` deps
```sh
poetry add setuptools==1.2.3 --group=dev
```




