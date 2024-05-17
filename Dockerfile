FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY main.py main.py
COPY ./static /code/static

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt 

#Docker이미지를 빌드하는데 필요한 지시문을 포함. python환경을 정의하고 필요한 의존성을 설치한 후 애플리케이션을 실행하는데 필요한 명령을 정의
