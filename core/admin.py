from django.contrib import admin
from .models import User, Question, Course, Answer


admin.site.register(User)
admin.site.register(Question)
admin.site.register(Course)
admin.site.register(Answer)
