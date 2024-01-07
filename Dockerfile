FROM python:3.10

RUN pip install sentence-transformers
RUN pip install nltk


ENV NLP_CACHE_DIR=/app/nlp_cache

RUN mkdir -p /app/nlp_cache

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 80
CMD ["uvicorn", "nlp_service.app:app", "--host", "0.0.0.0", "--port", "80"]
