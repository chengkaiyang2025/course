# HTML to Python Connection Guide

This document explains how the HTML file reads variables from the Python n-gram model.

## Current Architecture

### **Before (No Connection)**
```
HTML File (jeopardy_web_interface.html)
├── Hardcoded mock data
├── JavaScript-only logic
└── No Python integration
```

### **After (Connected to Python)**
```
HTML File (templates/jeopardy_interface.html)
├── Flask Web Server (app.py)
├── Python N-Gram Model (jeopardy_ngram_model.py)
├── API Endpoints
└── Real data from JSON file
```

## How the Connection Works

### **1. Flask Web Server (app.py)**

The Flask server acts as a bridge between HTML and Python:

```python
# Load the Python model
model = JeopardyNGramModel(n=3)
model.load_data('JEOPARDY_QUESTIONS1.json')
model.train_models()

# API endpoint to answer questions
@app.route('/api/answer', methods=['POST'])
def answer_question():
    data = request.json
    question = data.get('question', '').strip()
    
    # Use the Python model to get answer
    answer = model.answer_question(question)
    
    return jsonify({
        "status": "success",
        "answer": answer,
        "confidence": confidence
    })
```

### **2. HTML JavaScript API Calls**

The HTML file makes HTTP requests to the Python backend:

```javascript
async function answerQuestion() {
    const question = document.getElementById('questionInput').value.trim();
    
    // Send request to Python backend
    const response = await fetch('/api/answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question: question})
    });
    
    const data = await response.json();
    
    // Display result from Python model
    document.getElementById('answerResult').innerHTML = `
        <div class="result">
            <h3>Answer from Python Model:</h3>
            <p><strong>${data.answer}</strong></p>
            <p><em>Confidence: ${data.confidence}%</em></p>
        </div>
    `;
}
```

## Data Flow

### **Step-by-Step Process:**

1. **User Input**: User types question in HTML form
2. **JavaScript**: Captures input and sends HTTP request
3. **Flask Server**: Receives request and calls Python model
4. **Python Model**: Processes question using n-gram algorithms
5. **Response**: Python returns result to Flask
6. **HTML Update**: JavaScript receives response and updates UI

### **Example Flow:**

```
User: "What is the capital of France?"
    ↓
HTML: fetch('/api/answer', {question: "What is the capital of France?"})
    ↓
Flask: model.answer_question("What is the capital of France?")
    ↓
Python: Find similar questions, return "Paris"
    ↓
Flask: jsonify({"answer": "Paris", "confidence": 85})
    ↓
HTML: Display "Paris" with 85% confidence
```

## API Endpoints

### **Available Endpoints:**

| Endpoint | Method | Purpose | Returns |
|----------|--------|---------|---------|
| `/api/train` | POST | Train the model | Training status |
| `/api/answer` | POST | Answer questions | Answer + confidence |
| `/api/generate` | POST | Generate questions | List of Q&A pairs |
| `/api/similar` | POST | Find similar questions | Similar questions list |
| `/api/stats` | GET | Get model statistics | Model info |

### **Example API Usage:**

```javascript
// Train model
await fetch('/api/train', {method: 'POST'});

// Answer question
const response = await fetch('/api/answer', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({question: "What is the capital of France?"})
});

// Get statistics
const stats = await fetch('/api/stats');
```

## Running the Connected System

### **1. Install Dependencies:**
```bash
pip install -r requirements.txt
```

### **2. Start Flask Server:**
```bash
cd modules/llm
python app.py
```

### **3. Access Web Interface:**
```
http://localhost:5000
```

### **4. File Structure:**
```
modules/llm/
├── app.py                          # Flask server
├── jeopardy_ngram_model.py         # Python n-gram model
├── JEOPARDY_QUESTIONS1.json        # Dataset
├── templates/
│   └── jeopardy_interface.html     # Connected HTML
├── requirements.txt                # Dependencies
└── README_connection.md           # This file
```

## Key Differences

### **Before (Mock Data):**
```javascript
// Hardcoded data in HTML
const mockData = {
    questions: ["What is the capital of France?"],
    answers: ["Paris"]
};
```

### **After (Real Python Data):**
```javascript
// Real data from Python model
const response = await fetch('/api/answer', {
    method: 'POST',
    body: JSON.stringify({question: userQuestion})
});
const data = await response.json();
// data.answer comes from Python n-gram model
```

## Benefits of This Connection

### **✅ Real Data Processing:**
- Uses actual Jeopardy dataset from JSON file
- Real n-gram model predictions
- Dynamic vocabulary building

### **✅ Scalability:**
- Can handle large datasets
- Server-side processing
- Better performance

### **✅ Flexibility:**
- Easy to modify Python model
- Can add new features
- API-based architecture

### **✅ Error Handling:**
- Proper error responses
- Connection status monitoring
- Graceful fallbacks

## Troubleshooting

### **Common Issues:**

1. **"Cannot connect to Python backend"**
   - Make sure Flask server is running
   - Check if port 5000 is available
   - Verify all dependencies are installed

2. **"Model not trained"**
   - Click "Load & Train Model" button
   - Check if JSON file exists
   - Look for error messages in Flask console

3. **"Failed to get answer"**
   - Check Flask server logs
   - Verify JSON file format
   - Ensure model is properly trained

### **Debug Mode:**
```bash
# Run Flask in debug mode
export FLASK_ENV=development
python app.py
```

This will show detailed error messages and auto-reload on changes.

## Summary

The HTML file now **truly reads variables from the Python file** through:

1. **Flask Web Server** as middleware
2. **HTTP API endpoints** for communication
3. **JSON data exchange** between frontend and backend
4. **Real Python model** processing instead of mock data

This creates a proper full-stack application where the frontend (HTML/JavaScript) communicates with the backend (Python) to get real n-gram model predictions! 