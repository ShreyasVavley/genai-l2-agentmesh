from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from app.graph.workflow import start_mesh_run, approve_hitl_action, TASK_STORE
from app.tools.registry import tool_registry
from app.gateway.router import gateway_router
from app.observability.tracer import tracer

router = APIRouter()

class MeshRunRequest(BaseModel):
    prompt: str = Field(..., example="Architect and deploy an asynchronous payment verification microservice with zero-trust security.")

class HITLApprovalRequest(BaseModel):
    task_id: str
    approved: bool = True

@router.post("/run")
async def trigger_mesh_run(request: MeshRunRequest):
    """Triggers LangGraph multi-agent workflow."""
    state = start_mesh_run(request.prompt)
    return {
        "message": "Mesh run initialized",
        "task_id": state["task_id"],
        "status": state["status"],
        "current_node": state["current_node"],
        "high_risk_action": state["high_risk_action"],
        "requires_hitl_approval": state["status"] == "waiting_for_human",
        "confidence_score": state["confidence_score"]
    }

@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """Retrieves current state, personas' outputs, and execution logs."""
    state = TASK_STORE.get(task_id)
    if not state:
        raise HTTPException(status_code=404, detail="Task ID not found")
    traces = tracer.get_trace(task_id)
    return {
        "state": state,
        "traces": traces
    }

@router.post("/approve")
async def approve_task(request: HITLApprovalRequest):
    """Human-in-the-Loop gate approval or rejection."""
    try:
        updated_state = approve_hitl_action(request.task_id, request.approved)
        return {
            "message": f"Task {'approved and resumed' if request.approved else 'rejected'}",
            "task_id": request.task_id,
            "status": updated_state["status"],
            "final_output": updated_state["final_output"]
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/tools")
async def list_tools():
    """MCP (Model Context Protocol) Dynamic Tool Discovery."""
    return {
        "protocol": "Model Context Protocol (MCP) 2026",
        "tools": tool_registry.discover_tools()
    }

@router.get("/metrics")
async def get_metrics():
    """Observability metrics: LiteLLM gateway tokens, costs, and span metrics."""
    return {
        "gateway": {
            "total_tokens_consumed": gateway_router.total_tokens_consumed,
            "total_cost_usd": round(gateway_router.total_cost_usd, 6),
            "total_requests": len(gateway_router.request_history)
        },
        "tracing": tracer.get_summary_metrics()
    }
