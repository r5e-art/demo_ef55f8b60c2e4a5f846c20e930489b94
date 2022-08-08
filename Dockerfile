FROM python:3

WORKDIR /app

COPY requirements.txt ./
COPY ./src/ ./
RUN pip install --no-cache-dir -r requirements.txt


CMD [ "flask", "--app", "my_www", "run" ]