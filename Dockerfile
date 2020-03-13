FROM python:3.7-stretch
ENV PYTHONUNBUFFERED 1

RUN mkdir /codeUFFERED 1

RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip

WORKDIR /code
RUN pip install --upgrade pip



ADD requirement.txt ./requirement.txt
RUN pip3 install -r requirement.txt
ADD . ./



