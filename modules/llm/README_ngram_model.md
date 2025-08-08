# Jeopardy N-Gram Model

This project implements an n-gram language model for answering Jeopardy questions using the Jeopardy dataset.

## Overview

The n-gram model is a statistical language model that predicts the next word in a sequence based on the previous n-1 words. In this implementation, we use n-grams to:

1. **Generate new Jeopardy questions** based on patterns in the training data
2. **Answer questions** by finding similar questions in the dataset
3. **Find similar questions** using word overlap similarity

## Files

- `jeopardy_ngram_model.py` - Python implementation of the n-gram model
- `jeopardy_web_interface.html` - Web interface for interacting with the model
- `JEOPARDY_QUESTIONS1.json` - Dataset containing Jeopardy questions and answers

## How N-Gram Models Work

### 1. N-Gram Construction
An n-gram is a sequence of n consecutive words. For example, in the sentence "What is the capital of France":
- 1-grams (unigrams): ["What", "is", "the", "capital", "of", "France"]
- 2-grams (bigrams): [("What", "is"), ("is", "the"), ("the", "capital"), ("capital", "of"), ("of", "France")]
- 3-grams (trigrams): [("What", "is", "the"), ("is", "the", "capital"), ("the", "capital", "of"), ("capital", "of", "France")]

### 2. Probability Calculation
The model calculates the probability of a word given its context using:
```
P(word|context) = count(context, word) / count(context)
```

### 3. Smoothing
To handle unseen n-grams, we use Add-1 (Laplace) smoothing:
```
P(word|context) = (count(context, word) + 1) / (count(context) + |V|)
```
where |V| is the vocabulary size.

## Usage

### Python Script

1. **Load and train the model:**
```python
from jeopardy_ngram_model import JeopardyNGramModel

model = JeopardyNGramModel(n=3)
model.load_data('JEOPARDY_QUESTIONS1.json')
model.train_models()
```

2. **Answer a question:**
```python
answer = model.answer_question("What is the capital of France?")
print(answer)  # Output: Paris
```

3. **Generate new questions:**
```python
question = model.generate_question()
print(question)  # Output: Generated question based on training data
```

4. **Find similar questions:**
```python
similar = model.find_similar_questions("What is the capital of France?", top_k=5)
for q, a, sim in similar:
    print(f"Q: {q}")
    print(f"A: {a}")
    print(f"Similarity: {sim:.3f}")
```

### Web Interface

1. Open `jeopardy_web_interface.html` in a web browser
2. Click "Load & Train Model" to initialize the model
3. Use the interface to:
   - Ask questions and get answers
   - Generate new questions
   - Find similar questions
   - View model statistics

## Model Architecture

### Classes

1. **NGramModel**: Core n-gram implementation
   - `train(texts)`: Train on a list of texts
   - `get_probability(context, word)`: Calculate word probability
   - `predict_next_word(context)`: Predict next word

2. **JeopardyNGramModel**: Jeopardy-specific wrapper
   - `load_data(file_path)`: Load JSON dataset
   - `answer_question(question)`: Answer questions
   - `generate_question()`: Generate new questions
   - `find_similar_questions(query, top_k)`: Find similar questions

### Key Features

- **Text Preprocessing**: Removes HTML tags and special characters
- **Smoothing**: Add-1 smoothing for unseen n-grams
- **Similarity Matching**: Word overlap-based similarity
- **Multiple Models**: Separate models for questions, answers, and categories

## Example Output

```
=== Generated Questions and Answers ===
Q1: What is the capital of Germany?
A1: Berlin

Q2: Who wrote Hamlet?
A2: William Shakespeare

=== Question Answering Demo ===
Q: What is the capital of France?
A: Paris
Confidence: 85%

=== Similar Questions Demo ===
Query: What is the capital of France?
Similar questions:
1. Q: What is the capital of Germany?
   A: Berlin
   Similarity: 0.750
```

## Limitations

1. **Simple Similarity**: Uses basic word overlap for similarity
2. **No Semantic Understanding**: Doesn't understand meaning, only patterns
3. **Limited Context**: Only considers n-1 previous words
4. **Training Data Dependent**: Quality depends on the dataset

## Future Improvements

1. **Better Similarity**: Implement cosine similarity or word embeddings
2. **Semantic Understanding**: Use transformer models or word vectors
3. **Context Window**: Increase n-gram size for better context
4. **Advanced Smoothing**: Implement Kneser-Ney or other smoothing techniques
5. **Answer Generation**: Generate answers instead of just retrieving them

## Technical Details

### N-Gram Size
- Default: n=3 (trigrams)
- Can be adjusted based on dataset size and requirements
- Larger n provides more context but requires more training data

### Vocabulary
- Built from all unique words in the training data
- Includes special tokens: `<START>`, `<END>`
- Case-insensitive processing

### Performance
- Training time: O(N × n) where N is total words, n is n-gram size
- Query time: O(V) where V is vocabulary size
- Memory usage: O(V^n) for n-gram counts

## Dependencies

- Python 3.6+
- Standard library only (no external dependencies)
- Web interface: HTML, CSS, JavaScript (no frameworks)

## Running the Model

```bash
# Run the Python script
python jeopardy_ngram_model.py

# Open the web interface
# Open jeopardy_web_interface.html in a web browser
```

The model will automatically load the JSON dataset and demonstrate various capabilities including question answering, question generation, and similarity search. 