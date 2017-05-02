FROM wazopbx/wazo-admin-ui

RUN for plugin in cdr \
                  conference \
                  context \
                  device \
                  extension \
                  group \
                  incall \
                  ivr \
                  moh \
                  outcall \
                  paging \
                  parking-lot \
                  plugin \
                  switchboard \
                  trunk \
                  user \
                  voicemail; do \
    cd /usr/src; \
    git clone --depth 1 https://github.com/wazo-pbx/wazo-admin-ui-$plugin.git;  \
    cd /usr/src/wazo-admin-ui-$plugin; \
    python setup.py develop; \
    done

COPY . /usr/src/wazo-admin-ui
WORKDIR /usr/src/wazo-admin-ui

RUN pybabel compile --directory=wazo_admin_ui/translations
RUN python setup.py develop
