FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG APP_DIR=/code/
RUN mkdir ${APP_DIR}

ADD requirements.txt ${APP_DIR}
ADD wait_for.sh .
RUN chmod +x wait_for.sh
RUN set -ex \
    && pip install -r ${APP_DIR}requirements.txt

COPY shop_project  ${APP_DIR}

WORKDIR ${APP_DIR}
