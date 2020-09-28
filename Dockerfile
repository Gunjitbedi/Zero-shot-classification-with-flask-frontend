FROM ubuntu:18.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update && \
  apt-get install -y software-properties-common
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY ./model /app/model
COPY ./templates /app/templates
COPY ./flask_app.py /app/flask_app.py
COPY ./__init__.py /app/__init__.py

WORKDIR /app

RUN pip3 install transformers
RUN pip3 install --trusted-host download.pytorch.org torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install Flask

EXPOSE 5000

ENTRYPOINT ["python3", "flask_app.py"]