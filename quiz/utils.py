import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = os.path.join(BASE_DIR, 'data', 'questions.txt')

def load_questions():
    questions = []
    if not os.path.exists(DATA_FILE):
        return questions
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 4:
                questions.append({
                    'id': len(questions) + 1,
                    'text': parts[0],
                    'option1': parts[1],
                    'option2': parts[2],
                    'correct': parts[3]
                })
    return questions

def save_questions(questions):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        for q in questions:
            f.write(f"{q['text']}|{q['option1']}|{q['option2']}|{q['correct']}\n")