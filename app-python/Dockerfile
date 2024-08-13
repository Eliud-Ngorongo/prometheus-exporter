FROM python:3.9-slim-buster AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.9-slim-buster
ENV DOCKERHUB_ORGANIZATION=camunda
ENV UPDATE_INTERVAL=300

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app /app

EXPOSE 2113


CMD ["python", "src/main.py"]
