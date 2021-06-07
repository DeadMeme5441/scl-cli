FROM nikolaik/python-nodejs:latest

RUN apt-get update \
    && apt-get install -y build-essential make flex lttoolbox\
    && apt-get upgrade -y

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

RUN cp -r converters convertersbak

RUN cd converters \
    && make

RUN cd SHMT/prog/sandhi_splitter \
    && make

RUN cd SHMT/prog/Normalisation \
    && make

EXPOSE 8080

CMD ["node","app.js"]
