from flask import Flask, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta
import os
import json
import requests
from agent_engine import AgentEngine
from tools import execute_tool

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # Session expires in 2 hours

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Get OpenRouter API key from environment variables (free alternative)
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
# If no OpenRouter key, fall back to Hugging Face key
api_key = openrouter_api_key or os.getenv('HUGGINGFACE_API_KEY')

if not api_key:
    raise ValueError("API key not found in environment variables. Please set either OPENROUTER_API_KEY or HUGGINGFACE_API_KEY")

# OpenRouter configuration (free alternative)
if openrouter_api_key:
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    API_HEADERS = {
        "Authorization": f"Bearer {openrouter_api_key}",  # Use the specific key
        "HTTP-Referer": "http://localhost:5000",  # Optional, for openrouter stats
        "X-Title": "AI Assistant",  # Optional, for openrouter stats
        "Content-Type": "application/json"
    }
    # Using a free model that's known to work
    MODEL = "nvidia/nemotron-nano-9b-v2:free"
else:
    # Fallback to Hugging Face
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    API_HEADERS = {"Authorization": f"Bearer {api_key}"}
    MODEL = None

# Initialize agent engine
agent_engine = AgentEngine()

# Initialize conversation history in session
def get_conversation():
    if 'conversation' not in session:
        # Use agent system prompt instead of basic prompt
        session['conversation'] = [
            {"role": "system", "content": agent_engine.create_system_prompt()}
        ]
    return session['conversation']

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'AI Assistant Backend is running',
        'version': '1.0.0'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages with agentic capabilities
    Expects JSON: {"message": "user message"}
    Returns: {"reply": "AI response", "tool_calls": [], "iterations": 0}
    """
    try:
        # Get user message from request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data['message']
        
        # Get conversation history
        conversation = get_conversation()
        
        # Enhance message with intent detection
        enhanced_message = agent_engine.enhance_message_with_intent(user_message)
        
        # Add user message to conversation
        conversation.append({"role": "user", "content": enhanced_message})
        
        # Agent loop for multi-step reasoning
        iterations = 0
        max_iterations = 5
        tool_calls_made = []
        
        while iterations < max_iterations:
            iterations += 1
            
            try:
                if openrouter_api_key:
                    # Use OpenRouter API format
                    # Use full conversation for better context
                    payload = {
                        "model": MODEL,
                        "messages": conversation,
                        "temperature": 0.7,
                        "max_tokens": 1000
                    }
                else:
                    # Fallback to Hugging Face format
                    prompt = "<s>[INST] "
                    system_message = None
                    conversation_messages = []
                    
                    for msg in conversation:
                        if msg["role"] == "system":
                            system_message = msg["content"]
                        else:
                            conversation_messages.append(msg)
                    
                    if system_message:
                        prompt += f"<<SYS>>\n{system_message}\n<</SYS>>\n\n"
                    
                    for i, msg in enumerate(conversation_messages):
                        if msg["role"] == "user":
                            if i > 0:
                                prompt += "[INST] "
                            prompt += f"{msg['content']} [/INST]"
                        elif msg["role"] == "assistant":
                            prompt += f" {msg['content']}</s>"
                    
                    payload = {
                        "inputs": prompt,
                        "parameters": {
                            "max_new_tokens": 1000,
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "return_full_text": False
                        }
                    }
                
                print(f"\n=== Iteration {iterations} ===")
                print(f"Sending request to: {API_URL}")
                
                # Make request to API
                response = requests.post(
                    API_URL,
                    headers=API_HEADERS,
                    json=payload
                )
                
                print(f"Response status: {response.status_code}")
                
                if response.status_code != 200:
                    return jsonify({"error": f"API error: {response.text}"}), 500
                
                response_data = response.json()
                
                if openrouter_api_key:
                    if "choices" in response_data and len(response_data["choices"]) > 0:
                        ai_response = response_data["choices"][0]["message"]["content"].strip()
                        if not ai_response:
                            ai_response = "I'm processing your request. How can I help you?"
                    else:
                        ai_response = "Sorry, I couldn't generate a response. Please try again."
                else:
                    if isinstance(response_data, list) and len(response_data) > 0:
                        ai_response = response_data[0]['generated_text'].strip()
                    else:
                        ai_response = "Sorry, I couldn't generate a response. Please try again."
                
                print(f"AI Response: {ai_response[:200]}...")
                
                # Check if AI wants to use a tool
                tool_name, parameters = agent_engine.parse_tool_call(ai_response)
                
                if tool_name:
                    print(f"Tool call detected: {tool_name} with params: {parameters}")
                    
                    # Execute the tool
                    tool_result = agent_engine.execute_tool_call(tool_name, parameters)
                    tool_calls_made.append({
                        'tool': tool_name,
                        'parameters': parameters,
                        'result': tool_result
                    })
                    
                    print(f"Tool result: {tool_result}")
                    
                    # Add AI response with tool call to conversation
                    conversation.append({"role": "assistant", "content": ai_response})
                    
                    # Add tool result to conversation
                    tool_result_message = agent_engine.format_tool_result(tool_name, tool_result)
                    conversation.append({"role": "user", "content": tool_result_message})
                    
                    # Continue loop to let AI process the result
                    continue
                else:
                    # No tool call, this is the final response
                    conversation.append({"role": "assistant", "content": ai_response})
                    session['conversation'] = conversation
                    
                    return jsonify({
                        "reply": ai_response,
                        "tool_calls": tool_calls_made,
                        "iterations": iterations
                    })
                
            except Exception as e:
                print(f"Exception in iteration {iterations}: {str(e)}")
                return jsonify({"error": f"API error: {str(e)}"}), 500
        
        # Max iterations reached
        final_response = "I've completed the task. Let me know if you need anything else!"
        conversation.append({"role": "assistant", "content": final_response})
        session['conversation'] = conversation
        
        return jsonify({
            "reply": final_response,
            "tool_calls": tool_calls_made,
            "iterations": iterations
        })
        
    except Exception as e:
        print(f"Exception in chat endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/tools', methods=['GET'])
def list_tools():
    """List all available tools"""
    from tools import TOOL_DEFINITIONS
    return jsonify({
        'status': 'success',
        'tools': TOOL_DEFINITIONS
    })

@app.route('/execute-tool', methods=['POST'])
def execute_tool_endpoint():
    """Execute a specific tool directly"""
    try:
        data = request.get_json()
        if not data or 'tool_name' not in data:
            return jsonify({"error": "tool_name is required"}), 400
        
        tool_name = data['tool_name']
        parameters = data.get('parameters', {})
        
        result = execute_tool(tool_name, **parameters)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_conversation():
    """Clear the conversation history"""
    session.pop('conversation', None)
    return jsonify({"status": "conversation cleared"})

if __name__ == '__main__':
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'True') == 'True'
    )