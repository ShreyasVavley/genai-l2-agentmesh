from typing import TypedDict, List, Dict, Any, Optional

class AgentMeshState(TypedDict):
    task_id: str
    prompt: str
    architect_plan: Optional[str]
    security_report: Optional[str]
    devops_manifest: Optional[str]
    critic_review: Optional[str]
    confidence_score: float
    current_node: str
    status: str  # initialized, in_progress, waiting_for_human, completed, rejected
    hitl_approved: bool
    high_risk_action: Optional[str]
    execution_logs: List[Dict[str, Any]]
    final_output: Optional[str]
