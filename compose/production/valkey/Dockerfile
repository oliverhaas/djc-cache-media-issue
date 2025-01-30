FROM valkey/valkey:8.0
COPY ./compose/production/valkey/valkey.conf /usr/local/etc/valkey/valkey.conf
CMD [ "valkey-server", "/usr/local/etc/valkey/valkey.conf" ]
