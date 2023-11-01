ARG VERSION
ARG TYPE=development

FROM edwardbrown/python as base
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update -y

FROM base AS development
WORKDIR /usr/src
COPY . .
RUN pip install .

FROM base AS release
RUN if [ -z "$VERSION" ] ; then pip3 install haco ; else pip3 install haco==${VERSION} ; fi


FROM ${TYPE} as image

CMD haco-daemon


