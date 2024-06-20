FROM python:3.12

COPY /build/requirements.txt /code/
COPY /app /code/
COPY local.env /code/

RUN pip install --upgrade pip && pip install -r /code/requirements.txt