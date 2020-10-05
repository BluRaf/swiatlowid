FROM python:3.8-alpine

RUN apk add --no-cache git

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

ADD . /home/appuser/swiatlowid
WORKDIR /home/appuser/swiatlowid

ENV PATH=/home/appuser/.local/bin:$PATH

RUN pip install --user -r requirements.txt

ENTRYPOINT [ "python", "-m", "swiatlowid" ]
