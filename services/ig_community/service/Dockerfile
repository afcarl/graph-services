FROM python:2.7

RUN apt-get update && apt-get install git

RUN mkdir /services
WORKDIR /services

RUN pip install numpy scipy python-igraph

# TODO: replace with the new cxmate SDK.
RUN git clone https://github.com/keiono/cxmate-py.git
WORKDIR /services/cxmate-py
RUN git checkout 3-support

RUN python setup.py install

WORKDIR /services
COPY *.py ./

EXPOSE 8080

CMD ["python", "./service.py"]
