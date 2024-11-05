from django.shortcuts import render

from .models import Question, Course


def index(request):
    questions = Question.objects.all()
    courses = Course.objects.all()
    
    context = {
        'query_questions': questions,
        'courses': courses,
    }
    return render(request, 'core/index.html', context)
