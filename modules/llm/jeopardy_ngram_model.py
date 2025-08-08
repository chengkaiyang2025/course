import json
import re
import random
from collections import defaultdict, Counter
from typing import List, Dict, Tuple
import math

class NGramModel:
    def __init__(self, n: int = 3):
        self.n = n
        self.ngram_counts = defaultdict(Counter)
        self.context_counts = defaultdict(int)
        self.vocab = set()
        
    def preprocess_text(self, text: str) -> List[str]:
        """Clean and tokenize text"""
        # Remove HTML tags and special characters
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        # Convert to lowercase and split
        tokens = text.lower().split()
        return tokens
    
    def build_ngrams(self, tokens: List[str]) -> List[Tuple[str, ...]]:
        """Generate n-grams from tokens"""
        ngrams = []
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i + self.n])
            ngrams.append(ngram)
        return ngrams
    
    def train(self, texts: List[str]):
        """Train the n-gram model on a list of texts"""
        for text in texts:
            tokens = self.preprocess_text(text)
            self.vocab.update(tokens)
            
            # Add start and end markers
            padded_tokens = ['<START>'] * (self.n - 1) + tokens + ['<END>']
            
            # Generate n-grams
            ngrams = self.build_ngrams(padded_tokens)
            
            for ngram in ngrams:
                context = ngram[:-1]
                word = ngram[-1]
                self.ngram_counts[context][word] += 1
                self.context_counts[context] += 1
    
    def get_probability(self, context: Tuple[str, ...], word: str) -> float:
        """Get probability of word given context"""
        if context not in self.ngram_counts:
            return 1.0 / len(self.vocab)  # Laplace smoothing
        
        count = self.ngram_counts[context][word]
        total = self.context_counts[context]
        
        # Add-1 smoothing
        return (count + 1) / (total + len(self.vocab))
    
    def predict_next_word(self, context: Tuple[str, ...]) -> str:
        """Predict the most likely next word given context"""
        if context not in self.ngram_counts:
            return random.choice(list(self.vocab))
        
        best_word = None
        best_prob = -1
        
        for word in self.ngram_counts[context]:
            prob = self.get_probability(context, word)
            if prob > best_prob:
                best_prob = prob
                best_word = word
        
        return best_word if best_word else random.choice(list(self.vocab))

class JeopardyNGramModel:
    def __init__(self, n: int = 3):
        self.question_model = NGramModel(n)
        self.answer_model = NGramModel(n)
        self.category_model = NGramModel(n)
        self.questions = []
        self.answers = []
        self.categories = []
        
    def load_data(self, file_path: str):
        """Load Jeopardy data from JSON file"""
        print(f"Loading data from {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Loaded {len(data)} questions")
        
        for item in data:
            if 'question' in item and 'answer' in item:
                self.questions.append(item['question'])
                self.answers.append(item['answer'])
                if 'category' in item:
                    self.categories.append(item['category'])
        
        print(f"Processed {len(self.questions)} valid questions")
    
    def train_models(self):
        """Train all n-gram models"""
        print("Training question model...")
        self.question_model.train(self.questions)
        
        print("Training answer model...")
        self.answer_model.train(self.answers)
        
        print("Training category model...")
        self.category_model.train(self.categories)
        
        print("Training complete!")
    
    def generate_question(self, max_length: int = 20) -> str:
        """Generate a new Jeopardy question"""
        context = ('<START>',) * (self.question_model.n - 1)
        question = []
        
        for _ in range(max_length):
            next_word = self.question_model.predict_next_word(context)
            if next_word == '<END>':
                break
            question.append(next_word)
            context = context[1:] + (next_word,)
        
        return ' '.join(question)
    
    def generate_answer(self, max_length: int = 10) -> str:
        """Generate a new Jeopardy answer"""
        context = ('<START>',) * (self.answer_model.n - 1)
        answer = []
        
        for _ in range(max_length):
            next_word = self.answer_model.predict_next_word(context)
            if next_word == '<END>':
                break
            answer.append(next_word)
            context = context[1:] + (next_word,)
        
        return ' '.join(answer)
    
    def find_similar_questions(self, query: str, top_k: int = 5) -> List[Tuple[str, str, float]]:
        """Find questions similar to the query"""
        query_tokens = self.question_model.preprocess_text(query)
        similarities = []
        
        for i, question in enumerate(self.questions):
            question_tokens = self.question_model.preprocess_text(question)
            
            # Simple similarity based on common words
            common_words = set(query_tokens) & set(question_tokens)
            similarity = len(common_words) / max(len(set(query_tokens)), len(set(question_tokens)), 1)
            
            similarities.append((question, self.answers[i], similarity))
        
        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x[2], reverse=True)
        return similarities[:top_k]
    
    def answer_question(self, question: str) -> str:
        """Attempt to answer a question using the model"""
        # Find most similar question
        similar_questions = self.find_similar_questions(question, top_k=1)
        
        if similar_questions:
            return similar_questions[0][1]  # Return the answer to the most similar question
        
        # If no similar question found, generate a new answer
        return self.generate_answer()

def main():
    # Initialize the model
    model = JeopardyNGramModel(n=3)
    
    # Load and train the model
    try:
        model.load_data('JEOPARDY_QUESTIONS1.json')
        model.train_models()
    except FileNotFoundError:
        print("Error: JEOPARDY_QUESTIONS1.json not found in current directory")
        return
    
    # Demo: Generate some questions and answers
    print("\n=== Generated Questions and Answers ===")
    for i in range(5):
        question = model.generate_question()
        answer = model.generate_answer()
        print(f"Q{i+1}: {question}")
        print(f"A{i+1}: {answer}")
        print()
    
    # Demo: Answer some sample questions
    print("=== Question Answering Demo ===")
    sample_questions = [
        "What is the capital of France?",
        "Who wrote Romeo and Juliet?",
        "What is the largest planet in our solar system?",
        "In what year did World War II end?",
        "What is the chemical symbol for gold?"
    ]
    
    for question in sample_questions:
        answer = model.answer_question(question)
        print(f"Q: {question}")
        print(f"A: {answer}")
        print()
    
    # Demo: Find similar questions
    print("=== Similar Questions Demo ===")
    query = "What is the capital of France?"
    similar = model.find_similar_questions(query, top_k=3)
    
    print(f"Query: {query}")
    print("Similar questions:")
    for i, (question, answer, similarity) in enumerate(similar):
        print(f"{i+1}. Q: {question}")
        print(f"   A: {answer}")
        print(f"   Similarity: {similarity:.3f}")
        print()

if __name__ == "__main__":
    main() 
    