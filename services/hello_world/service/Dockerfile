FROM continuumio/miniconda3:latest

RUN apt-get update

RUN mkdir /services
WORKDIR /services

RUN conda install networkx
RUN pip install cxmate

COPY service.py ./

EXPOSE 8080
CMD ["python", "./service.py"]
