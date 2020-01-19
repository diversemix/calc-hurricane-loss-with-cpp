FROM python:3.7

WORKDIR /app
RUN apt-get update && apt-get -y install build-essential python3-venv python3-pip

# Now cache some of the requirements inside the container
COPY requirements-dev.txt .
RUN pip install --upgrade -r requirements-dev.txt
CMD [ "make" ]
