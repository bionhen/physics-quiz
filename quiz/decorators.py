from django.shortcuts import redirect
from django.contrib import messages

def teacher_required(view_func):
    """Декоратор для ограничения доступа только преподавателям"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_teacher', False):
            messages.error(request, "Доступ запрещён. Требуются права преподавателя.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper