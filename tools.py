"""
AI Agent Tools - Provides various capabilities for the AI agent
"""
import os
import json
import requests
from datetime import datetime
from duckduckgo_search import DDGS
import subprocess
import sys

class AgentTools:
    """Collection of tools that the AI agent can use"""
    
    @staticmethod
    def web_search(query, max_results=5):
        """
        Search the web using DuckDuckGo
        Args:
            query: Search query string
            max_results: Maximum number of results to return
        Returns:
            List of search results with title, link, and snippet
        """
        try:
            ddgs = DDGS()
            results = []
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    'title': r.get('title', ''),
                    'link': r.get('href', ''),
                    'snippet': r.get('body', '')
                })
            return {
                'success': True,
                'results': results,
                'query': query
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'query': query
            }
    
    @staticmethod
    def get_current_time():
        """Get current date and time"""
        now = datetime.now()
        return {
            'success': True,
            'datetime': now.strftime("%Y-%m-%d %H:%M:%S"),
            'date': now.strftime("%Y-%m-%d"),
            'time': now.strftime("%H:%M:%S"),
            'day': now.strftime("%A"),
            'timestamp': now.timestamp()
        }
    
    @staticmethod
    def calculate(expression):
        """
        Safely evaluate mathematical expressions
        Args:
            expression: Mathematical expression as string
        Returns:
            Result of the calculation
        """
        try:
            # Remove any dangerous characters
            allowed_chars = set('0123456789+-*/().,% ')
            if not all(c in allowed_chars for c in expression):
                return {
                    'success': False,
                    'error': 'Invalid characters in expression'
                }
            
            result = eval(expression, {"__builtins__": {}}, {})
            return {
                'success': True,
                'expression': expression,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'expression': expression
            }
    
    @staticmethod
    def read_file(file_path):
        """
        Read content from a file
        Args:
            file_path: Path to the file
        Returns:
            File content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                'success': True,
                'file_path': file_path,
                'content': content,
                'size': len(content)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_path': file_path
            }
    
    @staticmethod
    def write_file(file_path, content):
        """
        Write content to a file
        Args:
            file_path: Path to the file
            content: Content to write
        Returns:
            Success status
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {
                'success': True,
                'file_path': file_path,
                'bytes_written': len(content)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_path': file_path
            }
    
    @staticmethod
    def list_directory(directory_path='.'):
        """
        List files and directories in a given path
        Args:
            directory_path: Path to directory
        Returns:
            List of files and directories
        """
        try:
            items = os.listdir(directory_path)
            files = []
            directories = []
            
            for item in items:
                full_path = os.path.join(directory_path, item)
                if os.path.isfile(full_path):
                    files.append({
                        'name': item,
                        'size': os.path.getsize(full_path),
                        'modified': datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M:%S")
                    })
                elif os.path.isdir(full_path):
                    directories.append(item)
            
            return {
                'success': True,
                'directory': directory_path,
                'files': files,
                'directories': directories,
                'total_items': len(items)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'directory': directory_path
            }
    
    @staticmethod
    def execute_python_code(code):
        """
        Execute Python code safely (limited capabilities)
        Args:
            code: Python code to execute
        Returns:
            Execution result
        """
        try:
            # Create a temporary file
            temp_file = 'temp_code.py'
            with open(temp_file, 'w') as f:
                f.write(code)
            
            # Execute the code
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
        except Exception as e:
            # Clean up on error
            if os.path.exists('temp_code.py'):
                os.remove('temp_code.py')
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_weather(location):
        """
        Get weather information for a location using web search
        Args:
            location: City or location name
        Returns:
            Weather information
        """
        try:
            search_query = f"weather in {location} today"
            search_result = AgentTools.web_search(search_query, max_results=3)
            
            if search_result['success']:
                return {
                    'success': True,
                    'location': location,
                    'info': search_result['results']
                }
            else:
                return search_result
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'location': location
            }
    
    @staticmethod
    def create_directory(directory_path):
        """
        Create a new directory
        Args:
            directory_path: Path for the new directory
        Returns:
            Success status
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            return {
                'success': True,
                'directory': directory_path
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'directory': directory_path
            }

# Tool definitions for the AI to understand
TOOL_DEFINITIONS = {
    "web_search": {
        "name": "web_search",
        "description": "Search the web using DuckDuckGo. Use this to find current information, facts, news, or any information not in your knowledge base.",
        "parameters": {
            "query": "The search query string",
            "max_results": "Maximum number of results (default: 5)"
        },
        "example": "web_search('latest AI news', 5)"
    },
    "get_current_time": {
        "name": "get_current_time",
        "description": "Get the current date and time. Use this when user asks about current time, date, day of week.",
        "parameters": {},
        "example": "get_current_time()"
    },
    "calculate": {
        "name": "calculate",
        "description": "Perform mathematical calculations. Use this for math problems, computations, or numerical operations.",
        "parameters": {
            "expression": "Mathematical expression as string (e.g., '2+2', '10*5/2')"
        },
        "example": "calculate('2+2*5')"
    },
    "read_file": {
        "name": "read_file",
        "description": "Read content from a file. Use this to access file contents when requested.",
        "parameters": {
            "file_path": "Path to the file to read"
        },
        "example": "read_file('example.txt')"
    },
    "write_file": {
        "name": "write_file",
        "description": "Write content to a file. Use this to create or modify files.",
        "parameters": {
            "file_path": "Path to the file",
            "content": "Content to write to the file"
        },
        "example": "write_file('output.txt', 'Hello World')"
    },
    "list_directory": {
        "name": "list_directory",
        "description": "List files and directories in a path. Use this to explore directory contents.",
        "parameters": {
            "directory_path": "Path to directory (default: current directory)"
        },
        "example": "list_directory('.')"
    },
    "execute_python_code": {
        "name": "execute_python_code",
        "description": "Execute Python code. Use this to run Python scripts or code snippets.",
        "parameters": {
            "code": "Python code to execute"
        },
        "example": "execute_python_code('print(\"Hello World\")')"
    },
    "get_weather": {
        "name": "get_weather",
        "description": "Get weather information for a location. Use this when user asks about weather.",
        "parameters": {
            "location": "City or location name"
        },
        "example": "get_weather('New York')"
    },
    "create_directory": {
        "name": "create_directory",
        "description": "Create a new directory. Use this to create folders.",
        "parameters": {
            "directory_path": "Path for the new directory"
        },
        "example": "create_directory('new_folder')"
    }
}

def execute_tool(tool_name, **kwargs):
    """
    Execute a tool by name with given parameters
    Args:
        tool_name: Name of the tool to execute
        **kwargs: Parameters for the tool
    Returns:
        Tool execution result
    """
    tools = AgentTools()
    
    if hasattr(tools, tool_name):
        tool_func = getattr(tools, tool_name)
        return tool_func(**kwargs)
    else:
        return {
            'success': False,
            'error': f'Tool {tool_name} not found'
        }
