FROM python:2-alpine

WORKDIR /usr/src/app

COPY . .

CMD [ "python", "./twdvbt_xmltv.py" ]
