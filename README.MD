# GymBot Bott Appication


## App structures
main.py - Start enpoint of app
server.py - Telegram Bot server.
config.py - Store configs
services/ - Packages with business login off application

## virtual enviroment 
activate enviroment

```shell
poetry shell
```

in cases
```
The currently activated Python version 3.*.* is not supported by the project (3.12).
Trying to find and use a compatible version. 
```
should set python path with correct version
```shell
poetry env use /usr/bin/python3.12
```

poetry add new deps
for example:
```shell
poetry add setuptools==1.2.3
```
add to `dev` deps
```shell
poetry add setuptools==1.2.3 --group=dev
```

## Run bot localy
Add local.env file with TOKEN env
Run main.py file
```shell
python3 -m app.main
```

## run bot in docker 

run in docker compose 
```shell
make run
```

Build docker compose image
```shell
make build
```

Up mongo-db only.
That requires for local up TG-bot,
cause TH-bot required some services
for mongo must add env `MONGO_HOST=localhost` to local.dev

```shell
make up-service
```
