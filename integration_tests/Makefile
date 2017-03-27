.PHONY: test-setup test

CONFD_DIR ?= ../../confd/
MANAGE_DB_DIR ?= ../../manage-db/
POSTGRES_DOCKER=$(MANAGE_DB_DIR)/contribs/postgres-test/Dockerfile

test-setup: docker-pull build-admin-ui egg-info

docker-pull:
	docker pull n3llyb0y/wait
	docker pull p0bailey/docker-flask
	docker pull rabbitmq
	docker pull wazopbx/postgres
	docker pull wazopbx/postgres-test
	docker pull wazopbx/xivo-confd
	docker pull wazopbx/xivo-provd

build-admin-ui:
	docker build -t wazopbx/wazo-admin-ui ..
	docker build --no-cache -t wazo-admin-ui-test -f Dockerfile ..

update-confd:
	docker build --no-cache -t wazopbx/xivo-confd ${CONFD_DIR}

update-db:
	docker build --no-cache -t wazopbx/postgres-test -f $(POSTGRES_DOCKER) $(MANAGE_DB_DIR)

egg-info:
	cd .. && python setup.py egg_info

test:
	nosetests
