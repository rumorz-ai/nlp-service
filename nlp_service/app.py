from typing import Optional

from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from starlette.responses import JSONResponse

from fastapi import FastAPI

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


class EmbeddingsModel(BaseModel):
    text: str
    model: str
    cache_dir: str


# Lazy loading function
def load_embedding_model(model, cache_dir):
    if not hasattr(load_embedding_model, "model"):
        from sentence_transformers import SentenceTransformer
        load_embedding_model.model = SentenceTransformer(
            model,
            cache_dir
        )
    return load_embedding_model.model


@app.post("/embeddings")
async def get_embeddings(embeddings_model: EmbeddingsModel):
    text = embeddings_model.text
    model = embeddings_model.model
    cache_dir = embeddings_model.cache_dir
    model = load_embedding_model(model, cache_dir)
    return {
        "status": "success",
        "data":{
            "embeddings": model.encode(text).tolist()
        }
    }



@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    print(f"Request {request.method} {request.url} got exception: {exc}")
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)


if __name__ == "__main__":
    uvicorn.run(app,
                host="0.0.0.0",
                port=2222)
