FROM python:3.8-alpine3.11

RUN apk add --no-cache --virtual .build_deps \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
&& pip install \
    'python-telegram-bot>=12.4' \
&& apk del .build_deps \
&& mkdir -p /bot/data

COPY ./* /bot/

WORKDIR /bot

CMD ["/usr/local/bin/python", "/bot/bot.py"]