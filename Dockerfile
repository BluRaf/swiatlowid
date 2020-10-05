FROM python:3.8-slim

RUN apt update
RUN apt install -y git

RUN useradd --create-home bot
USER bot

ADD . /home/bot/swiatlowid
WORKDIR /home/bot/swiatlowid

ENV PATH=/home/bot/.local/bin:$PATH

RUN pip install --user -r requirements.txt

ENTRYPOINT [ "python", "-m", "swiatlowid" ]
