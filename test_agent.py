"""
Test script to demonstrate AI Agent capabilities
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Pretty print API response"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)
    if response.status_code == 200:
        data = response.json()
        print(f"Reply: {data.get('reply', 'No reply')}")
        if 'tool_calls' in data and data['tool_calls']:
            print(f"\nTool Calls Made: {len(data['tool_calls'])}")
            for i, tool_call in enumerate(data['tool_calls'], 1):
                print(f"\n  Tool {i}: {tool_call['tool']}")
                print(f"  Parameters: {tool_call['parameters']}")
                print(f"  Success: {tool_call['result'].get('success', False)}")
        if 'iterations' in data:
            print(f"\nIterations: {data['iterations']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    print("="*60 + "\n")

def test_web_search():
    """Test web search capability"""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "Search the web for latest AI news"},
        headers={"Content-Type": "application/json"}
    )
    print_response("WEB SEARCH TEST", response)

def test_time():
    """Test current time capability"""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "What is the current time and date?"},
        headers={"Content-Type": "application/json"}
    )
    print_response("TIME TEST", response)

def test_math():
    """Test calculation capability"""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "Calculate 156 * 789 + 4321"},
        headers={"Content-Type": "application/json"}
    )
    print_response("MATH TEST", response)

def test_weather():
    """Test weather capability"""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "What's the weather like in Tokyo?"},
        headers={"Content-Type": "application/json"}
    )
    print_response("WEATHER TEST", response)

def test_file_operations():
    """Test file read/write capability"""
    # First create a file
    response1 = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "Write 'Hello from AI Agent!' to a file called test_output.txt"},
        headers={"Content-Type": "application/json"}
    )
    print_response("FILE WRITE TEST", response1)
    
    # Then read it back
    response2 = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "Read the content of test_output.txt"},
        headers={"Content-Type": "application/json"}
    )
    print_response("FILE READ TEST", response2)

def test_directory_listing():
    """Test directory listing capability"""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "List all files in the current directory"},
        headers={"Content-Type": "application/json"}
    )
    print_response("DIRECTORY LISTING TEST", response)

def test_code_execution():
    """Test Python code execution"""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "Run Python code to print 'Hello World' and calculate 2+2"},
        headers={"Content-Type": "application/json"}
    )
    print_response("CODE EXECUTION TEST", response)

def test_multi_step():
    """Test multi-step reasoning"""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "First get the current time, then search for news about AI, and finally calculate 100 * 50"},
        headers={"Content-Type": "application/json"}
    )
    print_response("MULTI-STEP TEST", response)

def test_list_tools():
    """List all available tools"""
    response = requests.get(f"{BASE_URL}/tools")
    print("\n" + "="*60)
    print("  AVAILABLE TOOLS")
    print("="*60)
    if response.status_code == 200:
        data = response.json()
        tools = data.get('tools', {})
        for tool_name, tool_info in tools.items():
            print(f"\n{tool_name}:")
            print(f"  {tool_info['description']}")
            print(f"  Example: {tool_info['example']}")
    print("="*60 + "\n")

def test_direct_tool_execution():
    """Test direct tool execution endpoint"""
    response = requests.post(
        f"{BASE_URL}/execute-tool",
        json={
            "tool_name": "calculate",
            "parameters": {"expression": "2+2"}
        },
        headers={"Content-Type": "application/json"}
    )
    print("\n" + "="*60)
    print("  DIRECT TOOL EXECUTION TEST")
    print("="*60)
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    print("="*60 + "\n")

def run_all_tests():
    """Run all tests"""
    print("\n" + "#"*60)
    print("#  AI AGENT CAPABILITIES TEST SUITE")
    print("#"*60)
    
    # List available tools first
    test_list_tools()
    
    # Test basic capabilities
    print("\n### BASIC CAPABILITIES ###\n")
    test_time()
    test_math()
    
    # Test web capabilities
    print("\n### WEB CAPABILITIES ###\n")
    test_web_search()
    test_weather()
    
    # Test file operations
    print("\n### FILE OPERATIONS ###\n")
    test_file_operations()
    test_directory_listing()
    
    # Test code execution
    print("\n### CODE EXECUTION ###\n")
    test_code_execution()
    
    # Test direct tool execution
    print("\n### DIRECT TOOL EXECUTION ###\n")
    test_direct_tool_execution()
    
    # Test multi-step reasoning
    print("\n### MULTI-STEP REASONING ###\n")
    test_multi_step()
    
    print("\n" + "#"*60)
    print("#  ALL TESTS COMPLETED")
    print("#"*60 + "\n")

if __name__ == "__main__":
    print("\nMake sure the Flask server is running at http://localhost:5000")
    input("Press Enter to start tests...")
    run_all_tests()
    print("\nTesting complete!")
    input("Press Enter to exit...")
