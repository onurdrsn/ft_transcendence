#This makefile about ft_transendence project.
CONTAINERS	= $(shell docker ps -qa)
IMAGES		= $(shell docker images -qa)
VOLUMES		= $(shell docker volume ls -q)
NETWORKS	= $(shell docker network ls -q)

COMPOSE		= docker compose -f
MKDIR       = mkdir -p
all: up

volumes:
	@ $(MKDIR) ./srcs/.temp/data/postgres

up		: volumes
		@ $(COMPOSE) srcs/docker-compose.yml up --build

down	:
		@ $(COMPOSE) srcs/docker-compose.yml down

clean	: down
		@ docker rm -f $(CONTAINERS); true;
		@ docker rmi -f $(IMAGES); true;
		@ docker volume rm $(VOLUMES); true;
		@ docker network rm $(NETWORKS) 2> /dev/null; true;

cache	: clean
		@ docker system prune -af --volumes

re		: cache all

.PHONY	: up down containers images volumes networks rm_volume clean cache
