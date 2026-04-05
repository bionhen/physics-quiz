# Physics Quiz

Квиз по физике на Django с ролями ученик/преподаватель.

## О проекте

Physics Quiz — это проект, который позволяет:
- Ученикам проходить тестирование по физике и получать результат
- Преподавателям управлять базой вопросов (добавление, редактирование, удаление)

## Быстрый старт

```bash
git clone https://github.com/bionhen/physics-quiz
cd physics-quiz
python -m venv venv
venv\Scripts\activate  # Windows
pip install django
python manage.py migrate
python manage.py runserver