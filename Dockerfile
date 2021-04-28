FROM zakaryan2004/userbot_docker:latest

ENV PATH="/app/bin:$PATH"
WORKDIR /app

RUN git clone https://github.com/noobanon/Maximus.git -b master /app

#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* ./client_secrets.json* ./secret.json* /app/

COPY ./requirements.txt /home/Maximus/userbot
RUN pip3 install -r requirements.txt
#
# Finalization
#
CMD ["python3","-m","userbot"]
