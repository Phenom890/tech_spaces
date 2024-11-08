from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import AskQuestionForm
from .models import Question, Course, Answer


# TODO: add the upvote and downvote buttons to the answers
# TODO: add the upvote and downvote functionality to the answers
# TODO:add bootstrap css and js to the project
# TODO: add the error details in forms for clarification


class Index(View):
    def get(self, request):
        courses = Course.objects.filter()
        query = request.GET.get('query') if request.GET.get('query') else ""

        questions = Question.objects.filter(
            Q(course__name__icontains=query) |
            Q(name__icontains=query) |
            Q(student__username__icontains=query) |
            Q(description__icontains=query)
        )
        question_count = Question.objects.all().count()

        # FIXME:fix this code to display the acitvities for all quesitons not only those selected
        #  from the course component
        answers = Answer.objects.filter(question__course__name__icontains=query).order_by(
            '-created')

        context = {
            'query_questions': questions,
            'courses': courses,
            'question_answers': answers,
            'question_count': question_count,
        }
        return render(request, 'core/index.html', context)


class GetQuestionView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, id=pk)
        answers = question.answer_set.all()
        students = question.contributors.all()
        context = {
            'question': question,
            'answers': answers,
            'contributors': students,
        }
        return render(request, 'core/question.html', context)

    def post(self, request, pk):
        question = get_object_or_404(Question, id=pk)
        answers = question.answer_set.all()
        students = question.contributors.all()
        answer_body = request.POST.get('answer_body')
        question.answer_set.create(
            student=request.user,
            body=answer_body
        )
        question.contributors.add(request.user)
        question.save()
        context = {
            'question': question,
            'answers': answers,
            'contributors': students,
        }
        return render(request, 'core/question.html', context)


class AskQuestion(View):
    def get(self, request):
        form = AskQuestionForm()
        courses = Course.objects.filter()
        context = {
            'form': form,
            'courses': courses,
        }
        return render(request, 'core/ask_question.html', context)

    def post(self, request):
        form = AskQuestionForm(request.POST or None)

        if form.is_valid():
            courses = Course.objects.filter()
            course_name = request.POST.get('course')
            course, created = Course.objects.get_or_create(name=course_name)
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')

            question = Question()
            question.name = name
            question.course = course
            question.description = description
            question.student = request.user
            question.save()
            question.contributors.add(request.user)
            question.save()

            messages.success(request, 'Question Asked Successfully!')
            return redirect('home')
        messages.error(request, 'Check the fields and fill them correctly!')


class DeleteQuestion(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, id=pk)
        context = {
            'obj': question,
        }
        return render(request, 'core/delete.html', context)

    def post(self, request, pk):
        question = get_object_or_404(Question, id=pk)
        question.delete()
        messages.info(request, 'Question Removed Successful!')
        return redirect('home')


class DeleteAnswer(View):
    def get(self, request, pk):
        get_answer = get_object_or_404(Answer, id=pk)
        context = {
            'obj': get_answer,
        }
        return render(request, 'core/delete.html', context)

    def post(self, request, pk):
        get_answer = get_object_or_404(Answer, id=pk)
        get_answer.delete()
        return redirect('home')
