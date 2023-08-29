ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_VERSION
RUN pip install haco==${BUILD_VERSION}

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]