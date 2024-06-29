
build:
	docker compose build
run:
	docker compose up -d
stop:
	docker compose stop
up-service:
	# in that command should up all required services.
	docker compose run -d -p "27017:27017"  mongo   # 27017 is default mongo port