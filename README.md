# AI Assistant Backend

A Flask-based REST API backend for an AI Assistant powered by OpenAI's ChatGPT API.

## 📁 Project Structure

```
ai_assistant_backend/
│
├── app.py                 # Main Flask application
├── .env                   # Environment variables (API keys)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── test_requests/
    └── test_api.py       # API testing script
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
cd ai_assistant_backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Edit the `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True
```

**Get your OpenAI API key from:** https://platform.openai.com/api-keys

### 3. Run the Backend Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

## 📡 API Endpoints

### 1. Health Check
- **URL:** `GET /`
- **Description:** Check if the server is running
- **Response:**
```json
{
  "status": "success",
  "message": "AI Assistant Backend is running",
  "version": "1.0.0"
}
```

### 2. Chat Endpoint
- **URL:** `POST /api/chat`
- **Description:** Send a message to the AI assistant
- **Request Body:**
```json
{
  "message": "Your question here",
  "conversation_history": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```
- **Response:**
```json
{
  "status": "success",
  "response": "AI generated response",
  "model": "gpt-3.5-turbo",
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 100,
    "total_tokens": 150
  }
}
```

### 3. Available Models
- **URL:** `GET /api/models`
- **Description:** Get list of available OpenAI models
- **Response:**
```json
{
  "status": "success",
  "models": ["gpt-3.5-turbo", "gpt-4", ...]
}
```

## 🧪 Testing the API

### Using the Test Script

```bash
cd test_requests
python test_api.py
```

This will run comprehensive tests on all endpoints.

### Using cURL

**Health Check:**
```bash
curl http://localhost:5000/
```

**Send a Chat Message:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Hello, how are you?\"}"
```

**Get Available Models:**
```bash
curl http://localhost:5000/api/models
```

### Using Postman or Thunder Client

1. Import the endpoints into your API testing tool
2. Set the base URL to `http://localhost:5000`
3. Test each endpoint with sample payloads

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` |
| `FLASK_HOST` | Flask server host | `0.0.0.0` |
| `FLASK_PORT` | Flask server port | `5000` |
| `FLASK_DEBUG` | Enable debug mode | `True` |

## 🛡️ Error Handling

The API includes comprehensive error handling:
- **400 Bad Request:** Invalid or missing parameters
- **500 Internal Server Error:** Server or OpenAI API errors

All errors return JSON with:
```json
{
  "status": "error",
  "message": "Error description"
}
```

## 📝 Features

- ✅ RESTful API design
- ✅ CORS enabled for frontend integration
- ✅ Conversation history support
- ✅ Token usage tracking
- ✅ Multiple model support
- ✅ Comprehensive error handling
- ✅ Environment-based configuration
- ✅ Health check endpoint

## 🔜 Next Steps

1. **Frontend Integration:** Connect a React/Vue/Angular frontend
2. **Database:** Add conversation persistence with SQLite/PostgreSQL
3. **Authentication:** Implement user authentication and API keys
4. **Rate Limiting:** Add request rate limiting
5. **Logging:** Implement comprehensive logging
6. **Deployment:** Deploy to cloud platforms (Heroku, AWS, etc.)

## 📄 License

This project is open source and available for educational purposes.
