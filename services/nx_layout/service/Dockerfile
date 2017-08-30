FROM python:latest

RUN apt-get update && apt-get install git
RUN apt-get -y install graphviz


RUN mkdir /services
WORKDIR /services

RUN pip install networkx
RUN pip install pydotplus

# TODO: replace with the new cxmate SDK.
RUN git clone https://github.com/keiono/cxmate-py.git
WORKDIR /services/cxmate-py
RUN git checkout 3-support

RUN python setup.py install

WORKDIR /services
COPY service.py ./

EXPOSE 8080

CMD ["python", "./service.py"]
