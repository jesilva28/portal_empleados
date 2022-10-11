run-app:
	docker-compose up

build-image:
	docker build -t portal_empleados . && \
	docker image prune --force