FROM python:3

WORKDIR /app

COPY requirements.txt ./
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000/tcp
EXPOSE 80/tcp

CMD [ "/app/bin/run.sh" ]