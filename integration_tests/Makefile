.PHONY: test-setup test docker-pull build-admin-ui egg-info

test-setup: docker-pull build-admin-ui egg-info

docker-pull:
	docker pull n3llyb0y/wait
	docker pull wazopbx/xivo-auth-mock

build-admin-ui:
	docker build -t wazopbx/wazo-admin-ui ..
	docker build --no-cache -t wazo-admin-ui-test -f Dockerfile ..

egg-info:
	cd .. && python setup.py egg_info

test:
	nosetests
