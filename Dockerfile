FROM python:3.11.4

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


EXPOSE 8080