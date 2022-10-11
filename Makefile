run-app:
	docker-compose up

build-image:
	docker build -t amanotas20/portal_empleados:1.0 . && \
	docker image prune --force