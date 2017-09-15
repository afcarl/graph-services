FROM golang:1.9

RUN apt-get update

RUN mkdir /services
WORKDIR /services

RUN wget --quiet https://github.com/cxmate/cxmate/releases/download/v0.3.0/cxmate-linux-amd64
RUN mv cxmate-linux-amd64 cxmate && chmod +x ./cxmate

COPY cxmate.json ./

EXPOSE 3000
CMD ["./cxmate"]
