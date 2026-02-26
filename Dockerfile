# Base image containing Python runtime
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR ./app

# Install the dependencies listed in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
EXPOSE 8080

CMD ["streamlit", "run", "src/frontend/Copilot.py", "--server.port=8080", "--server.address=0.0.0.0"]