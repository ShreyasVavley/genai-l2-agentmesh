import os
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import router as v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Autonomous Multi-Agent DevOps & Audit Mesh with LangGraph, LiteLLM, MCP, and Human-in-the-Loop for GenAI Level 2 (44 Days Mysore)",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["X-Mesh-Latency"] = f"{duration * 1000:.2f}ms"
    return response

template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")

@app.get("/", response_class=HTMLResponse, tags=["Agentic Cockpit UI"])
async def cockpit():
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>AgenticDevOps Mesh Active</h1><p>Visit <a href='/docs'>/docs</a></p>")

app.include_router(v1_router, prefix=settings.API_V1_STR + "/mesh", tags=["Agentic Mesh"])

print("AgenticDevOps Mesh L2 Initialized successfully.")
