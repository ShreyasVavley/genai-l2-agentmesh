from fastapi.testclient import TestClient
from app.main import app
from app.tools.registry import tool_registry

client = TestClient(app)

def test_mcp_tool_discovery():
    tools = tool_registry.discover_tools()
    assert len(tools) >= 4
    tool_names = [t["name"] for t in tools]
    assert "git_inspector" in tool_names
    assert "execute_shell_command" in tool_names
    
    shell_tool = next(t for t in tools if t["name"] == "execute_shell_command")
    assert shell_tool["is_high_risk"] is True

def test_trigger_mesh_workflow_hitl():
    # 1. Trigger mission
    response = client.post("/api/v1/mesh/run", json={
        "prompt": "Deploy secure payment service"
    })
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    task_id = data["task_id"]
    assert data["requires_hitl_approval"] is True
    assert data["status"] == "waiting_for_human"

    # 2. Check task status
    status_res = client.get(f"/api/v1/mesh/status/{task_id}")
    assert status_res.status_code == 200
    state_data = status_res.json()["state"]
    assert state_data["architect_plan"] is not None
    assert state_data["security_report"] is not None
    assert state_data["confidence_score"] >= 0.75

    # 3. Approve via HITL gate
    approve_res = client.post("/api/v1/mesh/approve", json={
        "task_id": task_id,
        "approved": True
    })
    assert approve_res.status_code == 200
    assert approve_res.json()["status"] == "completed"

def test_observability_metrics():
    response = client.get("/api/v1/mesh/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "gateway" in data
    assert "tracing" in data
    assert data["gateway"]["total_tokens_consumed"] > 0
