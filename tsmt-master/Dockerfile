from python:3.7-buster

COPY . /var/www/tsmt
WORKDIR /var/www/tsmt

RUN apt-get update
RUN pip3 install -r requirements.txt
RUN python3 manage.py migrate

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
