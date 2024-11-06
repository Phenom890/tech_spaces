from django import forms

from .models import Question


class AskQuestionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Give a short description about your question and how you want it answered',
    }))
    class Meta:
        model = Question
        fields = ['name', 'description']
