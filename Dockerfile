FROM python:3.10

WORKDIR /code

COPY requirements.txt .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

RUN apt install tesseract-ocr -y

RUN pip install -r requirements.txt

RUN playwright install

RUN playwright install-deps


COPY ./ . 

CMD ["python", "./notification_bot.py"]