from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import QuestionForm, QuizAnswerForm, LoginForm, QuestionEditForm
from .utils import load_questions, save_questions
from .decorators import teacher_required

def home(request):
    return render(request, 'quiz/home.html')

@teacher_required
def question_list(request):
    # Только для преподавателей
    
    questions = load_questions()
    return render(request, 'quiz/question_list.html', {
        'questions': questions,
        'show_correct': True,  # Преподаватель всегда видит ответы
    })

@teacher_required
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
    # Если уже авторизован — редирект
    if request.session.get('is_teacher', False):
        messages.info(request, "Вы уже авторизованы как преподаватель")
        return redirect('question_list')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['is_teacher'] = True
            messages.success(request, "Добро пожаловать, преподаватель!")
            return redirect('question_list')
    else:
        form = LoginForm()
    return render(request, 'quiz/teacher_login.html', {'form': form})

def teacher_logout(request):
    """Выход из режима преподавателя"""
    if 'is_teacher' in request.session:
        del request.session['is_teacher']
        messages.info(request, "Вы вышли из режима преподавателя")
    return redirect('home')


@teacher_required
def question_edit(request, q_id):
    """Редактирование вопроса"""
    questions = load_questions()
    
    # Находим вопрос по id
    question = None
    for q in questions:
        if q['id'] == q_id:
            question = q
            break
    
    if not question:
        messages.error(request, "Вопрос не найден")
        return redirect('question_list')
    
    if request.method == 'POST':
        form = QuestionEditForm(request.POST)
        if form.is_valid():
            # Обновляем вопрос
            question['text'] = form.cleaned_data['text']
            question['option1'] = form.cleaned_data['option1']
            question['option2'] = form.cleaned_data['option2']
            question['correct'] = form.cleaned_data['correct']
            
            save_questions(questions)
            messages.success(request, "Вопрос успешно обновлён!")
            return redirect('question_list')
    else:
        # Заполняем форму текущими данными
        form = QuestionEditForm(initial={
            'text': question['text'],
            'option1': question['option1'],
            'option2': question['option2'],
            'correct': question['correct'],
        })
    
    return render(request, 'quiz/question_edit.html', {'form': form, 'question_id': q_id})

@teacher_required
def question_delete(request, q_id):
    """Удаление вопроса"""
    questions = load_questions()
    
    # Находим и удаляем вопрос
    new_questions = [q for q in questions if q['id'] != q_id]
    
    # Перенумеровываем id
    for i, q in enumerate(new_questions, 1):
        q['id'] = i
    
    save_questions(new_questions)
    messages.success(request, "Вопрос успешно удалён!")
    return redirect('question_list')