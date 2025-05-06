FROM python:3.12

COPY . /app
WORKDIR /app/app  # ⬅️ app/main.py가 있는 곳

RUN pip install --no-cache-dir -r ../requirements.txt

EXPOSE 33333

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "33333"]