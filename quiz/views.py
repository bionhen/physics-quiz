from django.shortcuts import render, redirect
from .forms import QuestionForm, QuizAnswerForm
from .utils import load_questions, save_questions

def home(request):
    return render(request, 'quiz/home.html')

def question_list(request):
    questions = load_questions()
    return render(request, 'quiz/question_list.html', {'questions': questions})

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            questions = load_questions()
            new_id = len(questions) + 1
            questions.append({
                'id': new_id,
                'text': form.cleaned_data['text'],
                'option1': form.cleaned_data['option1'],
                'option2': form.cleaned_data['option2'],
                'correct': form.cleaned_data['correct']
            })
            save_questions(questions)
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'quiz/add_question.html', {'form': form})

def quiz_view(request):
    questions = load_questions()
    if not questions:
        return render(request, 'quiz/no_questions.html')
    
    if request.method == 'POST':
        form = QuizAnswerForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for q in questions:
                user_answer = form.cleaned_data[f'q_{q["id"]}']
                if user_answer == q['correct']:
                    score += 1
            return render(request, 'quiz/result.html', {'score': score, 'total': len(questions)})
    else:
        form = QuizAnswerForm(questions=questions)
    return render(request, 'quiz/quiz.html', {'form': form, 'questions': questions})
