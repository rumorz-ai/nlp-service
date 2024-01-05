FROM python:3.10

RUN mkdir /app

WORKDIR /app

# Copy only the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:2222", "nlp_service.app:app", "--timeout", "120"]
