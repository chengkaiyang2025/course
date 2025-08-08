from flask import Flask, render_template, request, jsonify
from jeopardy_ngram_model import JeopardyNGramModel
import os

app = Flask(__name__)

# Initialize the model
model = None
is_trained = False

def load_model():
    global model, is_trained
    if not is_trained:
        model = JeopardyNGramModel(n=3)
        try:
            model.load_data('JEOPARDY_QUESTIONS1.json')
            model.train_models()
            is_trained = True
            print("Model loaded and trained successfully!")
        except FileNotFoundError:
            print("Error: JEOPARDY_QUESTIONS1.json not found")
            return False
    return True

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('jeopardy_interface.html')

@app.route('/api/train', methods=['POST'])
def train_model():
    """API endpoint to train the model"""
    global is_trained
    if load_model():
        return jsonify({
            "status": "success",
            "message": "Model trained successfully",
            "questions_count": len(model.questions),
            "vocab_size": len(model.question_model.vocab),
            "categories_count": len(set(model.categories))
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to load training data"
        }), 500

@app.route('/api/answer', methods=['POST'])
def answer_question():
    """API endpoint to answer questions"""
    if not load_model():
        return jsonify({
            "status": "error",
            "message": "Model not trained"
        }), 400
    
    data = request.json
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({
            "status": "error",
            "message": "No question provided"
        }), 400
    
    # Get answer using the Python model
    answer = model.answer_question(question)
    
    # Find similar questions for confidence calculation
    similar_questions = model.find_similar_questions(question, top_k=1)
    confidence = similar_questions[0][2] if similar_questions else 0
    
    return jsonify({
        "status": "success",
        "answer": answer,
        "confidence": round(confidence * 100, 1),
        "similar_question": similar_questions[0][0] if similar_questions else ""
    })

@app.route('/api/generate', methods=['POST'])
def generate_questions():
    """API endpoint to generate questions"""
    if not load_model():
        return jsonify({
            "status": "error", 
            "message": "Model not trained"
        }), 400
    
    data = request.json
    num_questions = data.get('num_questions', 3)
    
    generated_questions = []
    for _ in range(num_questions):
        question = model.generate_question()
        answer = model.generate_answer()
        generated_questions.append({
            "question": question,
            "answer": answer
        })
    
    return jsonify({
        "status": "success",
        "questions": generated_questions
    })

@app.route('/api/similar', methods=['POST'])
def find_similar():
    """API endpoint to find similar questions"""
    if not load_model():
        return jsonify({
            "status": "error",
            "message": "Model not trained"
        }), 400
    
    data = request.json
    query = data.get('query', '').strip()
    top_k = data.get('top_k', 5)
    
    if not query:
        return jsonify({
            "status": "error",
            "message": "No query provided"
        }), 400
    
    similar_questions = model.find_similar_questions(query, top_k=top_k)
    
    results = []
    for question, answer, similarity in similar_questions:
        results.append({
            "question": question,
            "answer": answer,
            "similarity": round(similarity * 100, 1)
        })
    
    return jsonify({
        "status": "success",
        "results": results
    })

@app.route('/api/stats')
def get_stats():
    """API endpoint to get model statistics"""
    if not load_model():
        return jsonify({
            "status": "error",
            "message": "Model not trained"
        }), 400
    
    return jsonify({
        "status": "success",
        "stats": {
            "questions_count": len(model.questions),
            "vocab_size": len(model.question_model.vocab),
            "categories_count": len(set(model.categories)),
            "is_trained": is_trained
        }
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("Starting Jeopardy N-Gram Model Server...")
    print("Access the interface at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 