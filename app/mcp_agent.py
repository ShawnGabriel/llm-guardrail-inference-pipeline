from typing import Dict, Any, Callable
import datetime


class MCPAgent:
    """
    Extremely simplified, MCP-inspired agent: it exposes a registry
    of tools that can be called via name + JSON arguments.
    """

    def __init__(self):
        self.tools: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self.register_default_tools()

    def register_tool(self, name: str, func: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.tools[name] = func

    def register_default_tools(self):
        self.register_tool("get_time_utc", self.tool_get_time_utc)
        self.register_tool("echo_safe_summary", self.tool_echo_safe_summary)

    # ---- tools ----

    def tool_get_time_utc(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return {"utc_time": datetime.datetime.utcnow().isoformat() + "Z"}

    def tool_echo_safe_summary(self, args: Dict[str, Any]) -> Dict[str, Any]:
        text = str(args.get("text", ""))[:500]
        return {"summary": f"User said (truncated): {text}"}

    # ---- public API ----

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        return self.tools[tool_name](arguments)


agent = MCPAgent()
