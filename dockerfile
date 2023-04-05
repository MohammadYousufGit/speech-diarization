FROM python:3.8.10


ADD requirements.txt /
RUN pip install -r requirements.txt
RUN apt-get -y update &&  apt-get -y  install sox
COPY ./config.ini config.ini
ADD . .
CMD [ "python", "./main.py" ]