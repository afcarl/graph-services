FROM continuumio/miniconda3:latest

RUN apt-get update

RUN mkdir /services
WORKDIR /services

RUN wget --quiet https://github.com/cxmate/cxmate/releases/download/v0.1.0/cxmate-linux-amd64

RUN pip install cxmate
COPY cxmate.json ./

EXPOSE 80
CMD ["cxmate"]
