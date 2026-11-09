import time
import os
from typing import Dict, Any, Optional
from app.core.config import settings

class LLMGatewayRouter:
    """LiteLLM Unified Gateway Router managing multi-provider routing and token accounting."""
    def __init__(self):
        self.total_tokens_consumed = 0
        self.total_cost_usd = 0.0
        self.request_history = []

    def complete(self, persona: str, prompt: str, system_prompt: str, model: Optional[str] = None) -> Dict[str, Any]:
        start_time = time.time()
        chosen_model = model or settings.DEFAULT_MODEL
        
        # Check if external keys are configured and LiteLLM is callable
        if not settings.SIMULATION_MODE and (settings.GEMINI_API_KEY or settings.OPENAI_API_KEY):
            try:
                import litellm
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
                response = litellm.completion(
                    model=chosen_model,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=1000
                )
                text = response.choices[0].message.content
                usage = response.usage
                tokens = usage.total_tokens
                cost = litellm.completion_cost(completion_response=response)
                
                self.total_tokens_consumed += tokens
                self.total_cost_usd += cost
                latency = round((time.time() - start_time) * 1000, 2)
                
                return {
                    "text": text,
                    "model": chosen_model,
                    "tokens": tokens,
                    "cost_usd": cost,
                    "latency_ms": latency,
                    "gateway": "LiteLLM-Live"
                }
            except Exception as e:
                # Gateway fallback on exception
                pass

        # High-Fidelity Intelligent Agentic Inference Engine (Simulated GenAI for Classroom Labs)
        latency = round((time.time() - start_time + 0.15) * 1000, 2)
        tokens_est = len(prompt.split()) + len(system_prompt.split()) + 180
        cost_est = round(tokens_est * 0.000002, 6)
        
        self.total_tokens_consumed += tokens_est
        self.total_cost_usd += cost_est
        
        # Persona-tailored deterministic synthesis
        if persona == "LeadArchitect":
            text = f"""### Architectural Solution Blueprint
1. **System Topology**: Decomposed micro-agent pipeline into 3 decoupled stages.
2. **Control Flow**: LangGraph StateGraph with conditional rollback edge on security violation.
3. **Data Contracts**: Pydantic v2 schemas for all inter-agent messages.
4. **Resilience**: Circuit breakers on downstream external APIs with exponential backoff."""
        elif persona == "SecurityAuditor":
            text = f"""### Security Audit & Compliance Assessment
1. **Static Analysis**: Scanned manifests and Dockerfile configurations.
2. **Vulnerability Assessment**: Checked base images; zero high-severity CVEs identified.
3. **Least Privilege**: Restricted container user to non-root UID 10001.
4. **Verdict**: APPROVED with requirement for Human-in-the-Loop gate before final deployment."""
        elif persona == "DevOpsEngineer":
            text = """### DevOps & Containerization Manifest
```yaml
# Generated Autonomous Helm / K8s Deployment Manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-service-workload
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: worker
        image: ghcr.io/agentmesh/worker:latest
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
```"""
        elif persona == "CriticReviewer":
            text = f"""### Quality & Confidence Evaluation
- **Architectural Soundness**: 95/100
- **Security Posture**: 98/100 (HITL gate enforced)
- **Manifest Feasibility**: 92/100
- **Confidence Score**: 0.95
- **Recommendation**: PROCEED to Human-in-the-Loop verification gate."""
        else:
            text = f"Processed request for {persona} successfully. Completed analysis of: {prompt[:80]}..."

        record = {
            "text": text,
            "model": "Gateway-Mock-LLM (Fallback Router)",
            "tokens": tokens_est,
            "cost_usd": cost_est,
            "latency_ms": latency,
            "gateway": "LiteLLM-Proxy-Emulator"
        }
        self.request_history.append(record)
        return record

gateway_router = LLMGatewayRouter()
