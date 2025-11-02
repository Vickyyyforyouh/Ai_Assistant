"""
AI Agent Engine - Manages agent reasoning, planning, and tool execution
"""
import json
import re
from tools import execute_tool, TOOL_DEFINITIONS

class AgentEngine:
    """AI Agent with reasoning and tool-using capabilities"""
    
    def __init__(self):
        self.tools = TOOL_DEFINITIONS
        self.max_iterations = 5
    
    def create_system_prompt(self):
        """Create system prompt with tool information"""
        tools_info = "Available Tools:\n"
        for tool_name, tool_info in self.tools.items():
            tools_info += f"\n{tool_name}:\n"
            tools_info += f"  Description: {tool_info['description']}\n"
            tools_info += f"  Example: {tool_info['example']}\n"
        
        system_prompt = f"""You are an advanced AI agent with the ability to use tools and reason about tasks.

{tools_info}

When you need to use a tool, respond in this exact format:
TOOL_CALL: tool_name
PARAMETERS: {{"param1": "value1", "param2": "value2"}}

After receiving tool results, you can either:
1. Use another tool if needed (for multi-step tasks)
2. Provide a final answer to the user

Always explain your reasoning and what you're doing.
Be helpful, accurate, and proactive in solving user problems.
Think step-by-step for complex tasks.
"""
        return system_prompt
    
    def parse_tool_call(self, message):
        """
        Parse tool calls from AI message
        Returns: (tool_name, parameters) or (None, None) if no tool call
        """
        if "TOOL_CALL:" not in message:
            return None, None
        
        try:
            # Extract tool name
            tool_match = re.search(r'TOOL_CALL:\s*(\w+)', message)
            if not tool_match:
                return None, None
            tool_name = tool_match.group(1)
            
            # Extract parameters
            params_match = re.search(r'PARAMETERS:\s*({.*?})', message, re.DOTALL)
            if params_match:
                params_str = params_match.group(1)
                parameters = json.loads(params_str)
            else:
                parameters = {}
            
            return tool_name, parameters
        except Exception as e:
            print(f"Error parsing tool call: {e}")
            return None, None
    
    def execute_tool_call(self, tool_name, parameters):
        """Execute a tool and return results"""
        try:
            result = execute_tool(tool_name, **parameters)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def should_continue(self, message):
        """Check if agent should continue with another iteration"""
        # Continue if there's a tool call
        if "TOOL_CALL:" in message:
            return True
        return False
    
    def format_tool_result(self, tool_name, result):
        """Format tool result for AI consumption"""
        return f"\nTOOL_RESULT from {tool_name}:\n{json.dumps(result, indent=2)}\n"
    
    def detect_intent(self, message):
        """
        Detect user intent and suggest appropriate tools
        Returns: List of suggested tools
        """
        message_lower = message.lower()
        suggestions = []
        
        # Search-related keywords
        if any(word in message_lower for word in ['search', 'find', 'look up', 'google', 'what is', 'who is', 'tell me about']):
            suggestions.append('web_search')
        
        # Time-related keywords
        if any(word in message_lower for word in ['time', 'date', 'today', 'now', 'current']):
            suggestions.append('get_current_time')
        
        # Math-related keywords
        if any(word in message_lower for word in ['calculate', 'compute', 'math', '+', '-', '*', '/', 'sum', 'multiply']):
            suggestions.append('calculate')
        
        # File-related keywords
        if any(word in message_lower for word in ['read file', 'open file', 'file content']):
            suggestions.append('read_file')
        
        if any(word in message_lower for word in ['write file', 'save file', 'create file']):
            suggestions.append('write_file')
        
        if any(word in message_lower for word in ['list files', 'show files', 'directory']):
            suggestions.append('list_directory')
        
        # Weather-related keywords
        if any(word in message_lower for word in ['weather', 'temperature', 'forecast']):
            suggestions.append('get_weather')
        
        # Code execution keywords
        if any(word in message_lower for word in ['run python', 'execute code', 'run code', 'python code']):
            suggestions.append('execute_python_code')
        
        return suggestions
    
    def enhance_message_with_intent(self, message):
        """Add tool suggestions to user message"""
        suggestions = self.detect_intent(message)
        if suggestions:
            enhanced = message + f"\n\n[System: Consider using these tools: {', '.join(suggestions)}]"
            return enhanced
        return message
