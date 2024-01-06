FROM python:3.10

RUN mkdir /app

WORKDIR /app

# Cache
RUN pip install sentence-transformers

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

#CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:80", "nlp_service.app:app", "--timeout", "120"]

CMD ["uvicorn", "nlp_service.app:app", "--host", "0.0.0.0", "--port", "80"]