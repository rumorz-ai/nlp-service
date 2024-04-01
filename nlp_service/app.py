import os
from typing import Any, Union, List

from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from starlette.responses import JSONResponse

from fastapi import FastAPI

from smartpy.utility import os_util

app = FastAPI()
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    print(f"Request {request.method} {request.url} got exception: {exc}")
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)


# Lazy loading function
def load_embedding_model(model):
    if not hasattr(load_embedding_model, "model"):
        from sentence_transformers import SentenceTransformer
        load_embedding_model.model = SentenceTransformer(
            model,
            os_util.getTempDir('nlp-service-cache')
        )
    return load_embedding_model.model


@app.post("/ping")
async def ping():
    return {"status": "success"}


class EmbeddingsModel(BaseModel):
    text: Union[str, List[str]]
    model: str = "sentence-transformers/all-MiniLM-L6-v2"

@app.post("/embeddings")
async def get_embeddings(embeddings_model: EmbeddingsModel):
    text = embeddings_model.text
    model = embeddings_model.model
    if isinstance(text, str):
        text = [text]
    model = load_embedding_model(model)
    embeddings_list = []
    for t in text:
        embeddings_list.append(model.encode(t).tolist())
    return {
        "status": "success",
        "data":{
            "embeddings": embeddings_list
        }
    }


if __name__ == "__main__":
    uvicorn.run(app,
                host="0.0.0.0",
                port=80)
