FROM python:3.9-alpine3.18

WORKDIR /app
COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

COPY code/ .

RUN adduser -D fastapi \
    && chown -R fastapi:fastapi /app

USER fastapi

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
