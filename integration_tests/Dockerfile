FROM wazopbx/wazo-admin-ui

WORKDIR /var/tmp
RUN git clone https://github.com/wazo-pbx/wazo-admin-ui-user.git
WORKDIR /var/tmp/wazo-admin-ui-user
RUN python setup.py install

WORKDIR /var/tmp
RUN git clone https://github.com/wazo-pbx/wazo-admin-ui-conference.git
WORKDIR /var/tmp/wazo-admin-ui-conference
RUN python setup.py install

WORKDIR /var/tmp
RUN git clone https://github.com/wazo-pbx/wazo-admin-ui-group.git
WORKDIR /var/tmp/wazo-admin-ui-group
RUN python setup.py install

WORKDIR /var/tmp
RUN git clone https://github.com/wazo-pbx/wazo-admin-ui-parking-lot.git
WORKDIR /var/tmp/wazo-admin-ui-parking-lot
RUN python setup.py install

WORKDIR /var/tmp
RUN git clone https://github.com/wazo-pbx/wazo-admin-ui-switchboard.git
WORKDIR /var/tmp/wazo-admin-ui-switchboard
RUN python setup.py install

WORKDIR /var/tmp
RUN git clone https://github.com/wazo-pbx/wazo-admin-ui-paging.git
WORKDIR /var/tmp/wazo-admin-ui-paging
RUN python setup.py install

WORKDIR /var/tmp
RUN git clone https://github.com/wazo-pbx/wazo-admin-ui-voicemail.git
WORKDIR /var/tmp/wazo-admin-ui-voicemail
RUN python setup.py install

WORKDIR /var/tmp
RUN git clone https://github.com/wazo-pbx/wazo-admin-ui-moh.git
WORKDIR /var/tmp/wazo-admin-ui-moh
RUN python setup.py install

WORKDIR /var/tmp
RUN git clone https://github.com/wazo-pbx/wazo-admin-ui-incall.git
WORKDIR /var/tmp/wazo-admin-ui-incall
RUN python setup.py install

WORKDIR /var/tmp
RUN git clone https://github.com/wazo-pbx/wazo-admin-ui-outcall.git
WORKDIR /var/tmp/wazo-admin-ui-outcall
RUN python setup.py install

COPY . /usr/src/wazo-admin-ui
WORKDIR /usr/src/wazo-admin-ui

RUN python setup.py develop
