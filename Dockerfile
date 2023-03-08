FROM python:3.9-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .

RUN apt-get update
RUN apt-get install libmariadb-dev gcc sudo -y

RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


# Creates a non-root user with an explicit UID and adds permission to access the /app folder

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app && echo 'appuser:appuser' | chpasswd \
    && adduser appuser sudo \
    && echo 'appuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "300", "config.wsgi"]

USER root