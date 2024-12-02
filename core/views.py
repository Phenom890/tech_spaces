from mailbox import Message
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import AskQuestionForm
from .models import Question, Course, Answer


# TODO: add view for all the courses and recent activities
# TODO: add font awesome to the site

class Index(View):
    def get(self, request):
        courses = Course.objects.filter()[:5]
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


class GetQuestionView(LoginRequiredMixin, View):
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


class AskQuestion(LoginRequiredMixin, View):
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


class UpdateQuestion(LoginRequiredMixin, View):
    def get(self, request, pk):
        curr_question = get_object_or_404(Question, id=pk)
        form = AskQuestionForm(instance=curr_question)
        context = {
            'question': curr_question,
            'form': form,
        }
        return render(request, 'core/update_question.html', context)

    def post(self, request, pk):
        curr_question = get_object_or_404(Question, id=pk)
        form = AskQuestionForm(request.POST or None, instance=curr_question)
        if form.is_valid():
            update_question = form.save(commit=False)
            course_name = request.POST.get('course')
            question_course, created = Course.objects.get_or_create(name=course_name)
            update_question.course = question_course
            update_question.save()
            messages.success(request, 'Question Updated Successfully!')
            return redirect('get_question', pk=curr_question.id)
        messages.error(request, 'Check form and fill it correctly!!')
        return redirect('update_question', pk=curr_question.id)


class DeleteQuestion(LoginRequiredMixin, View):
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


class DeleteAnswer(LoginRequiredMixin, View):
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


class UpVote(LoginRequiredMixin, View):
    def get(self, request, pk):
        answer = get_object_or_404(Answer, id=pk)
        answer.up_votes += 1
        answer.save()
        return redirect('get_question', pk=answer.question.id)


class DownVote(LoginRequiredMixin, View):
    def get(self, request, pk):
        answer = get_object_or_404(Answer, id=pk)
        answer.down_votes += 1
        answer.save()
        return redirect('get_question', pk=answer.question.id)


class AllCoursesView(View):
    def get(self, request):
        question_count = Question.objects.all().count()
        query = request.GET.get('query') if request.GET.get('query') else ""
        courses = Course.objects.filter(name__icontains=query)

        context = {
            'courses': courses,
            'question_count': question_count,
        }
        return render(request, 'core/all_courses.html', context)


class AllActivitiesView(View):
    def get(self, request):
        activities = Answer.objects.filter()
        context = {
            'question_answers': activities,
        }
        return render(request, 'core/all_activities.html', context)