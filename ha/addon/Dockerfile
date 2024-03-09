ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_VERSION
RUN apk add --no-cache pipx
ENV PATH="${PATH}:/root/.local/bin"

RUN pipx install haco==${BUILD_VERSION}

# Remove one haco is either updated to support aiomqtt 2.0.0 or specifies needed version in setup.py
RUN pipx inject haco aiomqtt==1.2.1

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
