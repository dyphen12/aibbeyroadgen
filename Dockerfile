FROM python:3.7.15-bullseye

ADD application.py /

COPY requirements.txt ./

RUN apt-get update

RUN apt-get install build-essential libasound2-dev libjack-dev portaudio19-dev -y sl

RUN apt-get install libsndfile1 -y sl

RUN apt install -y fluidsynth

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . . 

CMD [ "python", "./anvilapp.py" ]
