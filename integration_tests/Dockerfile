FROM wazopbx/wazo-admin-ui

RUN for plugin in conference \
                  group \
                  incall \
                  moh \
                  outcall \
                  paging \
                  parking-lot \
                  switchboard \
                  user \
                  voicemail; do \
    cd /var/tmp; \
    git clone --depth 1 https://github.com/wazo-pbx/wazo-admin-ui-$plugin.git;  \
    cd /var/tmp/wazo-admin-ui-$plugin; \
    python setup.py install; \
    done

COPY . /usr/src/wazo-admin-ui
WORKDIR /usr/src/wazo-admin-ui

RUN pybabel compile --directory=wazo_admin_ui/translations
RUN python setup.py develop
