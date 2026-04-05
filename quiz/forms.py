from django import forms

class QuestionForm(forms.Form):
    text = forms.CharField(max_length=200, label="Вопрос", widget=forms.Textarea)
    option1 = forms.CharField(max_length=100, label="Вариант 1")
    option2 = forms.CharField(max_length=100, label="Вариант 2")
    correct = forms.ChoiceField(
        choices=[('option1', 'Вариант 1'), ('option2', 'Вариант 2')],
        label="Правильный ответ"
    )

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text.strip()) < 5:
            raise forms.ValidationError("Вопрос должен содержать минимум 5 символов.")
        return text

class QuizAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for q in questions:
            self.fields[f'q_{q["id"]}'] = forms.ChoiceField(
                choices=[('option1', q['option1']), ('option2', q['option2'])],
                label=q['text'],
                widget=forms.RadioSelect
            )
            
class LoginForm(forms.Form):
    password = forms.CharField(
        label="Пароль преподавателя",
        widget=forms.PasswordInput,
        help_text="Введите пароль для доступа к редактированию"
    )
    
    def clean_password(self):
        password = self.cleaned_data['password']
        from .auth import check_password
        if not check_password(password):
            raise forms.ValidationError("Неверный пароль!")
        return password
