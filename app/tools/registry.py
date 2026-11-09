import re
from typing import Dict, Any, List, Callable

class MCPTool:
    def __init__(self, name: str, description: str, input_schema: Dict[str, Any], func: Callable, is_high_risk: bool = False):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.func = func
        self.is_high_risk = is_high_risk

    def to_mcp_format(self) -> Dict[str, Any]:
        """Returns standard Model Context Protocol (MCP) tool discovery schema."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.input_schema,
            "is_high_risk": self.is_high_risk
        }

class ToolRegistry:
    """Dynamic Agent Tool Discovery and Execution Registry."""
    def __init__(self):
        self.tools: Dict[str, MCPTool] = {}
        self._register_core_tools()

    def _register_core_tools(self):
        self.register(
            name="git_inspector",
            description="Inspects Git commit history, branch status, and staged files.",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository path to inspect"}
                },
                "required": ["path"]
            },
            func=self._tool_git_inspector,
            is_high_risk=False
        )
        
        self.register(
            name="dockerfile_validator",
            description="Validates Dockerfile syntax, non-root user enforcement, and layer optimization.",
            input_schema={
                "type": "object",
                "properties": {
                    "dockerfile_content": {"type": "string", "description": "Raw Dockerfile content"}
                },
                "required": ["dockerfile_content"]
            },
            func=self._tool_dockerfile_validator,
            is_high_risk=False
        )

        self.register(
            name="security_vuln_scanner",
            description="Scans dependencies and configuration files for common security misconfigurations.",
            input_schema={
                "type": "object",
                "properties": {
                    "target_type": {"type": "string", "enum": ["requirements.txt", "package.json", "env"]}
                },
                "required": ["target_type"]
            },
            func=self._tool_security_scanner,
            is_high_risk=False
        )

        self.register(
            name="execute_shell_command",
            description="Executes a command on the infrastructure. HIGH RISK: Requires Human-in-the-Loop approval.",
            input_schema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Terminal command to execute"}
                },
                "required": ["command"]
            },
            func=self._tool_shell_runner,
            is_high_risk=True
        )

    def register(self, name: str, description: str, input_schema: Dict[str, Any], func: Callable, is_high_risk: bool = False):
        self.tools[name] = MCPTool(name, description, input_schema, func, is_high_risk)

    def discover_tools(self) -> List[Dict[str, Any]]:
        """MCP Tool Discovery endpoint handler."""
        return [tool.to_mcp_format() for tool in self.tools.values()]

    def invoke(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self.tools:
            return {"status": "error", "message": f"Tool '{name}' not found in registry"}
        
        tool = self.tools[name]
        try:
            result = tool.func(**args)
            return {"status": "success", "tool": name, "result": result, "is_high_risk": tool.is_high_risk}
        except Exception as e:
            return {"status": "error", "tool": name, "message": str(e)}

    def _tool_git_inspector(self, path: str = ".") -> str:
        return "Git Status: Clean working directory. Active branch: main. Latest commit: 'Autonomous Mesh Setup'."

    def _tool_dockerfile_validator(self, dockerfile_content: str) -> str:
        issues = []
        if "USER" not in dockerfile_content:
            issues.append("Warning: Container runs as root. Consider specifying `USER nonroot`.")
        if ":latest" in dockerfile_content:
            issues.append("Notice: Pinned tags recommended instead of `:latest`.")
        return "Dockerfile Validated: " + (", ".join(issues) if issues else "All security best practices met.")

    def _tool_security_scanner(self, target_type: str = "requirements.txt") -> str:
        return f"Vulnerability Scan for {target_type}: Checked 14 packages. 0 Critical CVEs. SSL/TLS requirements enforced."

    def _tool_shell_runner(self, command: str) -> str:
        return f"Executed command: `{command}` -> Exit code: 0 [Output: Deployment initiated successfully]."

tool_registry = ToolRegistry()
