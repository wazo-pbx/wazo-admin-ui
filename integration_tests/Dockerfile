FROM wazopbx/wazo-admin-ui

COPY . /usr/src/wazo-admin-ui
WORKDIR /usr/src/wazo-admin-ui

ENV PYTHONDONTWRITEBYTECODE='true'

RUN pybabel compile --directory=wazo_admin_ui/translations
RUN python3 setup.py develop
