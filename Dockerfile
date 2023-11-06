FROM python:3.11.4

# RUN apt-get -y update
# RUN apt-get -y upgrade

WORKDIR /Users/rara/myapp

COPY requirements.txt /Users/rara/myapp/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /Users/rara/myapp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

EXPOSE 8000