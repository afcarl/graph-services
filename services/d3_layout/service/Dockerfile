FROM node:8

RUN mkdir /services
WORKDIR /services


COPY ./package.json ./
RUN npm install && npm install forever -g

COPY ./src/* ./
RUN ls -alh

EXPOSE 8080

CMD ["node", "./app.js"]
