FROM nikolaik/python-nodejs:latest

RUN apt-get update \
    && apt-get install -y build-essential  make flex \
    && apt-get upgrade -y

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

RUN cp -r converters convertersbak

RUN cd converters \
    && make

EXPOSE 8080

CMD ["node","app.js"]
