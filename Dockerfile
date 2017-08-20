FROM node:latest

ENV APPDIR=/app

WORKDIR $APPDIR

COPY server/package.json .
RUN npm install

COPY . .
WORKDIR server

CMD npm start
