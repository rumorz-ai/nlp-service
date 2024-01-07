## Why use an NLP Microservice?

When deploying an app with NLP features to production, there are many considerations related to deployment:
- CPU and RAM requirements + costs
- Build times
- Library dependencies and conflicts
- Model caching

## Benefits of an NLP microservice

#### Here is a sample scenario illustrating the benefits of an NLP microservice:
Imagine your application runs on 4 containers (backend, web scraper, data ETL, ops worker) and ALL of these containers need to run NLP tasks. Your NLP models have a RAM requirement of 4Gb minimum, but your app containers can run on 1Gb of RAM. When deploying, you can either:

- **Option 1 (no NLP microservice)**:
Deploy 4 containers with 4GB of RAM and run NLP tasks on all of them.
Total RAM used = 4 containers x 4Gb = **16Gb of RAM**

- **Option 2 (with NLP microservice)**: Deploy 4 containers with 1Gb of RAM + 1 NLP microservice with 4Gb of RAM
Total RAM used = 4 containers x 1Gb + 1 container (nlp service) x 4Gb = **8Gb of RAM**

By using an NLP microservice in this scenario, you are saving the costs of 8Gb of RAM.  Besides costs, there are many other benefits to isolating NLP models and Transformers behind a microservice:
- Isolated dependencies: you can install any version of torch, sentence-transformers etc without worrying about dependency conflicts with your application
- Faster builds for your app by removing dependency to heavy libraries.
- Asynchronous tasks: instead of blocking your process to run an NLP task, you'd send an async request to the microservice, allowing you to run other tasks while waiting for the model response.

## Build and run

```bash
docker build -t nlp-service .
docker run -p 80:80 nlp-service
```

## Example

The repo includes a FastAPI app with an /embeddings endpoint, as well as a python client to call the service. If you don't want to rely on the microsevice, you can still call the NLP models by using source='local'. This will download the models to the specified cache directories and run the NLP task on the same processor as your app.


```python
nlp_service = NLPService()
embeddings = loop.run_until_complete(nlp_service.get_embeddings("Your text here", source='app'))
embeddings = loop.run_until_complete(nlp_service.get_embeddings("Your text here", source='local'))
```

Deploy as Azure Container App 
```
az containerapp create \
  --name nlp-service \
  --resource-group rumorz \
  --image rumorzimages.azurecr.io/nlp-service:latest \
  --registry-server rumorzimages.azurecr.io \
  --ingress external \
  --target-port 2222
```
