.PHONY: test-setup test

test-setup: docker-pull build-admin-ui egg-info

docker-pull:
	docker pull n3llyb0y/wait
	docker pull p0bailey/docker-flask

build-admin-ui:
	docker build -t wazopbx/wazo-admin-ui ..
	docker build --no-cache -t wazo-admin-ui-test -f Dockerfile ..

egg-info:
	cd .. && python setup.py egg_info

test:
	nosetests
