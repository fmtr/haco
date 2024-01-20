ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_VERSION
RUN apk add --no-cache pipx
ENV PATH="${PATH}:/root/.local/bin"

RUN pipx install haco==${BUILD_VERSION}

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
