FROM python:3.11.4

# RUN apt-get -y update
# RUN apt-get -y upgrade

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

EXPOSE 8000