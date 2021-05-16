FROM ubuntu:20.04

LABEL maintainer="Raz Crimson"

# Running updates
RUN apt-get update -y && apt-get install -y python3-pip python3-dev

# Copying and install dependencies
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Copying source
COPY . /app

CMD [ "python3", "./run.py" ]
