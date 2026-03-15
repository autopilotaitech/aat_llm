import os
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from model_manager import download_model, list_models, delete_model

try:
    from llama_cpp import Llama
    LLAMA_AVAILABLE = True
except ImportError:
    Llama = None
    LLAMA_AVAILABLE = False

MODELS_DIR = "./models"
loaded_models: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs("./web", exist_ok=True)
    yield
    loaded_models.clear()


app = FastAPI(lifespan=lifespan)


def get_model(model_name: str):
    """Lazy load and cache a model by filename."""
    model_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(model_path):
        return None
    if model_name not in loaded_models:
        if not LLAMA_AVAILABLE:
            raise RuntimeError("llama-cpp-python is not installed")
        loaded_models[model_name] = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=os.cpu_count(),
        )
    return loaded_models[model_name]


# --- Request models ---

class GenerateRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int = 512
    stream: bool = False
    temperature: float = 0.7
    top_p: float = 0.9


class ChatRequest(BaseModel):
    model: str
    messages: list[dict]
    max_tokens: int = 512
    stream: bool = False
    temperature: float = 0.7
    top_p: float = 0.9


class DeleteRequest(BaseModel):
    name: str


class PullRequest(BaseModel):
    repo_id: str
    filename: str


# --- Endpoints ---

@app.post("/api/generate")
async def api_generate(req: GenerateRequest):
    model = get_model(req.model)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Model not found: {req.model}")

    if req.stream:
        def generate_stream():
            for chunk in model(req.prompt, max_tokens=req.max_tokens,
                               temperature=req.temperature, top_p=req.top_p,
                               stream=True):
                token = chunk["choices"][0]["text"]
                yield token

        return StreamingResponse(generate_stream(), media_type="text/plain")

    output = await asyncio.to_thread(
        model, req.prompt,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_p=req.top_p,
    )
    text = output["choices"][0]["text"]
    return {"response": text, "model": req.model, "done": True}


@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    model = get_model(req.model)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Model not found: {req.model}")

    prompt = ""
    for msg in req.messages:
        prompt += f"<|im_start|>{msg['role']}\n{msg['content']}<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"

    stop = ["<|im_end|>", "<|im_start|>"]

    if req.stream:
        def generate_stream():
            for chunk in model(prompt, max_tokens=req.max_tokens,
                               temperature=req.temperature, top_p=req.top_p,
                               stop=stop, stream=True):
                token = chunk["choices"][0]["text"]
                yield token

        return StreamingResponse(generate_stream(), media_type="text/plain")

    output = await asyncio.to_thread(
        model, prompt,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_p=req.top_p,
        stop=stop,
    )
    text = output["choices"][0]["text"]
    return {"message": {"role": "assistant", "content": text.strip()}}


@app.get("/api/tags")
async def api_tags():
    models = list_models(MODELS_DIR)
    return {"models": models}


@app.delete("/api/delete")
async def api_delete(req: DeleteRequest):
    if req.name in loaded_models:
        del loaded_models[req.name]
    deleted = delete_model(req.name, MODELS_DIR)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Model not found: {req.name}")
    return {"status": "deleted", "name": req.name}


@app.get("/health")
async def health():
    return {"status": "ok", "models_loaded": len(loaded_models)}


@app.post("/api/pull")
async def api_pull(payload: PullRequest):
    repo_id = payload.repo_id
    filename = payload.filename
    asyncio.create_task(
        asyncio.to_thread(download_model, repo_id, filename)
    )
    return {"status": "downloading", "filename": filename}


@app.get("/")
async def serve_ui():
    return FileResponse("./web/index.html")


# --- Error handler ---

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)},
    )


# Static files mount — AFTER all routes
app.mount("/web", StaticFiles(directory="web"), name="web")
