FROM python:3.11-slim

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install --upgrade pip pipenv && \
    pipenv install --system --deploy

COPY main.py .

CMD ["python", "main.py"]
