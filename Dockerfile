FROM python:3.7.15-bullseye

WORKDIR /usr/src/app

ADD application.py /

COPY requirements.txt ./

RUN apt-get update

RUN apt-get install build-essential libasound2-dev libjack-dev portaudio19-dev nginx -y sl

RUN apt-get install libsndfile1 -y sl

RUN apt install -y fluidsynth

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY . . 

COPY nginx.conf /etc/nginx/nginx.conf

RUN adduser --disabled-password --gecos '' nginx

# CMD [ "gunicorn", "--bind=0.0.0.0:8000", "application:app" ]
ENTRYPOINT ["sh", "/usr/src/app/run.sh"]
