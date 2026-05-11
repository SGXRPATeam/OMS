import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialise chatbot structured logging
    from app.chatbot.core.logging import configure_chatbot_logging
    configure_chatbot_logging()

    # Warm up chatbot DB connection (non-fatal if it fails at startup)
    try:
        from app.chatbot.db.session import enable_pgvector
        await enable_pgvector()
    except Exception:
        pass

    yield

    # Graceful shutdown: close async HTTP clients
    try:
        from app.chatbot.llm.gateway import llm_gateway
        from app.chatbot.agents.oms_client import oms_client
        await llm_gateway.close()
        await oms_client.close()
    except Exception:
        pass


app = FastAPI(title="OMS Backend", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://localhost:5173",
        "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def health_check():
    return {"message": "OMS Backend Running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)