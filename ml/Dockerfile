FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /mlWorkspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
