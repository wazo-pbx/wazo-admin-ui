FROM python:3.4
MAINTAINER Wazo Maintainers <dev@wazo.community>

ADD . /usr/src/wazo-admin-ui
WORKDIR /usr/src/wazo-admin-ui
RUN true \
    && pip install -r requirements.txt \
    && python setup.py install \
    && adduser --quiet --system --group --no-create-home --home /var/lib/wazo-admin-ui wazo-admin-ui \
    && cp -av etc/wazo-admin-ui /etc \
    && mkdir -p /etc/wazo-admin-ui/conf.d \
    && touch /var/log/wazo-admin-ui.log \
    && chown wazo-admin-ui /var/log/wazo-admin-ui.log \
    && mkdir /var/run/wazo-admin-ui/ \
    && chown wazo-admin-ui /var/run/wazo-admin-ui/ \
    && mkdir /var/lib/wazo-admin-ui/ \
    && chown wazo-admin-ui /var/lib/wazo-admin-ui/ \
    && true

ADD ./contribs/docker/certs /usr/share/xivo-certs
WORKDIR /usr/share/xivo-certs
RUN openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -nodes -config openssl.cfg -days 3650
WORKDIR /usr/src/wazo-admin-ui

EXPOSE 9296

CMD ["wazo-admin-ui", "-fd"]
