FROM python:2.7.9
MAINTAINER Wazo Maintainers <dev@wazo.community>

# Install wazo-admin-ui
ADD . /usr/src/wazo-admin-ui
WORKDIR /usr/src/wazo-admin-ui
RUN pip install -r requirements.txt
RUN python setup.py install

# Configure environment
RUN adduser --quiet --system --group --no-create-home --home /var/lib/wazo-admin-ui wazo-admin-ui \
RUN cp -av etc/wazo-admin-ui /etc
RUN mkdir -p /etc/wazo-admin-ui/conf.d

RUN touch /var/log/wazo-admin-ui.log
RUN chown wazo-admin-ui /var/log/wazo-admin-ui.log

RUN mkdir /var/run/wazo-admin-ui/
RUN chown wazo-admin-ui /var/run/wazo-admin-ui/

RUN mkdir /var/lib/wazo-admin-ui/
RUN chown wazo-admin-ui /var/lib/wazo-admin-ui/

ADD ./contribs/docker/certs /usr/share/xivo-certs
WORKDIR /usr/share/xivo-certs
RUN openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -nodes -config openssl.cfg -days 3650
WORKDIR /usr/src/wazo-admin-ui

EXPOSE 9296

CMD ["wazo-admin-ui", "-fd"]
