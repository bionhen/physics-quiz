def teacher_context(request):
    return {
        'is_teacher': request.session.get('is_teacher', False)
    }