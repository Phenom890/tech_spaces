from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('ask/question/', views.AskQuestion.as_view(), name='ask_question'),
    path('question/<int:pk>/view/', views.GetQuestionView.as_view(), name='get_question'),
    path('question/<int:pk>/delete/', views.DeleteQuestion.as_view(), name='delete_question'),
    path('answer/<int:pk>/delete/', views.DeleteAnswer.as_view(), name='delete_answer'),
]
