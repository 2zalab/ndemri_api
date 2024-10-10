FROM python:3.10.8

WORKDIR /code

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN #apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 libgl1 python3-opencv -y

RUN pip install opencv-python

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000
COPY . .

CMD [ "python", "app.py" ]