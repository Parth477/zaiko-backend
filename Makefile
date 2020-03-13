stop_services:
	@echo "Stopping postgresql and rabbitmq-server..."
	service postgresql stop && service rabbitmq-server stop

local_up:
	docker-compose -f docker-compose.yml up

web_shell:
	docker exec -it zaiko_django_container /bin/bash