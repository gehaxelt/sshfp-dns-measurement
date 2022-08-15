FROM python:3

WORKDIR /app/

RUN apt update
RUN apt install -y openssh-client
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "/app/app.py" ]