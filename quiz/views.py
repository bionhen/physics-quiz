from django.shortcuts import render, redirect
from .forms import QuestionForm, QuizAnswerForm, LoginForm
from .utils import load_questions, save_questions
from django.contrib import messages

def home(request):
    return render(request, 'quiz/home.html')

def question_list(request):
    # Только для преподавателей
    if not is_teacher(request):
        messages.error(request, "Доступ запрещён. Эта страница только для преподавателей.")
        return redirect('home')
    
    questions = load_questions()
    return render(request, 'quiz/question_list.html', {
        'questions': questions,
        'show_correct': True,  # Преподаватель всегда видит ответы
        'is_teacher': True
    })

def add_question(request):
    # Проверка: только преподаватель
    if not is_teacher(request):
        messages.error(request, "Доступ только для преподавателей!")
        return redirect('teacher_login')
    
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
            messages.success(request, "Вопрос успешно добавлен!")
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

def teacher_login(request):
    """Страница входа для преподавателя"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['is_teacher'] = True
            messages.success(request, "Добро пожаловать, преподаватель!")
            return redirect('add_question')
    else:
        form = LoginForm()
    return render(request, 'quiz/teacher_login.html', {'form': form})

def teacher_logout(request):
    """Выход из режима преподавателя"""
    if 'is_teacher' in request.session:
        del request.session['is_teacher']
        messages.info(request, "Вы вышли из режима преподавателя")
    return redirect('home')

def is_teacher(request):
    """Проверка, авторизован ли преподаватель"""
    return request.session.get('is_teacher', False)