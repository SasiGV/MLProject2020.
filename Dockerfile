FROM python:3.8.7

LABEL Author="Sasikala Varatharajan"

#ENV PYTHONDONTWRITEBYTECODE 1
#ENV FLASK_APP=server.py
#ENV FLASK_ENV=server.py
#ENV FLASK_DEBUG True


WORKDIR /usr/src/app

COPY requirements.txt ./


RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

ENV FLASK_APP=server.py
ENV FLASK_ENV-server.py

EXPOSE 5000

CMD flask run --host=127.0.0.1
