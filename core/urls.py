from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('ask/question/', views.AskQuestion.as_view(), name='ask_question'),
    path('question/<int:pk>/view/', views.GetQuestionView.as_view(), name='get_question'),
]
