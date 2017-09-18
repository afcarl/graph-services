FROM python:2.7

RUN apt-get update && apt-get install git

RUN mkdir /services
WORKDIR /services

RUN pip install python-igraph seaborn

RUN git clone https://github.com/cxmate/cxmate-py.git
WORKDIR /services/cxmate-py

RUN python setup.py install

WORKDIR /services
COPY *.py ./

EXPOSE 8080

CMD ["python", "./service.py"]
