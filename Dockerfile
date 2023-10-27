FROM python:3.11-alpine

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apk --no-cache add dcron

COPY . .

RUN touch cron.log

RUN echo "0 * * * * cd ../.. && python app/main.py --start program >> /cron.log 2>&1" > /etc/crontabs/root
