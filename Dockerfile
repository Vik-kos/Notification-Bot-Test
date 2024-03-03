FROM python:3.10

WORKDIR /code

COPY requirements.txt .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 tesseract-ocr xvfb tini -y

RUN pip install -r requirements.txt

RUN playwright install

RUN playwright install-deps


COPY ./ . 

CMD ["tini", "--", "xvfb-run", "python", "./notification_bot.py"]