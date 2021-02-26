FROM python:3.6

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD ./src /app
WORKDIR /app

CMD python app.py
