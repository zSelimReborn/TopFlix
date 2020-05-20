FROM python:3

ENV APP ../../app

RUN mkdir $APP
WORKDIR $APP

EXPOSE 5000

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install http://github.com/pythonforfacebook/facebook-sdk/tarball/master

COPY . .

CMD [ "uwsgi", "--ini", "app.ini" ]
