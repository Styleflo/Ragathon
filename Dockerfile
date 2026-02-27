# Base image containing Python runtime
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR ./app

# Install the dependencies listed in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]